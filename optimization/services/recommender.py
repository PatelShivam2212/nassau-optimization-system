# from optimization.models import Factory, Product
# from .calculator import calculate_distance
#
#
# def get_best_factory(product_id, customer_lat, customer_lon, priority_weight=0.5):
#     """
#     Finds the optimal factory based on a weighted score of:
#     1. Distance (Speed/Lead Time)
#     2. Profit Stability (Financial Risk)
#
#     priority_weight: 0.0 (Pure Profit/Safety) to 1.0 (Pure Speed/Distance)
#     """
#     try:
#         product = Product.objects.get(id=product_id)
#     except Product.DoesNotExist:
#         return None
#
#     all_factories = Factory.objects.all()
#     best_factory = None
#     best_score = float('inf')
#
#     current_factory = product.current_factory
#
#     # Historical base distance for normalization (approx across US)
#     MAX_DISTANCE_REF = 3000
#
#     for factory in all_factories:
#         # --- 1. SPEED METRIC (Distance) ---
#         dist = calculate_distance(customer_lat, customer_lon, factory.latitude, factory.longitude)
#         # Normalize distance to a 0-1 scale
#         distance_score = dist / MAX_DISTANCE_REF
#
#         # --- 2. PROFIT STABILITY METRIC (Risk) ---
#         # Moving away from the legacy factory introduces risk/cost.
#         # If it's the current factory, risk is 0. If moving, risk is higher.
#         profit_risk_score = 0 if factory == current_factory else 0.4
#
#         # --- 3. COMBINED DECISION LOGIC ---
#         # Formula: (Distance * Speed Weight) + (Risk * Profit Weight)
#         # Lower score = Better recommendation
#         total_score = (distance_score * priority_weight) + (profit_risk_score * (1 - priority_weight))
#
#         if total_score < best_score:
#             best_score = total_score
#             best_factory = factory
#             best_dist = dist
#
#     # Calculate Confidence Score (KPI)
#     # Higher confidence if the lead time reduction is significant vs the risk
#     confidence_score = round(max(0, 1 - best_score) * 100, 2)
#
#     return {
#         "product_name": product.name,
#         "current_factory": current_factory.name,
#         "recommended_factory": best_factory.name,
#         "distance_miles": round(best_dist, 2),
#         "is_optimized": best_factory != current_factory,
#         "kpi_metrics": {
#             "scenario_confidence": f"{confidence_score}%",
#             "profit_impact": "Stable" if best_factory == current_factory else "Review Required",
#             "optimization_strategy": "Speed-Focused" if priority_weight > 0.5 else "Profit-Focused"
#         }
#     }

from optimization.models import Factory, Product
from .calculator import calculate_distance


def get_best_factory(product_id, customer_lat, customer_lon, priority_weight=0.5, top_n=3):
    """
    Finds the optimal factory based on a weighted score of:
    1. Distance (Speed/Lead Time)
    2. Profit Stability (Financial Risk)

    priority_weight: 0.0 (Pure Profit/Safety) to 1.0 (Pure Speed/Distance)
    top_n: number of top recommendations to return
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return None

    all_factories = Factory.objects.all()
    current_factory = product.current_factory

    # Historical base distance for normalization (approx across US)
    MAX_DISTANCE_REF = 3000

    # Collect scores for all factories
    scored_factories = []

    for factory in all_factories:
        # --- 1. SPEED METRIC (Distance) ---
        dist = calculate_distance(customer_lat, customer_lon, factory.latitude, factory.longitude)
        # Normalize distance to a 0-1 scale
        distance_score = dist / MAX_DISTANCE_REF

        # --- 2. PROFIT STABILITY METRIC (Risk) ---
        # Moving away from the legacy factory introduces risk/cost.
        profit_risk_score = 0 if factory == current_factory else 0.4

        # --- 3. COMBINED DECISION LOGIC ---
        total_score = (distance_score * priority_weight) + (profit_risk_score * (1 - priority_weight))

        scored_factories.append({
            "factory": factory,
            "score": total_score,
            "distance": dist
        })

    # Sort by score (lower is better)
    scored_factories.sort(key=lambda x: x["score"])

    # Top N recommendations
    top_recommendations = []
    for i, item in enumerate(scored_factories[:top_n]):
        top_recommendations.append({
            "rank": i+1,
            "factory_name": item["factory"].name,
            "distance_miles": round(item["distance"], 2),
            "score": round(item["score"], 4),
            "is_current": item["factory"] == current_factory
        })

    # Best one
    best = top_recommendations[0]
    best_score = best["score"]
    best_dist = best["distance_miles"]
    best_factory = best["factory_name"]

    # Calculate Confidence Score (KPI)
    confidence_score = round(max(0, 1 - best_score) * 100, 2)

    return {
        "product_name": product.name,
        "current_factory": current_factory.name,
        "recommended_factory": best_factory,
        "distance_miles": best_dist,
        "is_optimized": best_factory != current_factory.name,
        "ranked_recommendations": top_recommendations,  # NEW
        "kpi_metrics": {
            "scenario_confidence": f"{confidence_score}%",
            "profit_impact": "Stable" if best_factory == current_factory.name else "Review Required",
            "optimization_strategy": "Speed-Focused" if priority_weight > 0.5 else "Profit-Focused"
        }
    }