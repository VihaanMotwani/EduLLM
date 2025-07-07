# An Introduction to Linear Regression

## What is Linear Regression?
Linear Regression is a fundamental supervised learning algorithm in machine learning. Its primary goal is to model a linear relationship between a dependent variable (what we want to predict) and one or more independent variables (the features). Imagine plotting points on a graph; linear regression finds the straight line that best fits through those points. This line is called the regression line.

## The Formula
The formula for simple linear regression is: Y = β₀ + β₁X + ε
- Y is the dependent variable.
- X is the independent variable.
- β₀ is the intercept of the line (the value of Y when X is 0).
- β₁ is the slope of the line (how much Y changes for a one-unit change in X).
- ε (epsilon) is the random error term.

## Use Case: Predicting House Prices
A classic example is predicting house prices. The independent variable (X) could be the size of the house in square feet, and the dependent variable (Y) would be its price. By training a linear regression model on a dataset of houses, we can find the best-fit line. Then, given a new house's size, we can use our model to predict its price. The scikit-learn library in Python provides an easy-to-use `LinearRegression` class for this purpose.