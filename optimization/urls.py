from django.urls import path
from . import views

urlpatterns = [
    # Your existing path
    path('recommend/', views.recommendation_api, name='recommend_api'),

    # New path for the simulation engine
    path('simulate/<int:product_id>/', views.simulation_api, name='simulation_api'),

path('clusters/', views.clustering_api, name='clustering_api'),
]