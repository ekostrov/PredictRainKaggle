
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
3. I build two different classifiers and train them.
4. I use over sampling and undersampling to balance data.
5. Tune two classifiers to improve performance.
6. I test tuned classifiers on the data that would be put aside and not used in the training purposes.

# Business Problem

* Predicting rainy weather for the next day is a very important task. 
* It plays a role in farming and other kinds of business, including restaurants, museums, etc.. 
* Good weather forecast plays important role for tourist too.
* Usually weather is predicted by using complicated deterministic models involving partial differential equations. 
* I would like to see how well the rain can be predicted by using Machine Learning.
* At the end I will recommend the best (based on this research) system to predict rainy days.

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
* I Used the same steps for the Test Data and Validation Data except to impute the missing data, I used previously saved data points from imputing process of the train/evaluation data.
* I used over sampling and under sampling to balance data.

***
# Modeling

 ## I have built the following two classifiers to compare the results based on the "f1" score as a primary metric and the inspection of the confusion matrix as a secondary metric:

* Random Forest Classifier
* XG Bosst Classifier

> Out of the box four "vanilla" classifiers "Random Forest" and "XG Boost" did fine on the "f1" metric achieving 90.4% and 90.5% respectively, but inspection of the confusion matrix shows that the models are not doing great on the false positives and false negatives (precion is much higher than recall). 

## I decided to "balance" the data with Over and Under sampling techniques.
> The performance has not improved

## I tuned up both models to improve the performance.
* Tuned up models lost a bit of performance on "f1" score, Random Forest has 89% and XGBoost has 88.9% but performed much better on the inspection of the confusion matrix (we have precision equal to recall). 
* After tuning Random Forest does overfit while XGBoost doesn't.
***
# Conclusions
***

## Modeling

* ## "Vanilla"  Random FOrest and XGBoost models performed just fine achieve overall f1 score about 90.3% and 90.5% respectively but f1 score just on the "rain" category is just 62% and 65% with about 77% and 75% precision respectively.
* ## Over and Under sampling didn't improve the performance.
* ## Tuninng up moved the performance on f1 score down a little bit but balanced out  precision  and recall scores.


***
# Business Suggestion:
***
## Based on my analysis, I suggest to use Tuned Up XGBoost model for the predicion of rain tomorrow based on the data about today's wheather.
***
# Ways to improve the prject
* Optimize the code by creating pipelines. This will make the project better and it would be easier to use and tune up different classifiers.
* It would be good to try feature engineering but it is hard without being an expert in the subject matter.
* Dive deeper into the tuning of the models to improve results for the f1 score while keeping precision and recall balanced.

# Please review my full work in [Jupyter Notebook](JupyterNotebooks/Jupyter.ipynb) or in the [non technical presentation](presentation_non_technical.pdf)

For any additional questions, please contact Yevgeniy (Gene) Kostrov at ekostrov@yahoo.com