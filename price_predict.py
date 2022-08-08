import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor
import pickle

df = pd.read_csv(r'.\dataset\train.csv')

columns=['LotArea','OverallQual','OverallCond','YearBuilt','SalePrice']
df = df[columns]

X = df.iloc[:, 0:4]
y = df.iloc[:, 4:]

y = y.values.ravel()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

lrbase=LinearRegression()
lrbase.fit(X_train, y_train)
lr = RandomForestRegressor(random_state=101, n_estimators=200)
lr.fit(X_train, y_train)
gbm1 = GradientBoostingRegressor(learning_rate=0.1, n_estimators=100, min_samples_split=2, 
                                 min_samples_leaf=1, max_depth=3, subsample=1.0, max_features= None, 
                                 random_state=100)
gbm1.fit(X_train, y_train)
xgb1 = XGBRegressor(learning_rate=0.1, n_estimators=100, max_depth=3, subsample=1.0, random_state=101)
xgb1.fit(X_train, y_train)

pickle.dump(lr, open('model.pkl', 'wb'))