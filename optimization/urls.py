# from django.urls import path
# from . import views
#
# urlpatterns = [
#     # Your existing path
#     path('recommend/', views.recommendation_api, name='recommend_api'),
#
#     # New path for the simulation engine
#     path('simulate/<int:product_id>/', views.simulation_api, name='simulation_api'),
#
# path('clusters/', views.clustering_api, name='clustering_api'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    # 1. Recommendation API (Weighted Optimization)
    path('recommend/', views.recommendation_api, name='recommend_api'),

    # 2. Simulation Engine (Predictive Analytics)
    path('simulate/<int:product_id>/', views.simulation_api, name='simulation_api'),

    # 3. Clustering API (Route Performance Analysis)
    path('clusters/', views.clustering_api, name='clustering_api'),

    # --- NEW: Master Data Endpoints (Requirement Compliance) ---

    # 4. Factory Master Data (Coordinates for Haversine Math)
    path('factories/', views.factory_list_api, name='factory_list_api'),

    # 5. Product Correlation Data (Legacy Rule Auditing)
    path('correlations/', views.product_correlation_api, name='product_correlation_api'),
]