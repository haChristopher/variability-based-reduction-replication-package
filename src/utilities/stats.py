"""
Different helper functions for calculating variability measures.
"""
import numpy as np


def max_spread(b) -> float:
    mb = np.mean(b)
    return np.max([(np.abs(r1-r2) / mb) for r1 in b for r2 in b])


def cv(x: list[float]) -> float:
    return np.std(x) / np.mean(x)


# Preprocessing 
# TODO: Remove crazy outliers which are because of external influence % Georges

def confidence_interval(x: list[float]) -> float:
    return 1.96 * np.std(x) / np.mean(x)