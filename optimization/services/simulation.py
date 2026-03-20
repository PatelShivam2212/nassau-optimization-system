# # import joblib
# # import os
# # import pandas as pd
# # from optimization.models import Factory, Product, Order
# # from .calculator import calculate_distance
# #
# #
# # class SimulationEngine:
# #     def __init__(self):
# #         # Load the trained model and encoders
# #         base_path = os.path.join(os.path.dirname(__file__), '../ml_models/')
# #         self.model = joblib.load(os.path.join(base_path, 'lead_time_model.joblib'))
# #         self.encoders = joblib.load(os.path.join(base_path, 'encoders.joblib'))
# #
# #     def simulate_reassignment(self, product_id):
# #         product = Product.objects.get(id=product_id)
# #         current_factory = product.current_factory
# #         factories = Factory.objects.all()
# #
# #         # Get historical average sales for this product to use in simulation
# #         avg_sales = Order.objects.filter(product=product).values_list('sales', flat=True)
# #         mean_sales = sum(avg_sales) / len(avg_sales) if avg_sales else 10.0
# #
# #         results = []
# #
# #         for factory in factories:
# #             # Predict Lead Time using the ML Model
# #             # We simulate a "Standard Class" shipment to the "Interior" region as a baseline
# #             input_data = pd.DataFrame([{
# #                 'ship_mode': self.encoders['ship_mode'].transform(['Standard Class'])[0],
# #                 'region': self.encoders['region'].transform(['Interior'])[0],
# #                 'product__division': self.encoders['product__division'].transform([product.division])[0],
# #                 'sales': mean_sales
# #             }])
# #
# #             predicted_lead_time = self.model.predict(input_data)[0]
# #
# #             # Calculate operational metrics
# #             # Note: In a real scenario, we'd calculate distance to a specific region hub
# #             # Here we use a fixed reference point (e.g., center of US) for comparison
# #             dist = calculate_distance(factory.latitude, factory.longitude, 39.8283, -98.5795)
# #
# #             results.append({
# #                 "factory_name": factory.name,
# #                 "predicted_lead_time": round(predicted_lead_time, 1),
# #                 "distance_to_hub": round(dist, 2),
# #                 "is_current": factory == current_factory,
# #                 "efficiency_gain": "N/A" if factory == current_factory else f"{round(((predicted_lead_time / 10) * 100), 1)}%"
# #                 # Simulated logic
# #             })
# #
# #         return {
# #             "product": product.name,
# #             "current_production_site": current_factory.name,
# #             "simulations": sorted(results, key=lambda x: x['predicted_lead_time'])
# #         }
# import joblib
# import os
# import pandas as pd
# from optimization.models import Factory, Product, Order
# from .calculator import calculate_distance
#
#
# class SimulationEngine:
#     def __init__(self):
#         # Load the trained model and encoders
#         base_path = os.path.join(os.path.dirname(__file__), '../ml_models/')
#         self.model = joblib.load(os.path.join(base_path, 'lead_time_model.joblib'))
#         self.encoders = joblib.load(os.path.join(base_path, 'encoders.joblib'))
#
#     def simulate_reassignment(self, product_id):
#         product = Product.objects.get(id=product_id)
#         current_factory = product.current_factory
#         factories = Factory.objects.all()
#
#         # Get historical average sales for this product
#         avg_sales = Order.objects.filter(product=product).values_list('sales', flat=True)
#         mean_sales = sum(avg_sales) / len(avg_sales) if avg_sales else 10.0
#
#         results = []
#
#         # Reference Point: Center of US (Geographic Hub)
#         HUB_LAT, HUB_LON = 39.8283, -98.5795
#
#         for factory in factories:
#             # 1. Base Prediction from ML Model
#             input_data = pd.DataFrame([{
#                 'ship_mode': self.encoders['ship_mode'].transform(['Standard Class'])[0],
#                 'region': self.encoders['region'].transform(['Interior'])[0],
#                 'product__division': self.encoders['product__division'].transform([product.division])[0],
#                 'sales': mean_sales
#             }])
#
#             # The ML model gives us a statistical baseline
#             base_lead_time = self.model.predict(input_data)[0]
#
#             # 2. Distance Calculation
#             dist = calculate_distance(factory.latitude, factory.longitude, HUB_LAT, HUB_LON)
#
#             # 3. Decision Intelligence logic:
#             # Adjust lead time based on distance (roughly 1 day per 400 miles)
#             # This ensures each factory has a unique, logical prediction
#             adjusted_lead_time = base_lead_time + (dist / 400)
#
#             results.append({
#                 "factory_name": factory.name,
#                 "predicted_lead_time": round(adjusted_lead_time, 2),
#                 "distance_to_hub": round(dist, 2),
#                 "is_current": factory == current_factory,
#                 "efficiency_gain": "N/A" if factory == current_factory else f"{round((1 - (adjusted_lead_time / 10)) * 100, 1)}%"
#             })
#
#         return {
#             "product": product.name,
#             "current_production_site": current_factory.name,
#             "simulations": sorted(results, key=lambda x: x['predicted_lead_time'])
#         }

