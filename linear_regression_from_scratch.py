import numpy as np

class CustomLinearRegression:
    def __init__(self, *, fit_intercept=True):
        self.fit_intercept = fit_intercept
        self.coefficient = None
        self.intercept = 0

    def fit(self, X, y):
        if self.fit_intercept:
            X = np.c_[np.ones(X.shape[0]), X]  # insert a column of ones at the beginning
            cof = np.linalg.inv(X.T @ X) @ X.T @ y
            self.coefficient = cof[1:]
            self.intercept = cof[0]
        else:
            cof = np.linalg.inv(X.T @ X) @ X.T @ y
            self.coefficient = cof

    def predict(self, X):
        if self.fit_intercept:
            X = np.c_[np.ones(X.shape[0]), X]  # insert a column of ones at the beginning
            return X @ np.insert(self.coefficient, 0, self.intercept)
        return X * self.coefficient

    def r2_score(self, y, yhat):
        return 1 - sum((y - yhat) ** 2) / sum((y - y.mean()) ** 2)

    def rmse(self, y, yhat):
        return (sum((y - yhat) ** 2) / len(y)) ** 0.5

capacity = [0.9, 0.5, 1.75, 2.0, 1.4, 1.5, 3.0, 1.1, 2.6, 1.9]
age = [11, 11, 9, 8, 7, 7, 6, 5, 5, 4]
cost_per_ton = [21.95, 27.18, 16.9, 15.37, 16.03, 18.15, 14.22, 18.72, 15.4, 14.69]
X = np.c_[np.array(capacity), np.array(age)]

y = np.array(cost_per_ton)

reg = CustomLinearRegression(fit_intercept=True)
reg.fit(X,y)
predictions = reg.predict(X)


dict = {'Intercept': reg.intercept,
 'Coefficient': reg.coefficient,
 'R2': reg.r2_score(y, predictions),
 'RMSE': reg.rmse(y ,predictions)}

print(dict)
