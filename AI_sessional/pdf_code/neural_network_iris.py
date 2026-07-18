"""
Neural Network (MLPClassifier) on Iris dataset, per the PDF example.
"""
from __future__ import annotations
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris


def train_and_score() -> float:
    data = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.25, random_state=42
    )
    model = MLPClassifier(hidden_layer_sizes=(5,), max_iter=500, random_state=42)
    model.fit(X_train, y_train)
    return model.score(X_test, y_test)


if __name__ == "__main__":
    acc = train_and_score()
    print("Accuracy:", acc)