import joblib
import os
import pandas as pd
from optimization.models import Factory, Product, Order
from .calculator import calculate_distance


class SimulationEngine:
    def __init__(self):
        # Load the trained model and encoders
        base_path = os.path.join(os.path.dirname(__file__), '../ml_models/')
        self.model = joblib.load(os.path.join(base_path, 'lead_time_model.joblib'))
        self.encoders = joblib.load(os.path.join(base_path, 'encoders.joblib'))

    def simulate_reassignment(self, product_id, region='Interior', ship_mode='Standard Class'):
        product = Product.objects.get(id=product_id)
        current_factory = product.current_factory
        factories = Factory.objects.all()

        # Get historical average sales for this product
        avg_sales = Order.objects.filter(product=product).values_list('sales', flat=True)
        mean_sales = sum(avg_sales) / len(avg_sales) if avg_sales else 10.0

        results = []

        # Reference Point: Center of US (Geographic Hub) – used only for distance baseline
        HUB_LAT, HUB_LON = 39.8283, -98.5795

        # Cost per mile (assumption for profit impact)
        COST_PER_MILE = 0.5

        # Baseline distance (distance from current factory to hub) – used for profit impact calculation
        baseline_dist = calculate_distance(current_factory.latitude, current_factory.longitude, HUB_LAT, HUB_LON)

        # In optimization/services/simulation.py, inside simulate_reassignment:

        for factory in factories:
            # 1. Encode features safely
            try:
                encoded_ship_mode = self.encoders['ship_mode'].transform([ship_mode])[0]
            except (KeyError, ValueError):
                encoded_ship_mode = 0
            try:
                encoded_region = self.encoders['region'].transform([region])[0]
            except (KeyError, ValueError):
                encoded_region = 0
            try:
                encoded_division = self.encoders['product__division'].transform([product.division])[0]
            except (KeyError, ValueError):
                encoded_division = 0
            try:
                encoded_factory = self.encoders['product__current_factory__name'].transform([factory.name])[0]
            except (KeyError, ValueError):
                encoded_factory = 0

            input_data = pd.DataFrame([{
                'ship_mode': encoded_ship_mode,
                'region': encoded_region,
                'product__division': encoded_division,
                'product__current_factory__name': encoded_factory,
                'sales': mean_sales
            }])
            # ... rest of the code
            # The ML model gives us a statistical baseline
            base_lead_time = self.model.predict(input_data)[0]

            # 2. Distance Calculation
            dist = calculate_distance(factory.latitude, factory.longitude, HUB_LAT, HUB_LON)

            # 3. Decision Intelligence logic: adjust lead time based on distance
            adjusted_lead_time = base_lead_time + (dist / 400)

            # 4. Profit Impact Calculation
            # profit_impact = (distance - baseline_distance) * cost_per_mile
            profit_impact = (dist - baseline_dist) * COST_PER_MILE

            results.append({
                "factory_name": factory.name,
                "predicted_lead_time": round(adjusted_lead_time, 2),
                "distance_to_hub": round(dist, 2),
                "is_current": factory == current_factory,
                "efficiency_gain": "N/A" if factory == current_factory else f"{round((1 - (adjusted_lead_time / 10)) * 100, 1)}%",
                "profit_impact": round(profit_impact, 2)  # NEW field
            })

        return {
            "product": product.name,
            "current_production_site": current_factory.name,
            "simulations": sorted(results, key=lambda x: x['predicted_lead_time'])
        }