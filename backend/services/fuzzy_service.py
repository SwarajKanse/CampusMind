"""
Unified Fuzzy Service combining Mamdani + Sugeno + NeuroFuzzy.
Covers:
- AISC Exp 13: Fuzzy Logic Controller
- AISC Exp 14: Mamdani & Sugeno FIS comparison
- AISC Exp 15: Neuro-Fuzzy (ANFIS) quality evaluation
"""
from fuzzy.mamdani_fis import MamdaniFIS
from fuzzy.sugeno_fis import SugenoFIS
from fuzzy.neurofuzzy import NeuroFuzzyScorer


class FuzzyQualityScorer:
    def __init__(self):
        self.mamdani = MamdaniFIS()
        self.sugeno = SugenoFIS()
        self.neurofuzzy = NeuroFuzzyScorer()

    def score(self, confidence: float, response_length: int, source_count: int) -> dict:
        m = self.mamdani.score(confidence, response_length, source_count)
        s = self.sugeno.score(confidence, response_length, source_count)
        nf = self.neurofuzzy.score(confidence, response_length, source_count)
        combined = round((m + s + nf) / 3.0, 3)
        return {
            "mamdani": m,
            "sugeno": s,
            "neurofuzzy": nf,
            "combined": combined,
        }
