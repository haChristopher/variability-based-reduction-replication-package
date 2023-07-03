"""
Helper to read out measurement data from sqlite database
"""

import sqlite3

def get_all_measurements(db_path: str, start_form_count: int) -> list[any]:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    query = "SELECT * FROM measurement"

    if start_form_count > 0:
        query = query + " WHERE count_idx >= " + str(start_form_count)

    query = query + ";"
    res = c.execute(query)
    measurements = c.fetchall()
    conn.close()
    return measurements

def get_all_benchmarks(db_path: str) -> list[any]:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    query = "SELECT * FROM benchmark;"
    c.execute(query)
    benchmarks = c.fetchall()
    conn.close()
    return benchmarks


def group_measurements_by_property(measurements: list[tuple], group_by_idx: int) -> dict[str, list[any]]:
    grouped = {}
    for entry in measurements:
        bench_name = entry[group_by_idx]
        if bench_name not in grouped:
            grouped[bench_name] = []
        grouped[bench_name].append(entry)
    return grouped