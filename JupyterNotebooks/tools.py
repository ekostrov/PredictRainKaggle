import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.model_selection import GridSearchCV
def modify_df(df, saved_median):
    pass


def fill_missing_values(data, saved_median):
    """
    Function fills missing values
    for the Test Data with values
    from the provided DataFrame
    'saved_median"
    Input:
    data -> DataFrame to be imputed
    saved_median -> DataFrame with saved values
    """

    cols = [cl for cl in data.columns if data[cl].dtype in ['float64']]
    for location in data.Location.unique():
        print("Workin on Location: ", location)
        for month in data.Month.unique():
            for column in cols:
                idx = list(data[(data.Location == location) 
                         & (data.Month == month) 
                         & (data[column].isna())].index)
                fill_value = saved_median[(saved_median.Location==location)
                                        & (saved_median.Month == month)][column]
                data.loc[idx,column] = float(fill_value)

                
def print_results(clf, X_val, y_val):
    """
    Input:
    clf -> trained classifier
    (X_val, y_val) -> validation values
    Output:
    function prints out:
    1. confustion matrix
    2. accuracy score
    3. precision score
    4. recall score
    5. f1 score
    """
    y_pred = clf.predict(X_val)
    print(confusion_matrix(y_val,y_pred), ": is the confustion matrix\n")
    print(accuracy_score(y_val,y_pred), ": is the accuracy score")
    print(precision_score(y_val,y_pred), ": is the precision score")
    print(recall_score(y_val,y_pred), ": is the recall score")
    print(f1_score(y_val,y_pred), ": is the f1 score")
    
    
    
def create_month(df):
    """
    Function creates a column
    Month from the Column Date
    and Removes the column Date
    from the DataFrame.
    Input:
    df -> DataFrame with column Date
    Output:
    function creates a column with Month removes the Date column 
    """
    df['Month'] = df.Date.apply(lambda x : int(x.split('-')[1]))
    df.drop('Date', axis=1, inplace=True)
    
    
def print_missing(df):
    """
    Function prints info 
    about missing values.
    Input:
    df -> DataFrame
    Output:
    prints out number and percent of missing
    values for numerical columns
    """
    zeros_cnt = df.isnull().sum().sort_values(ascending=False)
    percent_zeros = ( df.isnull().sum() /  df.isnull().count()).sort_values(ascending=False)

    missing_data = pd.concat([zeros_cnt, percent_zeros], axis=1, keys=['Total', 'Percent'])
    print("*"*50)
    print(missing_data)
    print("*"*50)

def assessClassifier(clf,allValues):
    """
    Function fits classifier 'clf' 
    by using provided values in the
    allValues, calculates appropriate
    scores, and returns the scores as
    a dictionary
    Input:
    clf -> classifier to fit
    allValues -> tuple of the form (X_train, X_val, y_train, y_test)
    Output:
    dictionary of the form:
    {'name':name,'f1':f1, 'precision':precision,'recall':recall,'roc_auc_score':roc_auc_sc,'accuracy':accuracy}
    """
    name = str(clf)
    X_train,X_test,y_train,y_test = allValues
    pipe = Pipeline([(name, clf)])
    pipe.fit(X_train,y_train)
    y_pred = pipe.predict(X_test)
    f1 = f1_score(y_test, y_pred)
    precision = precision_score(y_test,y_pred)
    recall = recall_score(y_test,y_pred)
    roc_auc_sc = roc_auc_score(y_test,y_pred)
    accuracy = accuracy_score(y_test,y_pred)
    return {'name':name,'f1':f1, 'precision':precision,'recall':recall,'roc_auc_score':roc_auc_sc,'accuracy':accuracy}


def assessClassifier_cv(clf,allValues, cv = 5):
    """
    Function fits classifier 'clf' 
    by using provided values in the
    allValues, calculates appropriate
    scores, and returns the scores as
    a dictionary
    Input:
    clf -> classifier to fit
    allValues -> tuple of the form (X_train, X_val, y_train, y_test)
    Output:
    dictionary of the form:
    {'name':name,'f1':f1, 'precision':precision,'recall':recall,'roc_auc_score':roc_auc_sc,'accuracy':accuracy}
    """
    scoring = ['precision', 'recall','f1','accuracy','roc_auc']
    name = clf.__class__.__name__
    X_train, y_train = allValues
    #clf.fit(X_train,y_train)
    scores = cross_validate(clf, X_train, y_train, scoring=scoring, cv=cv, return_estimator=True)
    print(sorted(scores.keys()))
    f1 = scores['test_f1'].mean()
    precision = scores['test_precision'].mean()
    accuracy = scores['test_accuracy'].mean()
    recall = scores['test_recall'].mean()
    roc_auc_sc = scores['test_roc_auc'].mean()
    print(scores.keys())
    return {'name':name,'f1':f1, 'precision':precision,'recall':recall,'roc_auc_score':roc_auc_sc,'accuracy':accuracy}


def testClassifier(clf, param_grid, scoring ,values,cv=5):
    """
    function creates GridSearchCV object,
    fits it on values and prints out 
    the resuls for scores
    Input:
    clf -> classifier to test
    param_grid -> grid of parameters for this clf
    values -> tuple of the type (X_train, X_val, X_test, y_train, y_val, y_test)
    Output:
    prints out the results for
    Training Data,
    Validation Data,
    and Testing Data
    '"""
    X_train, X_test, y_train, y_test = values 
    grid = GridSearchCV(clf, param_grid=param_grid, cv=cv,
                                    scoring=scoring,
                            return_train_score=True, verbose=1, n_jobs = -1)
    grid.fit(X_train,y_train)
    print("*"*50)
    print("** Results for Training Data **")
    print("*"*50)
    print_results(grid,X_train,y_train)
    print("*"*50)
    print("*"*50)
    print("** Results for Testing Data **")
    print("** not used for training/validation **")
    print("*"*50)
    print_results(grid,X_test,y_test)
    print("*"*50)
    
    return grid

def modify_data(X,y, saved_median, str_columns, num_columns,lb, num_pipline,):
    #print_missing(X)#print missing values/percents
    print("-"*50)
    print("Modifying Data")
    print("-"*50)
    create_month(X) #create month column and drop date
    fill_missing_values(X, saved_median) # Fill in missing values by using previously saved ones in "saved_median"
    # Transform String columns
    ohe = pd.get_dummies(data=X, columns=['WindGustDir','WindDir9am','WindDir3pm','Location'],drop_first=True)
    ohe['RainToday'] = X['RainToday'].astype(str)
    ohe['RainTomorrow'] =y.astype(str)
    ohe['RainToday'] = lb.transform(ohe['RainToday']) # use fitted LabelBinarizer to transform column
    ohe['RainTomorrow'] = lb.transform(ohe['RainTomorrow'])
    ohe = ohe.dropna()
    y = ohe['RainTomorrow']
    X = ohe.drop(['RainTomorrow'], axis=1)
    X[num_columns] = num_pipline.transform(X[num_columns]) # use fitted pipeline to transform numerical columns
    return X,y