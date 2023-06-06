"""
Helper to read out measurement data from sqlite database
"""

import sqlite3

def get_all_measurements(db_path: str) -> list[any]:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    res = c.execute("SELECT * FROM measurement;")
    measurements = c.fetchall()
    conn.close()
    return measurements


def group_measurements_by_name(measurements: list[tuple], group_by_idx: int) -> dict[str, list[any]]:
    grouped = {}
    for entry in measurements:
        bench_name = entry[group_by_idx]
        if bench_name not in grouped:
            grouped[bench_name] = []
        grouped[bench_name].append(entry)
    return grouped