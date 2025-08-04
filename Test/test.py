import sys
print("Python version:", sys.version)

# ✅ NumPy Test
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
print("NumPy Array:", arr)
print("NumPy Mean:", np.mean(arr))

# ✅ Pandas Test
import pandas as pd
data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35]}
df = pd.DataFrame(data)
print("Pandas DataFrame:\n", df)


# ✅ SciPy Test
from scipy import stats
data = [2, 4, 4, 4, 5, 5, 7, 9]
print("SciPy Mode:", stats.mode(data, keepdims=True))

# ✅ Matplotlib Test
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [1, 4, 9], label="y = x^2")
plt.title("Matplotlib Test")
plt.legend()
plt.savefig("matplotlib_test.png")  # Save plot as image
print("Matplotlib plot saved as matplotlib_test.png")

# ✅ Scikit-learn Test
from sklearn.linear_model import LinearRegression
model = LinearRegression()
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([1, 4, 9, 16, 25])
model.fit(X, y)
prediction = model.predict([[6]])
print("Scikit-learn Prediction for x=6:", prediction)

# ✅ BeautifulSoup Test
from bs4 import BeautifulSoup
html = "<html><body><h1>Hello World</h1></body></html>"
soup = BeautifulSoup(html, "html.parser")
print("BeautifulSoup Extracted Text:", soup.h1.text)

print("\n✅ All tests completed successfully!")
