import pandas as pd

class Node:
    def __init__(self):
        # Class initialization
        self.left = None
        self.right = None
        self.term = False
        self.label = None
        self.feature = None
        self.value = None

    def set_split(self, feature, value, gini, target_before_split, left_split, right_split):
        """Save the node splitting feature and its value"""
        self.feature = feature
        self.value = value
        self.gini = gini
        self.target_before_split = target_before_split
        self.left_split = left_split
        self.right_split = right_split

    def set_term(self, label):
        """Save label if the node is a leaf"""
        self.term = True
        self.label = label

class DecisionTree:
    def __init__(self, minimum=1):
        self.root_node = Node()
        self.minimum = minimum
        self.predictions = None

    # df is series of target
    def _gini_impurity(self, target):
        squares = [int(x) ** 2 for x in target.value_counts()]
        return 1 - (sum(squares) / (target.shape[0])**2)

    # df is dataframe with first column being feature and second being target
    def _weighted_gini(self, value, feature, target):
        # check type of feature values
        data_type = value.dtype

        if data_type == 'int64':
            feature_value = feature.loc[feature == value]
            feature_not_value = feature.loc[feature != value]
        else: # type float64
            feature_value = feature.loc[feature <= value]
            feature_not_value = feature.loc[feature > value]

        # if for some value one of the series is empty
        # it means it does not give us any information
        if feature_value.shape[0] * feature_not_value.shape[0] == 0:
            return 1

        left_target = target.drop(feature_not_value.index)
        right_target = target.drop(feature_value.index)

        x = self._gini_impurity(left_target)
        y = self._gini_impurity(right_target)

        # calculating weighted gini
        return (x * left_target.shape[0] + y * right_target.shape[0]) / target.shape[0]

    
    def _make_split(self, X, y):
        best_split_index = 1
        best_split_value = 0
        best_gini_index = 2


        # Iterate over all features
        for i in range(X.shape[1]):
            # Iterate over all values in feature
            for j in X.iloc[:, i].unique():

                temp_gini = self._weighted_gini(j, X.iloc[:, i], y)


                if temp_gini < best_gini_index:

                    best_gini_index = temp_gini
                    best_split_value = j
                    best_split_index = i

        return [best_gini_index, X.columns[best_split_index], best_split_value]

    def _recursive_splitting(self, node, X, y):
        if y.shape[0] <= self.minimum or self._gini_impurity(y) == 0:
            label = y.value_counts().idxmax()
            node.set_term(label)
        else:
            gini, feature, value = self._make_split(X, y)
            feature_data = X.loc[:, feature]

            data_type = feature_data.dtype
            if data_type == 'int64':
                left_y = y.loc[feature_data == value]
                right_y = y.loc[feature_data != value]
            else:
                left_y = y.loc[feature_data <= value]
                right_y = y.loc[feature_data > value]

            node.set_split(feature, value, gini, y, left_y, right_y)

            node.left = Node()
            node.right = Node()

            left_X = X.drop(right_y.index)
            right_X = X.drop(left_y.index)

            self._recursive_splitting(node.left, left_X, left_y)
            self._recursive_splitting(node.right, right_X, right_y)

    def fit(self, X, y):
        self._recursive_splitting(self.root_node, X, y)

    def _internal_predicting_method(self, node, sample):
        if node.term:
            return node.label
        else:
            if isinstance(sample, int):
                if sample[node.feature] == node.value:
                    return self._internal_predicting_method(node.left, sample)
                else:
                    return self._internal_predicting_method(node.right, sample)
            else:
                if sample[node.feature] <= node.value:
                    return self._internal_predicting_method(node.left, sample)
                else:
                    return self._internal_predicting_method(node.right, sample)

    def predict(self, X):
        self.predictions = []
        for i in X.index:
            prediction = self._internal_predicting_method(self.root_node, X.loc[i, :])
            self.predictions.append(prediction)
        return pd.Series(self.predictions)


# Load the dataset
data_paths = input()
training_data, test_data = data_paths.split()

training_data = pd.read_csv(training_data, index_col=0)
test_data = pd.read_csv(test_data, index_col=0)

X_train = training_data.drop("Survived", axis=1)
y_train = training_data.iloc[:, -1]

X_test = test_data.drop("Survived", axis=1)
y_test = test_data.iloc[:, -1]

# Fit the decision tree
dec = DecisionTree(74)  # 74
dec.fit(X_train, y_train)

y_pred = dec.predict(X_test)

cm = pd.crosstab(y_test, y_pred, rownames=['Actual'], colnames=['Predicted'])

print(cm)

#print(round(cm.iloc[1,1]/ (cm.iloc[1,1] + cm.iloc[1,0]), 3), round(cm.iloc[0,0]/ (cm.iloc[0,0] + cm.iloc[0,1]) ,3))
