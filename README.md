
```
├── README.md                           <- The top-level README for reviewers of this project
├── JupyterNotebooks/Jupyter.ipynb      <- Narrative documentation of analysis in Jupyter notebook
├── presentation.pdf                    <- PDF version of project presentation
├── data                                <- Both sourced externally 
└── images                              <- Both sourced externally and generated from code
```
![title_picture](images/1786.webp)
***
# Predict Rain in Australia
** By Yevgeniy Kostrov
***

# Overview 
The purpose of this project is to use weather dataset from Kaggle to predict rainfall for the next day based on the data about today's weather.

During the analysis:
1. I analyze data.
2. I deal with missing values.
3. I build few different classifiers and train them.
4. I select three best classifiers from step 3. and tune them to improve performance.
5. I test tuned classifiers on the data that would be put aside and not used in the training/validation purposes.

# Business Problem

Predicting rainy weather for the next day is a very important task. It plays a role in farming and other kinds of business, including restaurants, museums, etc.. Good weather forecast plays important role for tourist too. Usually weather is predicted by using complicated deterministic models involving partial differential equations. I would like to see how well the rain can be predicted by using Machine Learning.

***
# Data Description
The file called ['weatherAUS.csv'](data/weatherAUS.csv) holds the data for this project. Taken from Kaggle: "This dataset contains about 10 years of daily weather observations from many locations across Australia. RainTomorrow is the target variable to predict. It means -- did it rain the next day, Yes or No? This column is Yes if the rain for that day was 1mm or more."

#### Column Names and descriptions for Wheather Data Set

* **Date** - date
* **Location** - location
* **MinTemp** - minimum temperature for the day
* **MaxTemp** - maximum temperature for the day
* **Rainfall** - rainfall for the day
* **Evaporation** - evaporation for the day
* **Sunshine** - amount of sunlight
* **WindGustDir** - direction of the wind
* **WindGustSpeed** - speed of wind gust
* **WindDir9am** - wind direction at 9am
* **WindDir3pm** - wind direction at 3pm
* **WindSpeed9am** - wind speed at 9am
* **WindSpeed3pm** - wind speed at 3pm
* **Humidity9am** - humidity at 9am 
* **Humidity3pm** - humidity at 3pm
* **Pressure9am** - atmospheric pressure at 9am
* **Pressure3pm** - atmospheric pressure at 3pm
* **Cloud9am** - cloudiness at 9am
* **Cloud3pm** - cloudiness at 3pm
* **Temp9am** - air temperature at 9am
* **Temp3pm** - air temperature at 3pm
* **RainToday** - does it rain today or not
* **RainTomorrow** - does it rain tomorrow

Source & Acknowledgements
* Observations were drawn from numerous weather stations. The daily observations are available from [www.bom.gov](http://www.bom.gov.au/climate/data). 

* An example of latest weather observations in Canberra: http://www.bom.gov.au/climate/dwo/IDCJDW2801.latest.shtml

* Definitions adapted from http://www.bom.gov.au/climate/dwo/IDCJDW0000.shtml

* Data source: http://www.bom.gov.au/climate/dwo/ and http://www.bom.gov.au/climate/data.

* Copyright Commonwealth of Australia 2010, Bureau of Meteorology.


## Cleaning/Modifying Data:
* I extracted the month out of the Date column and saved it into the Month column. It seems more reasonable to use the month rather than specific date for rain prediction
* There were quite a lot of missing data in the numerical columns. I have filled the missing data with average values for the same region and the same month. I saved the data used to fill in the missing data into a separate Data Frame to use it later on to impute the missing values in the Test Data  (Test Data is not used for training/validation purposes).
* I scaled the data.
* I Used the same steps for the Test Data except to impute the missing data, I used previously saved data points from imputing process of the train/evaluation data.

***
# Modeling

 ## I have built the following classifiers to compare the results based on "recall" score as a primary metric and "precision" score as a secondary metric:
* Logistic Regression Classifier
* Random Forest Classifier
* K Nearest Neighbors Classifier
* Support Vector Machines Classifier
* XG Bosst Classifier
* Naive Bayes Classifier

Out of the box four "vanilla" classifiers "Logistic Regression", "Random Forest", "Support Vector Machines", and "XG Boost"  performed from 93% to 95.8% on "recall" metric and from 85.1% to 87% on the "precision" metric on the validation data set.

# * All four models preformed better after tune up 
## Here is the summary of preformance
*Logistic Regression Classifier*

After tuning hyper parameters for Logistic Regression classifier we have the following results:

* Logistic Regression classifier went up from 93.6% to 100% on validation data.
* Logistic Regression classifier achieves 100% on test data that I have not used for training.
* The precision score went down from 85.5% to 75.7% on validation data.
* The precision score on test data is 75.9%.

*Random Forest Classifier*

After tuning hyper parameters for Random Forest classifier we have the following results:
* Random Forest classifier went up from 94.87% to 94.97% on validation data.
* Random Forest classifier achieves 95% on test data that I have not used for training.
* The precision score stays at 86% on validation data.
* The precision score on test data is 86%.

*HGBoost Classifier*

After tuning hyper parameters for HGBoost classifier we have the following results:
* HGBoost classifier went up from 94% to 97.7% on validation data.
* HGBoost classifier achieves 97.7% on test data that I have not used for training.
* The precision score went from 87% to 80.6% on validation data.
* The precision score on test data is 80.6%.

*Support Vector Machines Classifier*

After tuning hyper parameters for Support Vector Machines classifier we have the following results:
* Support Vector Machines classifier went up from 95.9% to 100% on validation data.
* Support Vector Machines classifier achieves 100% on test data that I have not used for training.
* The precision score went from 85.1% to 75.7% on validation data.
* The precision score on test data is 75.9%.
***
***
# Conclusions
## Modeling

* #  Baseline models perform really well out of the box.
* # Tuninng up imporoved the performance.
## Comments on the performance after tuning 
* It seems that the best choice for the model is HGBoost since it has the best balance between recall score at 97.7% on the test data and precision score at 80.6% on the test data. 
* If one wants to neglect the precision score (labeling a lot of non-rainy days as rainy), then the best choice is Logistic Regression. Even though it is close in performance to Support Vector Machines, it is lighter and easier to retrain.

# Ways to improve the prject
* Optimize the code by creating pipelines. This will make the project better and it would be easier to use and tune up different classifiers.
* It would be good to try data engineering but it is hard without being an expert in the subject matter.
* Dive deeper into the tuning of the models to improve results for the precision score while keeping recall score high.

# Please review my full work in [Jupyter Notebook](JupyterNotebooks/Jupyter.ipynb) or in the [non technical presentation](presentation_non_technical.pdf)

For any additional questions, please contact Yevgeniy (Gene) Kostrov at ekostrov@yahoo.com