RESOURCE_NAMES = (
    "profile",
    "periods",
    "timetable",
    "homework",
    "absences",
    "delays",
    "punishments",
    "news",
    "menus",
    "grades",
    "averages",
)


def select_resources(data: dict, resources: list[str] | None) -> dict:
    if not resources:
        return data

    selected = {"export_metadata": data.get("export_metadata", {})}

    if "profile" in resources:
        selected["profile"] = data.get("user_info", {})
    if "periods" in resources:
        selected["periods"] = data.get("periods", [])
    if "timetable" in resources:
        selected["timetable"] = data.get("timetable", [])
    if "homework" in resources:
        selected["homework"] = data.get("homework", [])
    if "absences" in resources:
        selected["absences"] = data.get("absences", [])
    if "delays" in resources:
        selected["delays"] = data.get("delays", [])
    if "punishments" in resources:
        selected["punishments"] = data.get("punishments", [])
    if "news" in resources:
        selected["news"] = data.get("news", [])
    if "menus" in resources:
        selected["menus"] = data.get("menus", [])
    if "grades" in resources:
        selected["grades"] = [
            {"id": p.get("id"), "name": p.get("name"), "grades": p.get("grades", [])}
            for p in data.get("periods", [])
        ]
    if "averages" in resources:
        selected["averages"] = [
            {"id": p.get("id"), "name": p.get("name"), "averages": p.get("averages", [])}
            for p in data.get("periods", [])
        ]

    unknown = [resource for resource in resources if resource not in RESOURCE_NAMES]
    if unknown:
        selected["export_metadata"] = dict(selected["export_metadata"])
        selected["export_metadata"]["warnings"] = [f"Ressource inconnue ignorée : {resource}" for resource in unknown]

    return selected
