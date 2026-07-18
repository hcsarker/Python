"""
Explainable AI example: export decision rules from a trained DecisionTreeClassifier.
Matches the PDF's export_text demonstration.
"""
from __future__ import annotations
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, export_text


def export_rules() -> str:
    data = load_iris()
    model = DecisionTreeClassifier(random_state=42).fit(data.data, data.target)
    tree_rules = export_text(model, feature_names=data.feature_names)
    return tree_rules


if __name__ == "__main__":
    print(export_rules())
