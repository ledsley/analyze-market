from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import joblib
from main_dataset import clear_df
from pathlib import Path

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

pipeline_linearregression = Pipeline(
    steps=[
        ('preprocess',preprocessor),
        ('regressor',LinearRegression())   
    ]
)

pipeline_linearregression.fit(X_train,y_train)

base_dir = Path(__file__).resolve().parent
model_file = base_dir / 'lr_model.joblib'

joblib.dump(pipeline_linearregression,model_file)