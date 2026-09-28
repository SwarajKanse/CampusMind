"""
Intent Classifier using Multi-Class Perceptron.
AISC Exp 7: Perceptron classification.
AISC Exp 8: Supervised neural network learning.
"""
from ml.perceptron import MultiClassPerceptron
from services.embedding_service import EmbeddingService


class IntentClassifier:
    INTENTS = ["academic", "general", "feedback", "greeting"]

    def __init__(self):
        import numpy as np
        self.np = np
        self.perceptron = MultiClassPerceptron(input_dim=384, num_classes=len(self.INTENTS))
        self._is_trained = False

    def _ensure_trained(self):
        if self._is_trained:
            return
        training_data = {
            "academic": [
                "What is binary search tree?", "Explain neural networks",
                "Define polymorphism in OOP", "How does TCP work?",
                "What are sorting algorithms?", "Explain OSI model",
                "What is machine learning?", "Define encapsulation",
                "How does HTTP work?", "What is a database index?",
                "Explain convolutional neural networks", "What is RAG pipeline?",
            ],
            "general": [
                "What time is the exam?", "Where is the library?",
                "Who is the HOD?", "What are the holidays?",
                "When is the submission deadline?", "Where is room 301?",
                "What is the college fee?", "Campus wifi details",
            ],
            "feedback": [
                "This answer was helpful", "That was wrong",
                "Good answer", "Not useful", "Thanks for helping",
                "Could be better", "Great response", "Incorrect explanation",
            ],
            "greeting": [
                "Hello", "Hi there", "Good morning", "Hey",
                "Hi", "Good evening", "What's up", "Greetings",
            ],
        }

        texts, labels = [], []
        for intent, examples in training_data.items():
            for ex in examples:
                texts.append(ex)
                labels.append(self.INTENTS.index(intent))

        X = self.np.array(EmbeddingService.encode(texts))
        y = self.np.array(labels)
        self.perceptron.train(X, y, epochs=200, lr=0.01)
        self._is_trained = True

    def classify(self, query: str) -> dict:
        self._ensure_trained()
        embedding = self.np.array(EmbeddingService.encode_single(query))
        idx = self.perceptron.predict(embedding)
        proba = self.perceptron.predict_proba(embedding)
        return {
            "intent": self.INTENTS[idx],
            "confidence": round(float(proba[idx]), 3),
            "all_scores": {self.INTENTS[i]: round(float(p), 3) for i, p in enumerate(proba)},
        }


intent_classifier = IntentClassifier()
