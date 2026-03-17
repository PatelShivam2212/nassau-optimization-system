import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from optimization.models import Order


class ClusteringService:
    def cluster_routes(self):
        # 1. Fetch data
        orders = Order.objects.all().values('region', 'order_date', 'ship_date')
        df = pd.DataFrame(list(orders))

        if df.empty:
            return None

        # 2. Requirement: Calculate Lead Time
        df['order_date'] = pd.to_datetime(df['order_date'])
        df['ship_date'] = pd.to_datetime(df['ship_date'])
        df['lead_time'] = (df['ship_date'] - df['order_date']).dt.days

        # 3. Requirement: Remove extreme outliers (using 3 Standard Deviations)
        # This ensures 'Slow' clusters are actually slow, not just errors
        mean_lt = df['lead_time'].mean()
        std_lt = df['lead_time'].std()
        df = df[(df['lead_time'] <= mean_lt + (3 * std_lt)) & (df['lead_time'] >= 0)]

        # 4. Prepare data for K-Means (Grouping by region)
        route_stats = df.groupby('region')['lead_time'].agg(['mean', 'std', 'count']).fillna(0)

        # 5. Apply K-Means (Requirement: Identify performance similarity)
        # We use 'mean' to cluster the performance
        n_clusters = min(3, len(route_stats))
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        route_stats['cluster_id'] = kmeans.fit_predict(route_stats[['mean']])

        # 6. Requirement: Identify "Consistently slow routes"
        # We map cluster IDs to human-readable performance labels
        # We sort by mean lead time: lowest = Fast, highest = Slow
        sorted_clusters = route_stats.sort_values('mean').index

        label_map = {}
        labels = ["Fast/Efficient", "Normal", "Slow/High Risk"]

        # Assign labels based on the sorted order of the means
        for i, region in enumerate(sorted_clusters):
            label_map[region] = labels[min(i, 2)]

        # Final dictionary structure for the frontend
        results = []
        for region, row in route_stats.iterrows():
            results.append({
                "region": region,
                "avg_lead_time": round(row['mean'], 1),
                "stability": "Consistent" if row['std'] < 2 else "Volatile",
                "performance_label": label_map[region],
                "order_volume": int(row['count'])
            })

        return results