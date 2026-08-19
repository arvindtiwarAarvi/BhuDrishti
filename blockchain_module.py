"""
BhuDrishti — Blockchain-style Land Record Integrity Module
PS-28: Blockchain-Based Land Record Verification

Demo mode: local append-only ledger (JSON) + SHA-256
Later: same hash can be anchored on Polygon/Sepolia testnet
"""

import json
import hashlib
import os
from datetime import datetime, timezone

LEDGER_FILE = "bhu_ledger.json"


def build_canonical_record(district, tehsil, village, plot_no, coords, area_sqm, report_summary):
    """
    Stable JSON structure for hashing.
    Keys sorted so same data = same hash always.
    """
    record = {
        "district": str(district).strip(),
        "tehsil": str(tehsil).strip(),
        "village": str(village).strip(),
        "plot_no": str(plot_no).strip(),
        "coordinates": coords,          # list of [lon, lat]
        "area_sqm": round(float(area_sqm), 2),
        "report_summary": str(report_summary).strip(),
    }
    # canonical string (sorted keys)
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    return record, canonical


def compute_hash(canonical_string: str) -> str:
    """SHA-256 fingerprint of the land record."""
    return hashlib.sha256(canonical_string.encode("utf-8")).hexdigest()


def _load_ledger():
    if not os.path.exists(LEDGER_FILE):
        return []
    with open(LEDGER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_ledger(entries):
    with open(LEDGER_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def lock_on_chain(district, tehsil, village, plot_no, coords, area_sqm, report_summary):
    """
    Create hash and append to local ledger (demo blockchain).
    Returns entry with hash + timestamp.
    """
    record, canonical = build_canonical_record(
        district, tehsil, village, plot_no, coords, area_sqm, report_summary
    )
    record_hash = compute_hash(canonical)

    entry = {
        "index": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "plot_key": f"{district}|{tehsil}|{village}|{plot_no}",
        "record": record,
        "hash": record_hash,
        "prev_hash": None,
    }

    ledger = _load_ledger()
    entry["index"] = len(ledger)
    entry["prev_hash"] = ledger[-1]["hash"] if ledger else "0" * 64
    # block hash includes prev (chain link)
    block_payload = json.dumps(
        {"prev_hash": entry["prev_hash"], "hash": record_hash, "index": entry["index"]},
        sort_keys=True,
        separators=(",", ":"),
    )
    entry["block_hash"] = compute_hash(block_payload)

    ledger.append(entry)
    _save_ledger(ledger)

    return {
        "status": "LOCKED",
        "index": entry["index"],
        "hash": record_hash,
        "block_hash": entry["block_hash"],
        "timestamp": entry["timestamp"],
        "plot_key": entry["plot_key"],
        "message": "Record locked on BhuDrishti ledger (demo chain)",
    }


def verify_record(district, tehsil, village, plot_no, coords, area_sqm, report_summary):
    """
    Recompute hash and check against ledger.
    """
    record, canonical = build_canonical_record(
        district, tehsil, village, plot_no, coords, area_sqm, report_summary
    )
    current_hash = compute_hash(canonical)
    plot_key = f"{district}|{tehsil}|{village}|{plot_no}"

    ledger = _load_ledger()
    matches = [e for e in ledger if e.get("plot_key") == plot_key]

    if not matches:
        return {
            "status": "NOT_FOUND",
            "authentic": False,
            "current_hash": current_hash,
            "message": "No locked record found for this plot",
        }

    latest = matches[-1]
    stored_hash = latest["hash"]
    authentic = stored_hash == current_hash

    return {
        "status": "AUTHENTIC" if authentic else "TAMPERED",
        "authentic": authentic,
        "current_hash": current_hash,
        "stored_hash": stored_hash,
        "locked_at": latest["timestamp"],
        "block_index": latest["index"],
        "message": (
            "Record matches blockchain lock — authentic"
            if authentic
            else "Hash mismatch — data may have been changed after lock"
        ),
    }


def get_ledger_summary():
    ledger = _load_ledger()
    return {
        "total_blocks": len(ledger),
        "entries": [
            {
                "index": e["index"],
                "plot_key": e["plot_key"],
                "hash": e["hash"][:16] + "...",
                "time": e["timestamp"],
            }
            for e in ledger
        ],
    }


# ----- Test -----
if __name__ == "__main__":
    from extract import get_plot_coordinates
    from geo_utils import create_geodataframe, get_area_sqm
    from fertility_water import estimate_fertility, detect_water_resources
    from ai_report import generate_ai_report

    district, tehsil, village, plot_no = "Prayagraj", "Koraon", "Koodar", "30"
    coords = get_plot_coordinates(district, tehsil, village, plot_no)
    gdf = create_geodataframe(coords, plot_no)
    area = get_area_sqm(gdf)
    fert = estimate_fertility(coords)
    water = detect_water_resources(coords)
    report = generate_ai_report(plot_no, fert, water)
    summary = report.get("summary", "") if isinstance(report, dict) else str(report)

    print("=== LOCK ===")
    locked = lock_on_chain(district, tehsil, village, plot_no, coords, area, summary)
    print(json.dumps(locked, indent=2))

    print("\n=== VERIFY (same data) ===")
    verified = verify_record(district, tehsil, village, plot_no, coords, area, summary)
    print(json.dumps(verified, indent=2))

    print("\n=== LEDGER ===")
    print(json.dumps(get_ledger_summary(), indent=2))