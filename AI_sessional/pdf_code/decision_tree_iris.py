"""
Decision Tree on Iris dataset, matching the PDF example.
"""
from __future__ import annotations
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris


def train_and_score() -> float:
    data = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.25, random_state=42
    )
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model.score(X_test, y_test)


if __name__ == "__main__":
    acc = train_and_score()
    print("Accuracy:", acc)
