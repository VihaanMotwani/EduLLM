# Introduction to Linear Regression

## Summary
Linear Regression is a fundamental **supervised learning** algorithm used for predicting continuous numeric values. It models the relationship between a **dependent variable** (target) and one or more **independent variables** (features) by fitting a straight line through the data points.

This “best-fit” line allows us to make predictions based on patterns the model has learned.

---

## Key Concepts

- **Linear relationship:** The assumption that changes in input (X) cause proportional changes in output (Y).
- **Regression line:** The line of best fit that minimizes error between predicted and actual values.
- **Dependent variable (Y):** The value to predict.
- **Independent variable (X):** The input feature(s) used for prediction.
- **Least Squares:** A method to find the best-fit line by minimizing the sum of squared errors.

---

## Mathematical Formula

\[
Y = \beta_0 + \beta_1 X + \epsilon
\]

- \( Y \): Dependent variable (predicted output)  
- \( X \): Independent variable (input feature)  
- \( \beta_0 \): Intercept (value of Y when X = 0)  
- \( \beta_1 \): Slope (how much Y changes for a one-unit increase in X)  
- \( \epsilon \): Error term (accounts for noise in the data)

---

## Real-World Example

A common use case is **predicting house prices**.  
Suppose you have data on house size (in square feet) and sale prices. Linear regression finds the best-fit line through the data points so you can predict a house's price based on its size.

---

## Advantages

- Simple to understand and implement
- Works well with linearly related data
- Fast to train and interpret

---

## FAQs

- **Q:** What is the difference between simple and multiple linear regression?  
  **A:** Simple linear regression uses one input feature; multiple linear regression uses two or more.

- **Q:** Can linear regression be used for classification tasks?  
  **A:** No. It’s for predicting continuous values. Use **logistic regression** or classifiers for classification problems.

- **Q:** What are the main limitations of linear regression?  
  **A:** It assumes a linear relationship, is sensitive to outliers, and may underperform on non-linear or complex datasets.

- **Q:** How does the model determine the best-fit line?  
  **A:** By minimizing the sum of squared errors between predicted and actual values (the **least squares method**).

- **Q:** What if the relationship between variables is not linear?  
  **A:** Consider using **polynomial regression**, **decision trees**, or other non-linear models.

---

## Tags
#LinearRegression #SupervisedLearning #Regression #ML #Beginner
