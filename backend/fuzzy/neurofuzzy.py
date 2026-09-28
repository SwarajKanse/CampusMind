"""
ANFIS-style Hybrid Neuro-Fuzzy System. AISC Exp 15.
Combines neural network gradient-based parameter learning with fuzzy inference rules.
"""
import numpy as np


class ANFISLayer:
    def __init__(self, n_inputs: int = 3, n_rules: int = 4):
        self.n_inputs = n_inputs
        self.n_rules = n_rules
        self.means = np.random.randn(n_rules, n_inputs) * 0.3 + 0.5
        self.sigmas = np.abs(np.random.randn(n_rules, n_inputs) * 0.2) + 0.15
        self.consequent = np.random.randn(n_rules, n_inputs + 1) * 0.1
        self.lr = 0.01

    def gaussian_mf(self, x: float, mean: float, sigma: float) -> float:
        return float(np.exp(-0.5 * ((x - mean) / max(sigma, 1e-6)) ** 2))

    def forward(self, x: np.ndarray) -> float:
        mu = np.zeros((self.n_rules, self.n_inputs))
        for i in range(self.n_rules):
            for j in range(self.n_inputs):
                mu[i, j] = self.gaussian_mf(float(x[j]), float(self.means[i, j]), float(self.sigmas[i, j]))
        w = np.prod(mu, axis=1)
        w_sum = np.sum(w) + 1e-10
        w_norm = w / w_sum
        x_aug = np.append(x, 1.0)
        rule_outputs = self.consequent @ x_aug
        output = np.sum(w_norm * rule_outputs)
        return float(np.clip(output, 0.0, 1.0))

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 100):
        for epoch in range(epochs):
            for xi, yi in zip(X, y):
                pred = self.forward(xi)
                error = yi - pred
                x_aug = np.append(xi, 1.0)
                for r in range(self.n_rules):
                    self.consequent[r] += self.lr * error * x_aug * 0.25


class NeuroFuzzyScorer:
    def __init__(self):
        self.anfis = ANFISLayer(n_inputs=3, n_rules=4)
        self._pretrain()

    def _pretrain(self):
        np.random.seed(42)
        X = np.random.rand(300, 3)
        y = 0.5 * X[:, 0] + 0.2 * np.clip(X[:, 1], 0.2, 0.8) + 0.3 * X[:, 2]
        y = np.clip(y + np.random.randn(300) * 0.03, 0.0, 1.0)
        self.anfis.train(X, y, epochs=100)

    def score(self, confidence: float, response_length: int, source_count: int) -> float:
        x = np.array([confidence, min(response_length / 2000.0, 1.0), min(source_count / 10.0, 1.0)])
        return round(self.anfis.forward(x), 3)
