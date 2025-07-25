import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
import webbrowser

# === Quickbase Data Fetch ===
pd.set_option('display.max_columns', None)
# Specify the Site ID to query
target_Site_ID = "1036"  # replace with your desired Site_ID
api_token = "b856uu_qq8q_0_bax7pb6di4dudu2iave5drx5dk"
api_url = "https://api.quickbase.com/v1"
realm = "uirtus"
EQUIPMENT_TABLE_ID = "bukpkaqtr"
field_ids = [3,7,12,15,18,33,106,184,185,186,187,193]
headers = {
    "QB-Realm-Hostname": f"{realm}.quickbase.com",
    "Authorization": f"QB-USER-TOKEN {api_token}",
    "Content-Type": "application/json"
}
response = requests.post(
    f"{api_url}/records/query", verify=False,
    json={"from": EQUIPMENT_TABLE_ID, "select": field_ids, "where": f"{{33.EX.'{target_Site_ID}'}}"},
    headers=headers
).json()
fields = {f["id"]: f["label"] for f in response.get("fields", [])}
records = response.get("data", [])
df = pd.DataFrame([
    {fields[int(k)]: v.get("value") for k, v in record.items()}
    for record in records
])

# === Geometry Setup ===
height = 50  # tower height in meters
base_side = 3  # square side length for four-legged tower
# Define leg positions at square corners
leg_positions = {
    "Leg 1": np.array([0.0, 0.0]),
    "Leg 2": np.array([base_side, 0.0]),
    "Leg 3": np.array([base_side, base_side]),
    "Leg 4": np.array([0.0, base_side])
}
# Map Face labels to leg keys
face_map = {
    "Face A": "Leg 1",
    "Face B": "Leg 2",
    "Face C": "Leg 3",
    "Face 4": "Leg 4"
}
centroid = sum(leg_positions.values()) / len(leg_positions)

# Utility: mesh creation
def create_box_mesh(vertices, faces, color, name):
    verts = np.array(vertices)
    i, j, k = zip(*faces)
    return go.Mesh3d(
        x=verts[:,0], y=verts[:,1], z=verts[:,2],
        i=list(i), j=list(j), k=list(k),
        color=color, opacity=1.0, name=name
    )

# Ground (10×10 m grass)
ground_offset = centroid - np.array([5,5])
ground_verts = [
    [ground_offset[0], ground_offset[1], 0],
    [ground_offset[0]+10, ground_offset[1], 0],
    [ground_offset[0]+10, ground_offset[1]+10, 0],
    [ground_offset[0], ground_offset[1]+10, 0]
]
ground_faces = [[0,1,2], [0,2,3]]
ground = create_box_mesh(
    vertices=[*ground_verts] + [[0,0,-0.1]]*4,
    faces=ground_faces, color='green', name='Ground'
)

# Tower legs as vertical lines
def create_legs(positions, height):
    lines = []
    for name, pos in positions.items():
        lines.append(
            go.Scatter3d(
                x=[pos[0], pos[0]], y=[pos[1], pos[1]], z=[0, height],
                mode='lines', line=dict(color='gray', width=8), name=name
            )
        )
    return lines

# Horizontal & diagonal braces at 5m intervals
def create_braces(positions, height, interval=5):
    braces = []
    pts = list(positions.values())
    levels = np.arange(interval, height, interval)
    # horizontal braces
    for h in levels:
        for p1, p2 in zip(pts, pts[1:] + pts[:1]):
            braces.append(
                go.Scatter3d(
                    x=[p1[0], p2[0]], y=[p1[1], p2[1]], z=[h, h],
                    mode='lines', line=dict(color='black', width=4), showlegend=False
                )
            )
    # diagonal braces up one level
    for h in levels:
        h2 = h + interval
        if h2 > height: break
        for p1, p2 in zip(pts, pts[1:] + pts[:1]):
            braces.append(
                go.Scatter3d(
                    x=[p1[0], p2[0]], y=[p1[1], p2[1]], z=[h, h2],
                    mode='lines', line=dict(color='black', width=2), showlegend=False
                )
            )
    return braces

# RF panel (rectangular prism)
def create_rf_panel(pos, install_h, length, width, depth, color='skyblue'):
    L, W, D = length, width, depth
    dir_vec = (pos - centroid) / np.linalg.norm(pos - centroid)
    perp = np.array([-dir_vec[1], dir_vec[0]])
    base = pos + dir_vec * (D/2)
    verts = []
    for dz in [0, L]:
        for w in [-W/2, W/2]:
            for d in [-D/2, D/2]:
                p = base + perp * w + dir_vec * d
                verts.append([p[0], p[1], install_h + dz])
    faces = [
        [0,1,2],[1,2,3], [4,5,6],[5,6,7],
        [0,1,5],[0,5,4], [2,3,7],[2,7,6],
        [1,2,6],[1,6,5], [0,3,7],[0,7,4]
    ]
    return create_box_mesh(verts, faces, color, 'Equipment')

# MW dish as flat circular disc
def create_mw_dish(pos, install_h, diameter, color='white'):
    R = diameter / 2
    dir_vec = (pos - centroid) / np.linalg.norm(pos - centroid)
    # Disc plane: vertical and horiz perp
    v1 = np.array([0,0,1])
    v2 = np.array([-dir_vec[1], dir_vec[0], 0])
    center = np.array([pos[0], pos[1], install_h]) + np.append(dir_vec, 0) * R
    thetas = np.linspace(0, 2*np.pi, 50)
    verts = [list(center)]
    verts += [list(center + R*(v1*np.cos(th) + v2*np.sin(th))) for th in thetas]
    faces = [[0, i, i+1] for i in range(1, len(verts)-1)] + [[0, len(verts)-1, 1]]
    return create_box_mesh(verts, faces, color, 'Equipment')

# Build scene
elems = [ground] + create_legs(leg_positions, height) + create_braces(leg_positions, height)
for _, row in df.iterrows():
    raw = row.get('Face', '')
    leg_key = face_map.get(raw, raw)
    pos = leg_positions.get(leg_key)
    if pos is None: continue
    h0 = float(row.get('Install Height', 0))
    eq = row.get('Equipment Type', '')
    if eq == 'MW Dish':
        dia = row.get('Equipment Diameter (mm)', 0) / 1000.0
        elems.append(create_mw_dish(pos, h0, dia))
    else:
        L = row.get('Equipment Length (mm)', 0) / 1000.0
        W = row.get('Equipment Width (mm)', 0) / 1000.0
        D = row.get('Equipment Depth (mm)', 0) / 1000.0
        elems.append(create_rf_panel(pos, h0, L, W, D))

fig = go.Figure(data=elems)
fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
        aspectmode='data', bgcolor='skyblue'
    ),
    showlegend=False,
    title='3D Tower Visualization (4-Leg)',
    margin=dict(l=0, r=0, b=0, t=40),
    paper_bgcolor='white'
)
# Output
output_file = 'tower_visualization.html'
fig.write_html(output_file)
webbrowser.open(f'file://{os.path.abspath(output_file)}')