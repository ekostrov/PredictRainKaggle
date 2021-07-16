# Imports
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
# machine learning
from sklearn.ensemble import RandomForestClassifier
#from xgboost import XGBClassifier
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report
from sklearn.metrics import roc_auc_score, accuracy_score, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
import warnings # suppress warnings
# End of Imports

class CustomScaler(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()
        self.num_cols_ = None
        self.scaler_ = None
        
    def fit(self, X, y=None):
        self.num_cols_ =[column for column in X.columns if X[column].dtype == 'float64']
        self.scaler = StandardScaler()
        self.scaler.fit(X[self.num_cols_])

        return self
    
    def transform(self, X, y=None):
        X[self.num_cols_] = self.scaler.transform(X[self.num_cols_]) # fit and transform the data
        
        return X

class CustomImputer(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()
        self.loc_month_medians_ = {}
        self.month_medians_ = {}
        self.num_cols_ = None
        self.str_cols_ = None
        
    def fit(self, X, y=None):
        self.num_cols_ = [column for column in X.columns if X[column].dtype == 'float64']
        self.str_cols_ = [column for column in X.columns if X[column].dtype == 'object']
        self.loc_month_medians_ = X.groupby(['Location','Month']).median()
        self.month_medians_ = X.groupby(['Month']).median()
        return self
    
    def transform(self, X, y=None):
        print("Transforming Data Set")
        for location in X.Location.unique():
            for month in X.Month.unique():
                for column in self.num_cols_:
                    median_for_month = self.loc_month_medians_.loc[(location,month)][column]
                    if np.isnan(median_for_month):
                        median_for_month = self.month_medians_.loc[month][column]
                    idx = list(X[(X.Location == location) & (X.Month == month) & (X[column].isna())].index)
                    X.loc[idx,column] = median_for_month
        
        return X

class CustomCreateMonth(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        super().__init__()
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X['Month'] = X.Date.apply(lambda x : int(x.split('-')[1]))
        X = X.drop('Date', axis=1)
        
        return X

class CustomCategoryImputer(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()
        self.str_cols_ = None
    
    def fit(self, X, y=None):
        self.str_cols_ = [column for column in X.columns if X[column].dtype == 'object']
        return self
    
    def transform(self, X, y=None):
        for column in self.str_cols_:
            idx = X[X[column].isna()].index
            X.loc[idx,column] ='MIA'
        return X

class CustomCategoryEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()
        self.enc_ = None
        self.str_cols_ = None
        self.num_cols_ = None
    
    def impute(self, X_str):
        imputer = CustomCategoryImputer()
        imputer.fit(X_str)
        X_str = imputer.transform(X_str)
        return X_str
    
    def fit(self, X, y=None):
        self.num_cols_ = [column for column in X.columns if X[column].dtype == 'float64']
        self.str_cols_ = [column for column in X.columns if X[column].dtype == 'object']
        self.enc_ = OneHotEncoder(handle_unknown='ignore', sparse=False)
        self.enc_.fit(X[self.str_cols_])
        
        return self
    
    def transform(self, X, y=None):
        X_str = X[list(self.str_cols_)]
        X_num = X[list(self.num_cols_)]
        X_str = self.enc_.transform(X_str)
        column_names = self.enc_.get_feature_names(self.str_cols_)
        for i, col in enumerate(column_names):
            X_num[col] = X_str[:,i]
        
        X = X_num
        return X

class CustomFixLocation(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()
        self.lb_ = None
    
    def fit(self, X, y=None):
        self.lb_ = LabelEncoder()
        self.lb_.fit(X['Location'])
        
        return self
    
    def transform(self, X, y=None):
        X['Location'] = self.lb_.transform(X['Location'])
        
        return X

class CustomPipeline():
    def __init__(self, clf=None, param_grid=None, cv=3, scoring='accuracy',
                 return_train_score=True, verbose=1, n_jobs=-1):
                 self.clf_ = clf
                 self.param_grid_ = param_grid
                 self.cv_ = cv
                 self.scooring_ = scoring
                 self.return_train_score_ = return_train_score
                 self.verbose_ = verbose
                 self.n_jobs_ = n_jobs
                 self.pipeline_ = Pipeline(steps=[('create_month', CustomCreateMonth()),('create_loc_number', CustomFixLocation()),
                                                    ('num_imputer', CustomImputer()), ('num_scaler', CustomScaler()),('cat_imputer',
                                                    CustomCategoryImputer()),('cat_encoder', CustomCategoryEncoder())])
                 self.fullpipeline_ = Pipeline(steps=[('pip',self.pipeline_), ('clf',self.clf_)])
                 self.RF_ =  GridSearchCV(estimator=self.fullpipeline_,  param_grid=self.param_grid_,
                                        scoring=self.scooring_, cv=self.cv_, verbose=self.verbose_,
                                        n_jobs=self.n_jobs_, return_train_score=self.return_train_score_ )
    def fit(self, X, y):
        if y.dtype == 'object':
            y = y.apply(convert_to_numeric)
        self.RF_.fit(X, y)
    
    def predict(self, X):
        preds = self.RF_.predict(X)

        return preds

def convert_to_numeric(val):
    if val == "No":
        return 0
    else:
        return 1