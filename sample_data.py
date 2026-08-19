# sample_data.py
# BhuDrishti - Sample Plot Data (Bhunaksha style)

SAMPLE_PLOTS = {
    # Format: (District, Tehsil, Village, Plot) : data
    ("Prayagraj", "Koraon", "Koodar", "30"): {
        "coordinates": [
            [81.8621, 25.2338],
            [81.8635, 25.2345],
            [81.8642, 25.2332],
            [81.8630, 25.2325],
            [81.8621, 25.2338]
        ],
        "area_sqm": 25370,
        "centroid": [81.8632, 25.2335]
    },
    ("Prayagraj", "Koraon", "Koodar", "31"): {
        "coordinates": [
            [81.8645, 25.2350],
            [81.8658, 25.2355],
            [81.8662, 25.2342],
            [81.8650, 25.2338],
            [81.8645, 25.2350]
        ],
        "area_sqm": 18200,
        "centroid": [81.8654, 25.2346]
    },
    ("Prayagraj", "Koraon", "Koodar", "45"): {
        "coordinates": [
            [81.8600, 25.2310],
            [81.8615, 25.2318],
            [81.8620, 25.2305],
            [81.8608, 25.2298],
            [81.8600, 25.2310]
        ],
        "area_sqm": 15600,
        "centroid": [81.8611, 25.2308]
    },
    ("Lucknow", "Lucknow", "Sample Village", "101"): {
        "coordinates": [
            [80.9462, 26.8467],
            [80.9475, 26.8475],
            [80.9480, 26.8460],
            [80.9468, 26.8455],
            [80.9462, 26.8467]
        ],
        "area_sqm": 9800,
        "centroid": [80.9471, 26.8464]
    }
}

# Cascading dropdown structure
LOCATION_TREE = {
    "Prayagraj": {
        "Koraon": {
            "Koodar": ["30", "31", "45"]
        }
    },
    "Lucknow": {
        "Lucknow": {
            "Sample Village": ["101"]
        }
    }
}


def get_plot_data(district: str, tehsil: str, village: str, plot: str):
    """Return plot data if available, else None"""
    key = (district, tehsil, village, str(plot))
    return SAMPLE_PLOTS.get(key)