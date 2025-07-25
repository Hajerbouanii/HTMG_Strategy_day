for record in records:
    site_id = record.get("19", {}).get("value")
    height_str = record.get("30", {}).get("value")

    print(f"Site: {site_id} | Raw Height: {height_str}")  # 👈 add this

    try:
        height = float(height_str)
        if height > max_height:
            max_height = height
            max_site = site_id
    except (TypeError, ValueError):
        continue
