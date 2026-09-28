"""
Mamdani Fuzzy Inference System for response quality scoring.
AISC Exp 13: Fuzzy Logic Controller
AISC Exp 14: Mamdani FIS implementation

Inputs: confidence (0-1), response_length (0-2000), source_count (0-10)
Output: quality_score (0-1)
"""
import numpy as np
from fuzzy.membership_functions import MembershipFunction as MF


class MamdaniFIS:
    def fuzzify_confidence(self, val: float) -> dict:
        return {
            "low": MF.trapezoidal(val, 0, 0, 0.3, 0.5),
            "medium": MF.triangular(val, 0.3, 0.5, 0.7),
            "high": MF.trapezoidal(val, 0.5, 0.7, 1.0, 1.0),
        }

    def fuzzify_length(self, val: float) -> dict:
        return {
            "short": MF.trapezoidal(val, 0, 0, 50, 200),
            "medium": MF.triangular(val, 100, 500, 1000),
            "long": MF.trapezoidal(val, 800, 1200, 2000, 2000),
        }

    def fuzzify_sources(self, val: float) -> dict:
        return {
            "few": MF.trapezoidal(val, 0, 0, 1, 2),
            "some": MF.triangular(val, 1, 3, 5),
            "many": MF.trapezoidal(val, 3, 5, 10, 10),
        }

    def evaluate_rules(self, conf: dict, length: dict, sources: dict) -> dict:
        return {
            "excellent": max(
                min(conf["high"], sources["many"]),
                min(conf["high"], length["long"])
            ),
            "good": min(conf["medium"], sources["some"]),
            "poor": max(
                max(conf["low"], sources["few"]),
                length["short"]
            ),
        }

    def defuzzify(self, output: dict) -> float:
        x = np.linspace(0, 1, 100)
        aggregated = np.zeros_like(x)
        for i, xi in enumerate(x):
            poor = min(output["poor"], MF.trapezoidal(xi, 0, 0, 0.2, 0.4))
            good = min(output["good"], MF.triangular(xi, 0.3, 0.5, 0.7))
            excellent = min(output["excellent"], MF.trapezoidal(xi, 0.6, 0.8, 1.0, 1.0))
            aggregated[i] = max(poor, good, excellent)
        total = np.sum(aggregated)
        if total == 0:
            return 0.5
        return float(np.sum(x * aggregated) / total)

    def score(self, confidence: float, response_length: int, source_count: int) -> float:
        conf = self.fuzzify_confidence(confidence)
        length = self.fuzzify_length(float(response_length))
        sources = self.fuzzify_sources(float(source_count))
        output = self.evaluate_rules(conf, length, sources)
        return round(self.defuzzify(output), 3)
