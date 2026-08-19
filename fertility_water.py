def estimate_fertility(coords, ai_text=None):
    """
    Prototype fertility / upjau indication.
    Later: NDVI or AI Vision result.
    """
    if ai_text and "fertility" in str(ai_text).lower():
        return str(ai_text)

    return {
        "level": "Medium",
        "reason": "Prototype estimate for rural agricultural plot. Replace with NDVI/AI.",
        "ndvi_note": "NDVI from Sentinel-2 Red+NIR can refine this score"
    }


def detect_water_resources(coords, ai_text=None):
    """
    Prototype water resource summary.
    Later: AI vision or water-layer overlay.
    """
    if ai_text and "water" in str(ai_text).lower():
        return str(ai_text)

    return {
        "nearby_water": "Not detected in prototype mode",
        "note": "AI Vision / Bhuvan-OSM layers will report pond, canal, river within ~500m–1km",
        "irrigation_hint": "Check satellite map visually for nearby canals or ponds"
    }


if __name__ == "__main__":
    from extract import get_plot_coordinates

    coords = get_plot_coordinates("Prayagraj", "Koraon", "Koodar", "30")
    print("Fertility:", estimate_fertility(coords))
    print("Water:", detect_water_resources(coords))