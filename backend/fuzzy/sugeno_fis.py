"""
Sugeno Fuzzy Inference System. AISC Exp 14.
Unlike Mamdani (where output is a fuzzy set), Sugeno output is a crisp linear function of the inputs.
"""
from fuzzy.membership_functions import MembershipFunction as MF


class SugenoFIS:
    def fuzzify_confidence(self, val: float) -> dict:
        return {
            "low": MF.trapezoidal(val, 0, 0, 0.3, 0.5),
            "medium": MF.triangular(val, 0.3, 0.5, 0.7),
            "high": MF.trapezoidal(val, 0.5, 0.7, 1.0, 1.0),
        }

    def fuzzify_sources(self, val: float) -> dict:
        return {
            "few": MF.trapezoidal(val, 0, 0, 1, 3),
            "many": MF.trapezoidal(val, 2, 4, 10, 10),
        }

    def score(self, confidence: float, response_length: int, source_count: int) -> float:
        conf = self.fuzzify_confidence(confidence)
        src = self.fuzzify_sources(float(source_count))
        norm_len = min(response_length / 2000.0, 1.0)
        norm_src = min(source_count / 10.0, 1.0)

        # Sugeno Rules: output is a linear combination of inputs
        # Rule 1: IF conf IS high AND sources IS many THEN z1 = 0.5*conf + 0.3*norm_len + 0.2*norm_src
        z1 = 0.5 * confidence + 0.3 * norm_len + 0.2 * norm_src
        w1 = min(conf["high"], src["many"])

        # Rule 2: IF conf IS medium THEN z2 = 0.4*conf + 0.3*norm_len + 0.1
        z2 = 0.4 * confidence + 0.3 * norm_len + 0.1
        w2 = conf["medium"]

        # Rule 3: IF conf IS low OR sources IS few THEN z3 = 0.2*conf + 0.1
        z3 = 0.2 * confidence + 0.1
        w3 = max(conf["low"], src["few"])

        total_w = w1 + w2 + w3
        if total_w == 0:
            return 0.5
        return round(float((w1 * z1 + w2 * z2 + w3 * z3) / total_w), 3)
