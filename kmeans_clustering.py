from sklearn.cluster import AgglomerativeClustering
import numpy as np
from math import radians, sin, cos, sqrt, atan2

class TravelAgglomerative:
    """
    A class that uses Agglomerative (Hierarchical) clustering to group attractions based on their geographical coordinates.
    This helps in creating more efficient travel routes by grouping nearby attractions together.
    """
    
    def __init__(self, n_clusters):
        """
        Initialize the TravelAgglomerative class.
        Args:
            n_clusters (int): Number of clusters to create
        """
        self.n_clusters = n_clusters
        self.agg = AgglomerativeClustering(n_clusters=n_clusters)

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate distance between two points using Haversine formula.
        Args:
            lat1 (float): Latitude of first point
            lon1 (float): Longitude of first point
            lat2 (float): Latitude of second point
            lon2 (float): Longitude of second point
        Returns:
            float: Distance in kilometers
        """
        R = 6371  # Earth's radius in kilometers
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        return distance

    def fit(self, attractions):
        """
        Fit the Agglomerative model to the attractions data and group them into clusters.
        Args:
            attractions (list): List of attraction dictionaries containing 'Latitude' and 'Longitude'
        Returns:
            list: List of clusters, where each cluster is a list of attractions
        """
        if not attractions:
            return []
        # Extract coordinates
        coordinates = np.array([[a['Latitude'], a['Longitude']] for a in attractions])
        # Fit Agglomerative
        labels = self.agg.fit_predict(coordinates)
        # Group attractions by cluster
        clusters = [[] for _ in range(self.n_clusters)]
        for i, label in enumerate(labels):
            clusters[label].append(attractions[i])
        # Sort attractions within each cluster by distance from the cluster's mean point
        for i, cluster in enumerate(clusters):
            if cluster:
                # Calculate mean point for the cluster
                mean_lat = np.mean([a['Latitude'] for a in cluster])
                mean_lon = np.mean([a['Longitude'] for a in cluster])
                cluster.sort(key=lambda x: self.calculate_distance(
                    x['Latitude'], x['Longitude'],
                    mean_lat, mean_lon
                ))
        return clusters 