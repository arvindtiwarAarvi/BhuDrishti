"""
AASIA — Automated Assistance for Spatial & Integrity Analysis
Simple page/result summarizer for BhuDrishti portal.
"""

def summarize_page(page_name: str) -> str:
    guides = {
        "Home": (
            "BhuDrishti ek digital land intelligence portal hai. "
            "Yahan aap plot verify kar sakte ho, satellite view dekh sakte ho, "
            "fertility/water insights le sakte ho, aur blockchain se authenticity check kar sakte ho. "
            "Upar se apna role choose karein: Lekhpal, Farmer, Citizen, Real Estate ya Officer."
        ),
        "Lekhpal": (
            "Lekhpal desk par aap District–Tehsil–Village–Plot daal kar "
            "satellite map, plot boundary aur har corner ka Lat-Long nikal sakte ho. "
            "Yeh boundary verification aur field work ke liye useful hai."
        ),
        "Farmers": (
            "Farmer desk fertility (Upjau), water resource hints aur simple land summary deta hai. "
            "Yeh official soil lab certificate nahi hai — guidance ke liye hai."
        ),
        "Real Estate": (
            "Real Estate desk plot area, location summary aur blockchain authenticity check "
            "mein madad karta hai — purchase se pehle basic verification ke liye."
        ),
        "Citizen": (
            "Citizen desk simple plot check + Lock/Verify flow deta hai. "
            "Aap record lock kar sakte ho aur baad mein AUTHENTIC/TAMPERED dekh sakte ho."
        ),
        "Gov Officer": (
            "Officer desk ledger overview, locked records count aur verification support "
            "ke liye hai — transparency aur audit trail ke saath."
        ),
        "Feedback": (
            "Feedback page par aap sujhav ya shikayat bhej sakte ho. "
            "Team isse portal improve karne ke liye use karegi."
        ),
        "Related Portals": (
            "Yahan official related links hain jaise Bhulekh, Bhunaksha, Jansunwai — "
            "taaki aap seedha sarkari portals pe ja saken."
        ),
        "About": (
            "About page par BhuDrishti ka mission, PS-28 connection aur team information hai."
        ),
        "Database": (
            "Database/Ledger page locked plot records dikhata hai — hash, time aur plot key ke saath."
        ),
        "Dashboard": (
            "Dashboard par aapki basic profile, recent activity aur quick links milte hain."
        ),
    }
    return guides.get(page_name, "AASIA: Is page par available options use karein. Help chahiye to role-wise desk choose karein.")


def summarize_result(kind: str, data: dict | None = None) -> str:
    data = data or {}
    if kind == "analyze":
        area = data.get("area", "-")
        village = data.get("village", "")
        plot = data.get("plot_no", "")
        return (
            f"AASIA summary: Plot {plot} ({village}) analyze ho gaya. "
            f"Area lagbhag {area} sq.m hai. Map par red boundary corners dikhani chahiye. "
            f"Neeche fertility, water aur AI report check karein."
        )
    if kind == "lock":
        idx = data.get("index", "-")
        return (
            f"AASIA summary: Record ledger pe lock ho gaya (Block #{idx}). "
            f"Ab same data se Verify AUTHENTIC aana chahiye. Data change hua to TAMPERED dikhega."
        )
    if kind == "verify":
        status = data.get("status", "")
        if data.get("authentic"):
            return "AASIA summary: Verification successful — record AUTHENTIC hai. Hash match ho gaya."
        return f"AASIA summary: Status {status}. Hash match nahi hua ya record nahi mila — data check karein."
    return "AASIA: Result ready. Details panels mein dekhein."
