import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.metrics import mean_absolute_error,root_mean_squared_error,r2_score

from dataframes import clear_df

X = clear_df.drop(columns = ['id','price_rub'])
y = clear_df['price_rub']

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=11)

num_cols = X.select_dtypes(include=['number']).columns
cat_cols = X.select_dtypes(include=['object','string','str']).columns

num_transformer = Pipeline(steps=[('scaler', StandardScaler())])

cat_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(transformers=[
        ('num',num_transformer,num_cols),
        ('cat',cat_transformer,cat_cols)])

pl = Pipeline(
    steps=[
        ('preprocess',preprocessor),
        ('regressor',LinearRegression())   
    ]
)

#pl.fit(X_train,y_train)

#pred = pl.predict(X_test)

#mae = mean_absolute_error(y_test,pred)
#rmse = root_mean_squared_error(y_test,pred)
#r2 = r2_score(y_test,pred)

#pred_train = pl.predict(X_train)

#mae_train = mean_absolute_error(y_train,pred_train)
#rmse_train = root_mean_squared_error(y_train,pred_train)
#r2_train = r2_score(y_train,pred_train)

print(cross_val_score(pl,X_train,y_train,cv=5,scoring='neg_mean_absolute_error'))