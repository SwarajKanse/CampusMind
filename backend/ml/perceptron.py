"""
Multi-class and Binary Perceptron implementations.
AISC Exp 7: Perceptron for logic operations (AND/OR) & multi-class intent classification.
AISC Exp 8: Supervised neural network learning.
"""
import numpy as np


class BinaryPerceptron:
    """Binary Perceptron with step activation. Covers AISC Exp 7 logic gates."""
    def __init__(self, input_dim: int, lr: float = 0.1, epochs: int = 50):
        self.lr = lr
        self.epochs = epochs
        self.weights = np.zeros(input_dim)
        self.bias = 0.0

    def activation(self, z: float) -> int:
        return 1 if z >= 0 else 0

    def predict(self, x: np.ndarray) -> int:
        z = np.dot(self.weights, x) + self.bias
        return self.activation(z)

    def train(self, X: np.ndarray, y: np.ndarray) -> list[int]:
        errors_per_epoch = []
        for _ in range(self.epochs):
            total_errors = 0
            for xi, target in zip(X, y):
                pred = self.predict(xi)
                err = target - pred
                if err != 0:
                    self.weights += self.lr * err * xi
                    self.bias += self.lr * err
                    total_errors += 1
            errors_per_epoch.append(total_errors)
            if total_errors == 0:
                break
        return errors_per_epoch


class MultiClassPerceptron:
    """Multi-class Perceptron with Softmax confidence. Covers AISC Exp 7 & 8."""
    def __init__(self, input_dim: int, num_classes: int):
        self.weights = np.random.randn(num_classes, input_dim) * 0.01
        self.bias = np.zeros(num_classes)

    def predict(self, x: np.ndarray) -> int:
        scores = self.weights @ x + self.bias
        return int(np.argmax(scores))

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        scores = self.weights @ x + self.bias
        exp_scores = np.exp(scores - np.max(scores))
        return exp_scores / exp_scores.sum()

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 150, lr: float = 0.01):
        for _ in range(epochs):
            for xi, yi in zip(X, y):
                pred = self.predict(xi)
                if pred != yi:
                    self.weights[yi] += lr * xi
                    self.bias[yi] += lr
                    self.weights[pred] -= lr * xi
                    self.bias[pred] -= lr
