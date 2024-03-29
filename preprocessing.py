import pandas as pd
import numpy as np
import json
import pickle
from scipy.stats import zscore
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_selector, make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
from xgboost import XGBRegressor


def predict(property_data: dict):
    """
    Imports the model from a pickle file and make a prediction based on the given features.

    Parameters :
    - property_data : A dict containing the data about the property.

    Format : ['Openfire' 'Furnished' 'Terrace' 'Garden' 'TypeOfProperty' 'PostalCode'
            'SubtypeOfProperty' 'TypeOfSale' 'Kitchen' 'StateOfBuilding' 'Heating'
            'Bedrooms' 'SurfaceOfGood' 'SwimmingPool' 'NumberOfFacades' 'LivingArea'
            'ConstructionYear' 'GardenArea']

    Returns :
    - Predicted price (float number)
    """
    # Import model
    with open("utils/pipeline.obj", "rb") as file:
        pipeline = pickle.load(file)

    features = pd.DataFrame(property_data, index=[0])

    return int(round(pipeline.predict(features)[0], -4))


def remove_outliers_zscore(df, columns, threshold=3):
    """
    Remove outliers from the specified columns of a DataFrame using z-score method.

    Parameters:
    - df: DataFrame containing the data
    - columns: List of column names to remove outliers from
    - threshold: Threshold value for z-score. Data points with z-score greater than
                 this threshold will be considered as outliers. Default is 3.

    Returns:
    - DataFrame: DataFrame with outliers removed
    """
    df_out = df.copy()
    for column in columns:
        z_scores = zscore(df_out[column])
        abs_z_scores = abs(z_scores)
        filtered_entries = abs_z_scores < threshold
        df_out = df_out[filtered_entries]
    return df_out


# read dataset
with open("data/train.json") as file:
    data = json.load(file)
    train = pd.DataFrame.from_dict(data)

with open("data/test.json") as file:
    data = json.load(file)
    test = pd.DataFrame.from_dict(data)

# drop duplicates
train = train.drop_duplicates()
test = test.drop_duplicates()

# remove useless columns
train = train.drop(columns=["Url", "PropertyId"])
test = test.drop(columns=["Url", "PropertyId"])

# handle outliers
train = remove_outliers_zscore(train, ["Price"])
test = remove_outliers_zscore(test, ["Price"])

train = train[train["Price"] > 0]
test = test[test["Price"] > 0]

# split features and target
X_train, y_train = train.drop("Price", axis=1), train["Price"]
X_test, y_test = test.drop("Price", axis=1), test["Price"]

# numeric columns
num_imp = SimpleImputer(strategy="median", add_indicator=True)
scaler = StandardScaler()

# categorical columns
cat_imp = SimpleImputer(strategy="most_frequent", add_indicator=True)
ohe = OneHotEncoder(handle_unknown="ignore", drop="first", sparse_output=False)

# select column by dtype
num_cols = make_column_selector(dtype_include="number")
cat_cols = make_column_selector(dtype_exclude="number")

# preprocessing object
preprocessor = make_column_transformer(
    (make_pipeline(num_imp, scaler), num_cols), (make_pipeline(cat_imp, ohe), cat_cols)
)

# pipeline
pipe = make_pipeline(
    preprocessor,
    XGBRegressor(
        colsample_bytree=0.7,
        learning_rate=0.03,
        max_depth=10,
        min_child_weight=4,
        n_estimators=1000,
        objective="reg:squarederror",
        subsample=0.7,
        random_state=42,
    ),
)

# cross-validation
# print(cross_val_score(pipe, X_train, y_train, cv=10, scoring="r2").mean())

# Optional : if the tests are done, uncomment the next three lines to save the final model
"""pipe.fit(X_train, y_train)
with open("utils/pipeline.obj", "wb") as file:
    pickle.dump(pipe, file)"""
