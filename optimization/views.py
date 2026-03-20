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
from .models import Factory, Product, Order  # Import models to fetch data
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


# def simulation_api(request, product_id):
#     try:
#         engine = SimulationEngine()
#         data = engine.simulate_reassignment(product_id)
#         return JsonResponse(data)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
def simulation_api(request, product_id):
    # NEW: read optional region and ship_mode from query string
    region = request.GET.get('region', 'Interior')
    ship_mode = request.GET.get('ship_mode', 'Standard Class')
    try:
        engine = SimulationEngine()
        data = engine.simulate_reassignment(product_id, region, ship_mode)  # pass them
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

# --- NEW: Endpoints for dynamic filters and KPIs ---
def get_regions(request):
    """Return distinct regions from orders."""
    regions = Order.objects.values_list('region', flat=True).distinct()
    return JsonResponse(list(regions), safe=False)

def get_ship_modes(request):
    """Return distinct ship modes from orders."""
    ship_modes = Order.objects.values_list('ship_mode', flat=True).distinct()
    return JsonResponse(list(ship_modes), safe=False)

def coverage_kpi(request):
    """Calculate percentage of products with order data."""
    total_products = Product.objects.count()
    if total_products == 0:
        return JsonResponse({"coverage": 0})
    products_with_orders = Order.objects.values('product').distinct().count()
    coverage = (products_with_orders / total_products) * 100
    return JsonResponse({"coverage": round(coverage, 2)})