# Immo-Eliza-Pipeline-2.0

## Description
Immo-Eliza is a regression project that we had to do in the bootcamp. Provided with real estate data from Immoweb.be, 
the goal was to build a Machine Learning model able to predict the prices of the properties. This project is an attempt
to improve the preprocessing quality and the model performance by including a pipeline and using scikit-learn transformers.

## Installation
1. Make sure you have the latest version of Python installed
2. If you are on Windows, you can just launch "start.bat". Otherwise, you can `cd` your way to the directory and run the command `pip install -r requirements.txt`, then start the program locally with `streamlit run interface.py`
3. That's all. You can now test the model.

## Pre-Pipeline
Before even entering the pipeline and going through the series of transformers, the initial modifications made on the data are
the following :
1. Drop the duplicates
2. Remove the columns we are not interested in for modeling, such as ID's and URL's
3. Handle outliers using zscore with a threshold of 3
4. Split the data into a target and features.

## Pipeline
Two different pipelines are used : one for categorical features and the other one for numeric features.

The categorical features' pipeline :
- Imputes the missing values with the mode
- Applies one hot encoding

The numeric features' pipeline :
- Imputes the missing values with the median
- Standardizes the data

The model has been tuned with GridSearchCV and is then evaluated using 10-fold cross validation.

R² Score : 0.7796745321037716

## What I've learned with this project
- Make use of make_column_selector to automatically select columns depending on its DataType.
- Make use of column_transformer to apply different preprocessing steps on different columns.
- The power of a preprocessing pipeline and how to implement a neat one.
- Perform cross validation directly on the pipeline.
- When trying to fine tune the parameters of a model lying inside a pipeline, it is necessary to define the parameter as part of the Regressor. For example, instead of writing "learning_rate:" in the parameters dict, write "xgbregressor__learning_rate:".
- Create a simple interface with Streamlit
- In case of getting the error message "ValueError: If using all scalar values, you must pass an index" when creating a dataframe, pass the argument "index=[0]"