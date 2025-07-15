# Supervised Learning

## Summary
Supervised learning is a machine learning method that uses labeled data to train a model. The goal is to predict outputs from given inputs.

## Key Concepts
- Labeled datasets
- Training vs testing
- Regression vs classification

## Common Algorithms
- Linear Regression
- Decision Trees
- k-Nearest Neighbors (k-NN)

## Real-World Example
Predicting house prices based on area, number of rooms, and location.

## Python Example
```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
