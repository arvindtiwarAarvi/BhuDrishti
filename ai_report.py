import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass


def generate_ai_report(plot_no, fertility_info, water_info, image_path=None):
    """
    AI property report.
    Agar OPENAI_API_KEY ho + image ho to real Vision call.
    Warna mock report (demo ke liye).
    """
    api_key = os.getenv("OPENAI_API_KEY", "")

    # Mock report — hamesha kaam karega (demo / SIH)
    fert_level = fertility_info.get("level", "Medium") if isinstance(fertility_info, dict) else "Medium"
    water_note = water_info.get("nearby_water", "Check satellite view") if isinstance(water_info, dict) else str(water_info)

    mock = {
        "land_use": "Agricultural / Rural plot",
        "fertility_indication": fert_level,
        "water_resources": water_note,
        "structures": "Open land — verify on satellite imagery",
        "summary": (
            f"Plot {plot_no}: Boundary extracted and overlaid on satellite view. "
            f"Fertility indication: {fert_level}. "
            f"Water: {water_note}. "
            "Full AI Vision can refine this when API key + map image are available."
        )
    }

    if not api_key or image_path is None:
        return mock

    # Real OpenAI Vision (optional)
    try:
        from openai import OpenAI
        import base64

        client = OpenAI(api_key=api_key)
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()

        prompt = """Analyze this cadastral plot on satellite imagery.
Reply in pure JSON with keys:
land_use, fertility_indication, water_resources, structures, summary"""

        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
                ]
            }],
            temperature=0.3
        )
        return {"raw": resp.choices[0].message.content}
    except Exception as e:
        mock["error"] = str(e)
        return mock


if __name__ == "__main__":
    from extract import get_plot_coordinates
    from fertility_water import estimate_fertility, detect_water_resources

    coords = get_plot_coordinates("Prayagraj", "Koraon", "Koodar", "30")
    fert = estimate_fertility(coords)
    water = detect_water_resources(coords)
    report = generate_ai_report("30", fert, water)
    print("AI Report:")
    for k, v in report.items():
        print(f"  {k}: {v}")