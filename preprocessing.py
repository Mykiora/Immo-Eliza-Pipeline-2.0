import pandas as pd
import numpy as np
import json
from scipy.stats import zscore
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_selector, make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
from xgboost import XGBRegressor


def check_missing_values(column: pd.Series) -> float:
    """
    Calculates the percentage of missing values in a given column.

    Parameters :
    - df  : The DataFrame the function will work with.
    - column : The column in which the percentage must be calculated.

    Returns:
    - Float number between 0 and 100
    """
    total_values = column.size
    missing_values = column.isna().sum()
    return round((missing_values / total_values) * 100, 2)


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
pipe = make_pipeline(preprocessor, XGBRegressor())

# cross-validation
print(cross_val_score(pipe, X_train, y_train).mean())
