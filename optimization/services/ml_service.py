# import pandas as pd
# import numpy as np
# import joblib
# import os
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# from sklearn.preprocessing import LabelEncoder
# from optimization.models import Order
#
#
# class MLService:
#     def __init__(self):
#         # Paths for saving the winning model and translation keys
#         self.model_path = os.path.join(os.path.dirname(__file__), '../ml_models/lead_time_model.joblib')
#         self.encoder_path = os.path.join(os.path.dirname(__file__), '../ml_models/encoders.joblib')
#         os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
#
#     def train_model(self):
#         # 1. Fetch data from the database
#         orders = Order.objects.all().values(
#             'order_date', 'ship_date', 'ship_mode', 'region', 'product__division', 'sales'
#         )
#         df = pd.DataFrame(list(orders))
#
#         if df.empty:
#             return "No data found. Please run import_order first."
#
#         # 2. Feature Engineering: Target Variable = Lead Time
#         df['order_date'] = pd.to_datetime(df['order_date'])
#         df['ship_date'] = pd.to_datetime(df['ship_date'])
#         df['lead_time'] = (df['ship_date'] - df['order_date']).dt.days
#
#         # 3. Encoding Categorical Variables (Translatation for the AI)
#         encoders = {}
#         for col in ['ship_mode', 'region', 'product__division']:
#             le = LabelEncoder()
#             df[col] = le.fit_transform(df[col])
#             encoders[col] = le
#
#         # 4. Prepare Feature Matrix (X) and Target Vector (y)
#         X = df[['ship_mode', 'region', 'product__division', 'sales']]
#         y = df['lead_time']
#
#         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
#         # 5. Requirement: Compare Multiple Models
#         models = {
#             "Linear Regression": LinearRegression(),
#             "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
#             "Gradient Boosting": GradientBoostingRegressor(random_state=42)
#         }
#
#         best_r2 = -float('inf')
#         best_model = None
#         all_metrics = {}
#
#         for name, model in models.items():
#             # Train
#             model.fit(X_train, y_train)
#
#             # Predict & Evaluate
#             preds = model.predict(X_test)
#             r2 = r2_score(y_test, preds)
#             mae = mean_absolute_error(y_test, preds)
#             rmse = np.sqrt(mean_squared_error(y_test, preds))
#
#             all_metrics[name] = {"R2": r2, "MAE": mae, "RMSE": rmse}
#
#             # Identify the best performing model
#             if r2 > best_r2:
#                 best_r2 = r2
#                 best_model = model
#                 best_model_name = name
#
#         # 6. Save the Best Model and Encoders
#         joblib.dump(best_model, self.model_path)
#         joblib.dump(encoders, self.encoder_path)
#
#         # Return metrics for all models to show in the executive summary
#         return {
#             "all_results": all_metrics,
#             "winner": best_model_name,
#             "best_r2": best_r2
#         }

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
from optimization.models import Order


class MLService:
    def __init__(self):
        # Paths for saving the winning model and translation keys
        self.model_path = os.path.join(os.path.dirname(__file__), '../ml_models/lead_time_model.joblib')
        self.encoder_path = os.path.join(os.path.dirname(__file__), '../ml_models/encoders.joblib')
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

    def train_model(self):
        # 1. Fetch data from the database
        # NEW: include factory name via product__current_factory__name
        orders = Order.objects.select_related('product__current_factory').values(
            'order_date', 'ship_date', 'ship_mode', 'region',
            'product__division', 'product__current_factory__name', 'sales'
        )
        df = pd.DataFrame(list(orders))

        if df.empty:
            return "No data found. Please run import_order first."

        # 2. Feature Engineering: Target Variable = Lead Time
        df['order_date'] = pd.to_datetime(df['order_date'])
        df['ship_date'] = pd.to_datetime(df['ship_date'])
        df['lead_time'] = (df['ship_date'] - df['order_date']).dt.days

        # 3. Encoding Categorical Variables
        encoders = {}
        # NEW: include factory name in categorical columns
        for col in ['ship_mode', 'region', 'product__division', 'product__current_factory__name']:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            encoders[col] = le

        # 4. Prepare Feature Matrix (X) and Target Vector (y)
        # NEW: add factory column
        X = df[['ship_mode', 'region', 'product__division', 'product__current_factory__name', 'sales']]
        y = df['lead_time']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 5. Requirement: Compare Multiple Models
        models = {
            "Linear Regression": LinearRegression(),
            "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
            "Gradient Boosting": GradientBoostingRegressor(random_state=42)
        }

        best_r2 = -float('inf')
        best_model = None
        all_metrics = {}

        for name, model in models.items():
            # Train
            model.fit(X_train, y_train)

            # Predict & Evaluate
            preds = model.predict(X_test)
            r2 = r2_score(y_test, preds)
            mae = mean_absolute_error(y_test, preds)
            rmse = np.sqrt(mean_squared_error(y_test, preds))

            all_metrics[name] = {"R2": r2, "MAE": mae, "RMSE": rmse}

            # Identify the best performing model
            if r2 > best_r2:
                best_r2 = r2
                best_model = model
                best_model_name = name

        # 6. Save the Best Model and Encoders
        joblib.dump(best_model, self.model_path)
        joblib.dump(encoders, self.encoder_path)

        # Return metrics for all models to show in the executive summary
        return {
            "all_results": all_metrics,
            "winner": best_model_name,
            "best_r2": best_r2
        }