# from django.http import JsonResponse
# from django.shortcuts import render
# from .services.recommender import get_best_factory
# from .services.simulation import SimulationEngine
# from .services.clustering_service import ClusteringService  # New Service
#
#
# # 1. Updated Recommendation API
# def recommendation_api(request):
#     """
#     Updated to handle dynamic inputs from the Streamlit sidebar.
#     """
#     # Get parameters from request.GET (sent by Streamlit)
#     # Falling back to your sample defaults if not provided
#     product_id = request.GET.get('product_id', 1)
#     customer_lat = float(request.GET.get('lat', 40.7128))
#     customer_lon = float(request.GET.get('lon', -74.0060))
#
#     # NEW: Optimization Priority Slider (Speed vs Profit)
#     # value between 0.0 and 1.0
#     priority = float(request.GET.get('priority', 0.5))
#
#     result = get_best_factory(product_id, customer_lat, customer_lon, priority)
#
#     if result:
#         return JsonResponse(result)
#     return JsonResponse({"error": "Product not found"}, status=404)
#
#
# # 2. Simulation functionality
# def simulation_api(request, product_id):
#     """
#     Predicts performance across all factories using the best-performing ML model.
#     """
#     try:
#         engine = SimulationEngine()
#         data = engine.simulate_reassignment(product_id)
#         return JsonResponse(data)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
#
#
# # 3. NEW: Clustering API (Requirement: Route & Product Clustering)
# def clustering_api(request):
#     """
#     Identifies consistently slow routes using K-Means clustering.
#     """
#     try:
#         service = ClusteringService()
#         clusters = service.cluster_routes()
#         return JsonResponse({"clusters": clusters})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
#
#
# # 4. Dashboard View
# def dashboard(request):
#     return render(request, 'optimization/dashboard.html')
from django.http import JsonResponse
from django.shortcuts import render
from .models import Factory, Product  # Import models to fetch data
from .services.recommender import get_best_factory
from .services.simulation import SimulationEngine
from .services.clustering_service import ClusteringService

# --- NEW: Master Data API (To meet requirement documentation) ---

def factory_list_api(request):
    """
    Returns the dynamic list of factories and their coordinates from the database.
    """
    factories = list(Factory.objects.values('name', 'latitude', 'longitude'))
    return JsonResponse(factories, safe=False)

def product_correlation_api(request):
    """
    Returns the current product-to-factory assignments (Legacy Rules).
    """
    # Fetching relevant fields to show the "Ground Truth" correlation
    correlations = list(Product.objects.select_related('current_factory').values(
        'division', 'name', 'current_factory__name'
    ))
    return JsonResponse(correlations, safe=False)


# --- RETAINED: Existing Functionality ---

def recommendation_api(request):
    product_id = request.GET.get('product_id', 1)
    customer_lat = float(request.GET.get('lat', 40.7128))
    customer_lon = float(request.GET.get('lon', -74.0060))
    priority = float(request.GET.get('priority', 0.5))

    result = get_best_factory(product_id, customer_lat, customer_lon, priority)

    if result:
        return JsonResponse(result)
    return JsonResponse({"error": "Product not found"}, status=404)


def simulation_api(request, product_id):
    try:
        engine = SimulationEngine()
        data = engine.simulate_reassignment(product_id)
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def clustering_api(request):
    try:
        service = ClusteringService()
        clusters = service.cluster_routes()
        return JsonResponse({"clusters": clusters})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def dashboard(request):
    return render(request, 'optimization/dashboard.html')