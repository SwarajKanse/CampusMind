"""
Fuzzy membership functions.
AISC Exp 13: Fuzzy Logic Controller.
"""
import numpy as np


class MembershipFunction:
    @staticmethod
    def triangular(x: float, a: float, b: float, c: float) -> float:
        if x <= a or x >= c:
            return 0.0
        elif x <= b:
            return (x - a) / (b - a) if b != a else 1.0
        else:
            return (c - x) / (c - b) if c != b else 1.0

    @staticmethod
    def trapezoidal(x: float, a: float, b: float, c: float, d: float) -> float:
        if x <= a or x >= d:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a) if b != a else 1.0
        elif b < x <= c:
            return 1.0
        else:
            return (d - x) / (d - c) if d != c else 1.0

    @staticmethod
    def gaussian(x: float, mean: float, sigma: float) -> float:
        return float(np.exp(-0.5 * ((x - mean) / max(sigma, 1e-6)) ** 2))
