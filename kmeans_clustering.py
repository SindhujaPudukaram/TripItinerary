from sklearn.cluster import KMeans
import numpy as np
from math import radians, sin, cos, sqrt, atan2

class TravelKMeans:
    """
    A class that uses K-means clustering to group attractions based on their geographical coordinates.
    This helps in creating more efficient travel routes by grouping nearby attractions together.
    """
    
    def __init__(self, n_clusters):
        """
        Initialize the TravelKMeans class.
        
        Args:
            n_clusters (int): Number of clusters to create
        """
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)

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
        Fit the K-means model to the attractions data and group them into clusters.
        
        Args:
            attractions (list): List of attraction dictionaries containing 'Latitude' and 'Longitude'
            
        Returns:
            list: List of clusters, where each cluster is a list of attractions
        """
        if not attractions:
            return []

        # Extract coordinates
        coordinates = np.array([[a['Latitude'], a['Longitude']] for a in attractions])
        
        # Fit k-means
        self.kmeans.fit(coordinates)
        
        # Group attractions by cluster
        clusters = [[] for _ in range(self.n_clusters)]
        for i, label in enumerate(self.kmeans.labels_):
            clusters[label].append(attractions[i])
        
        # Sort attractions within each cluster by distance from cluster center
        for i, cluster in enumerate(clusters):
            if cluster:
                center = self.kmeans.cluster_centers_[i]
                cluster.sort(key=lambda x: self.calculate_distance(
                    x['Latitude'], x['Longitude'],
                    center[0], center[1]
                ))
        
        return clusters

    def get_cluster_centers(self):
        """
        Get the coordinates of cluster centers.
        
        Returns:
            numpy.ndarray: Array of cluster center coordinates
        """
        return self.kmeans.cluster_centers_

    def predict_cluster(self, lat, lon):
        """
        Predict which cluster a new location belongs to.
        
        Args:
            lat (float): Latitude of the location
            lon (float): Longitude of the location
            
        Returns:
            int: Cluster label
        """
        return self.kmeans.predict([[lat, lon]])[0] 