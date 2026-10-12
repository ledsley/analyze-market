from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split,cross_val_score, GridSearchCV
from sklearn.metrics import mean_absolute_error,root_mean_squared_error,r2_score

from main_dataset import clear_df

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


pipeline_randomforest = Pipeline(steps=[
    ('preprocess',preprocessor),
   ('regressor',RandomForestRegressor(random_state=11))])

pipeline_randomforest.fit(X_train,y_train)

pred_randomforest = pipeline_randomforest.predict(X_test)

mae_randomforest = mean_absolute_error(y_test,pred_randomforest)
rmse_randomforest = root_mean_squared_error(y_test,pred_randomforest)
r2_randomforest = r2_score(y_test,pred_randomforest)

print(mae_randomforest)
print(rmse_randomforest)
print(r2_randomforest)

scores_randomforest = -cross_val_score(pipeline_randomforest,X_train,y_train,cv=5,scoring='neg_mean_absolute_error')

scores_randomforest_mean = scores_randomforest.mean()

scores_randomforest_std = scores_randomforest.std()

print(scores_randomforest_mean)
print(scores_randomforest_std)

param_grid = {
    'regressor__n_estimators': [50,100,200],
    'regressor__max_depth': [3,5,10,None],
    'regressor__min_samples_leaf': [1,2,4]
}

gs_randomforest = GridSearchCV(pipeline_randomforest,param_grid,cv=5,scoring='neg_mean_absolute_error')

gs_randomforest.fit(X_train,y_train)

best_model_randomforest = gs_randomforest.best_estimator_

best_model_randomforest_predict = best_model_randomforest.predict(X_test)

best_model_randomforest_mae = mean_absolute_error(y_test,best_model_randomforest_predict)
best_model_randomforest_rmse = root_mean_squared_error(y_test,best_model_randomforest_predict)
best_model_randomforest_r2 = r2_score(y_test,best_model_randomforest_predict)

print(best_model_randomforest_mae)
print(best_model_randomforest_rmse)
print(best_model_randomforest_r2)

best_param = gs_randomforest.best_params_
best_score = -gs_randomforest.best_score_
print(best_param,best_score)