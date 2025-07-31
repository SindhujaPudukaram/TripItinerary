from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from math import radians, sin, cos, sqrt, atan2
from kmeans_clustering import TravelAgglomerative
import os
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans, AgglomerativeClustering, SpectralClustering, DBSCAN
import matplotlib.pyplot as plt

print("Current working directory:", os.getcwd())
print("Files in current directory:", os.listdir())

app = Flask(__name__)

# Load attractions data
def load_attractions():
    try:
        df = pd.read_csv('attractions.csv')
        return df.to_dict('records')
    except Exception as e:
        print(f"Error loading attractions: {e}")
        return []

# Travel planner class
class SouthIndiaTravelPlanner:
    def __init__(self):
        self.attractions = load_attractions()
        self.south_indian_states = [
            'Kerala',
            'Tamil Nadu',
            'Karnataka',
            'Andhra Pradesh',
            'Telangana',
            'Goa',
            'Puducherry'
        ]
        # Common variations and misspellings
        self.location_variations = {
            # Karnataka
            'bangalore': ['bangalore', 'bengaluru', 'bengalore', 'bangaluru', 'bengalooru', 'bangalooru', 'bengaloor', 'bangaloor'],
            'mysore': ['mysuru', 'mysore', 'mysur'],
            'hampi': ['hampi', 'hampe', 'hampi ruins', 'hampi temple'],
            'gokarna': ['gokarna', 'gokarn', 'gokarna beach', 'gokarna temple'],
            'mangalore': ['mangaluru', 'mangalore', 'mangalooru', 'mangaloor'],
            'hubli': ['hubballi', 'hubli', 'dharwad'],
            'belgaum': ['belagavi', 'belgaum', 'belagav'],
            'gulbarga': ['kalaburagi', 'gulbarga', 'kalburgi'],
            'bidar': ['bidar', 'bidar fort'],
            'bijapur': ['vijayapura', 'bijapur', 'bijapur fort'],
            
            # Telangana
            'hyderabad': ['hyd', 'hyderabad', 'bhagyanagar', 'hyderabad city'],
            'warangal': ['warangal', 'orugallu', 'ekasila nagaram'],
            'karimnagar': ['karimnagar', 'elagandula'],
            'nizamabad': ['nizamabad', 'induru'],
            'adilabad': ['adilabad', 'edlabad'],
            'khammam': ['khammam', 'stambhadri'],
            'medak': ['medak', 'methuku'],
            'nalgonda': ['nalgonda', 'nilagiri'],
            'rangareddy': ['rangareddy', 'ranga reddy'],
            'siddipet': ['siddipet', 'siddipeta'],
            
            # Andhra Pradesh
            'visakhapatnam': ['vizag', 'visakhapatnam', 'waltair', 'vizag city'],
            'vijayawada': ['vijayawada', 'bezawada', 'vijayawada city'],
            'tirupati': ['tirupati', 'tirupathi', 'tirupati temple'],
            'guntur': ['guntur', 'garthapuri'],
            'nellore': ['nellore', 'neluru'],
            'kurnool': ['kurnool', 'kandanavolu'],
            'anantapur': ['anantapur', 'anantapuram'],
            'kadapa': ['kadapa', 'cuddapah'],
            'chittoor': ['chittoor', 'chittur'],
            'srikakulam': ['srikakulam', 'chicacole'],
            
            # Tamil Nadu
            'chennai': ['madras', 'chennai', 'chennai city'],
            'madurai': ['madurai', 'madura', 'madurai city'],
            'coimbatore': ['coimbatore', 'kovai', 'coimbatore city'],
            'salem': ['salem', 'sale'],
            'tiruchirappalli': ['trichy', 'tiruchirappalli', 'trichinopoly'],
            'thanjavur': ['tanjore', 'thanjavur'],
            'tirunelveli': ['tirunelveli', 'nelveli'],
            'tuticorin': ['thoothukudi', 'tuticorin'],
            'vellore': ['vellore', 'velur'],
            'dindigul': ['dindigul', 'dindukal'],
            
            # Kerala
            'thiruvananthapuram': ['trivandrum', 'thiruvananthapuram', 'tvm'],
            'kochi': ['cochin', 'kochi', 'ernakulam', 'kochi city'],
            'kozhikode': ['calicut', 'kozhikode', 'calicut city'],
            'thrissur': ['trichur', 'thrissur'],
            'kollam': ['quilon', 'kollam'],
            'kannur': ['cannanore', 'kannur'],
            'alappuzha': ['alleppey', 'alappuzha'],
            'palakkad': ['palghat', 'palakkad'],
            'malappuram': ['malappuram', 'malapuram'],
            'wayanad': ['wayanad', 'waynad'],
            
            # Goa
            'panaji': ['panjim', 'panaji', 'panaji city'],
            'margao': ['madgaon', 'margao'],
            'vasco': ['vasco da gama', 'vasco'],
            'mapusa': ['mapusa', 'mapuca'],
            'ponda': ['ponda', 'farmagudi'],
            
            # Puducherry
            'puducherry': ['pondicherry', 'pondy', 'puducherry', 'puducherry city'],
            'karaikal': ['karaikal', 'karikal'],
            'mahe': ['mahe', 'mayyazhi'],
            'yanam': ['yanam', 'yanam'],
            
            # Hill Stations
            'ooty': ['udhagamandalam', 'ooty', 'ooty hill station'],
            'kodaikanal': ['kodaikanal', 'kodai', 'kodaikanal hill station'],
            'munnar': ['munnar', 'munar', 'munnar hill station'],
            'yercaud': ['yercaud', 'yerkaud'],
            'coonoor': ['coonoor', 'kunur'],
            'valparai': ['valparai', 'valparai hills'],
            'kolli hills': ['kolli hills', 'kollimalai'],
            'br hills': ['br hills', 'biligiriranga hills'],
            'nandi hills': ['nandi hills', 'nandidurga'],
            'skandagiri': ['skandagiri', 'kalavara durga'],
            
            # Beaches
            'kovalam': ['kovalam', 'kovalam beach'],
            'varkala': ['varkala', 'varkala cliff'],
            'marina': ['marina beach', 'marina'],
            'gokarna': ['gokarna beach', 'gokarna'],
            'palolem': ['palolem', 'palolem beach'],
            'baga': ['baga beach', 'baga'],
            'calangute': ['calangute beach', 'calangute'],
            'anjuna': ['anjuna beach', 'anjuna'],
            'colva': ['colva beach', 'colva'],
            'paradise': ['paradise beach', 'paradise'],
            
            # Temples
            'tirupati': ['tirupati temple', 'tirupati'],
            'meenakshi': ['meenakshi temple', 'meenakshi'],
            'padmanabhaswamy': ['padmanabhaswamy temple', 'padmanabhaswamy'],
            'sabarimala': ['sabarimala temple', 'sabarimala'],
            'guruvayur': ['guruvayur temple', 'guruvayur'],
            'srirangam': ['srirangam temple', 'srirangam'],
            'tiruvannamalai': ['tiruvannamalai temple', 'tiruvannamalai'],
            'chidambaram': ['chidambaram temple', 'chidambaram'],
            'rameshwaram': ['rameshwaram temple', 'rameshwaram'],
            'kanyakumari': ['kanyakumari temple', 'kanyakumari']
        }

    def matches_location(self, attraction, location):
        location_lower = location.lower().strip()
        
        # Special handling for Tirupati
        if 'tirupati' in location_lower:
            if 'Andhra Pradesh' in attraction['State']:
                return True
        
        # Check if the location has known variations
        for key, variations in self.location_variations.items():
            if location_lower in variations:
                # If it matches any variation, check against all variations
                for var in variations:
                    if (var in attraction['City'].lower().strip() or 
                        var in attraction['State'].lower().strip() or 
                        var in attraction['Name'].lower().strip() or 
                        var in attraction['Category'].lower().strip()):
                        return True
                return False
        
        # If no variations found, do normal matching
        return (
            location_lower in attraction['City'].lower().strip() or
            location_lower in attraction['State'].lower().strip() or
            location_lower in attraction['Name'].lower().strip() or
            location_lower in attraction['Category'].lower().strip()
        )

    def calculate_travel_time(self, lat1, lon1, lat2, lon2):
        """Calculate estimated travel time between two points in minutes"""
        distance = self.calculate_distance(lat1, lon1, lat2, lon2)
        # Assuming average speed of 40 km/h in cities
        return int((distance / 40) * 60)

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points using Haversine formula"""
        R = 6371  # Earth's radius in kilometers

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c

        return distance

    def generate_itinerary(self, places, duration, start_date, max_hours):
        try:
            # Validate inputs
            if not places or not start_date or duration < 1 or duration > 7:
                return {'error': 'Please provide valid input for all fields.'}

            # Find matching attractions for each location
            location_attractions = {}
            for place in places:
                matching_attractions = [attr for attr in self.attractions 
                                     if self.matches_location(attr, place)]
                if not matching_attractions:
                    return {'error': f'No matching attractions found for: {place}'}
                location_attractions[place] = matching_attractions

            # Calculate maximum minutes for pure visit time
            max_visit_minutes_per_day = max_hours * 60

            # Create daily schedules
            daily_schedules = []
            used_attractions = set()

            # Calculate optimal travel sequence based on distances
            locations = list(location_attractions.keys())
            if len(locations) > 1:
                # Create distance matrix between locations
                distance_matrix = {}
                for loc1 in locations:
                    distance_matrix[loc1] = {}
                    for loc2 in locations:
                        if loc1 != loc2:
                            # Use the first attraction from each location as reference point
                            attr1 = location_attractions[loc1][0]
                            attr2 = location_attractions[loc2][0]
                            distance_matrix[loc1][loc2] = self.calculate_distance(
                                attr1['Latitude'], attr1['Longitude'],
                                attr2['Latitude'], attr2['Longitude']
                            )

                # Sort locations by proximity
                sorted_locations = []
                current = locations[0]
                remaining = set(locations[1:])
                sorted_locations.append(current)

                while remaining:
                    next_loc = min(remaining, 
                                 key=lambda x: distance_matrix[current][x])
                    sorted_locations.append(next_loc)
                    current = next_loc
                    remaining.remove(next_loc)
            else:
                sorted_locations = locations

            # Calculate days per location
            total_locations = len(sorted_locations)
            days_per_location = max(1, duration // total_locations)
            remaining_days = duration - (days_per_location * total_locations)

            current_day = 0
            for location in sorted_locations:
                attractions = location_attractions[location]
                
                # Use K-means clustering to group nearby attractions
                n_clusters = min(3, len(attractions))  # Use at most 3 clusters
                kmeans = TravelAgglomerative(n_clusters=n_clusters)
                attraction_clusters = kmeans.fit(attractions)
                
                # Calculate days for this location
                location_days = days_per_location
                if remaining_days > 0:
                    location_days += 1
                    remaining_days -= 1

                # Create daily schedules for this location
                for day in range(location_days):
                    if current_day >= duration:
                        break

                    final_attractions = []
                    current_visit_time = 0
                    last_location = None

                    # Try to fill the day with attractions from the same cluster
                    for cluster_idx, cluster in enumerate(attraction_clusters):
                        if not cluster:
                            continue

                        for attraction in cluster[:]:
                            if attraction['Name'] in used_attractions:
                                continue

                            visit_time = attraction.get('Estimated Visit Time (mins)', 0)
                            travel_time = 0
                            if last_location:
                                travel_time = self.calculate_travel_time(
                                    last_location['Latitude'], 
                                    last_location['Longitude'],
                                    attraction['Latitude'], 
                                    attraction['Longitude']
                                )

                            if current_visit_time + visit_time + travel_time <= max_visit_minutes_per_day:
                                # Add cluster information to attraction
                                attraction['cluster'] = cluster_idx
                                final_attractions.append(attraction)
                                current_visit_time += visit_time + travel_time
                                last_location = attraction
                                used_attractions.add(attraction['Name'])
                                cluster.remove(attraction)

                    if final_attractions:
                        # Calculate additional time
                        food_time = len(final_attractions) * 60  # 1 hour for food per attraction
                        total_time = current_visit_time + food_time

                        # Get cluster centers for map visualization (use mean lat/lon for each cluster)
                        cluster_info = []
                        for i, cluster in enumerate(attraction_clusters):
                            if cluster:
                                mean_lat = float(np.mean([a['Latitude'] for a in cluster]))
                                mean_lon = float(np.mean([a['Longitude'] for a in cluster]))
                                cluster_info.append({
                                    'lat': mean_lat,
                                    'lng': mean_lon,
                                    'cluster_id': i
                                })

                        # Create date for this day
                        start = datetime.strptime(start_date, '%Y-%m-%d')
                        current_date = start + timedelta(days=current_day)
                        date_str = current_date.strftime('%Y-%m-%d')

                        daily_schedules.append({
                            'day': current_day + 1,
                            'date': date_str,
                            'attractions': final_attractions,
                            'total_time': total_time,
                            'visit_time': current_visit_time,
                            'travel_time': current_visit_time - sum(a.get('Estimated Visit Time (mins)', 0) for a in final_attractions),
                            'food_time': food_time,
                            'last_location': {
                                'name': final_attractions[-1]['Name'],
                                'city': final_attractions[-1]['City'],
                                'state': final_attractions[-1]['State']
                            },
                            'map_data': {
                                'attractions': [{
                                    'name': attr['Name'],
                                    'lat': float(attr['Latitude']),
                                    'lng': float(attr['Longitude']),
                                    'cluster': attr['cluster'],
                                    'visit_time': attr.get('Estimated Visit Time (mins)', 0)
                                } for attr in final_attractions],
                                'cluster_centers': cluster_info
                            }
                        })
                        current_day += 1

            # After finding location_attractions
            all_attractions = []
            for place, attrs in location_attractions.items():
                all_attractions.extend(attrs)

            # Calculate silhouette scores for each location's clustering
            silhouette_scores = []
            location_names = []

            for location in sorted_locations:
                attractions = location_attractions[location]
                if len(attractions) < 2:
                    silhouette_scores.append(np.nan)
                    location_names.append(location)
                    continue
                n_clusters = min(2, len(attractions))  # Use at most 2 clusters
                kmeans = TravelAgglomerative(n_clusters=n_clusters)
                attraction_clusters = kmeans.fit(attractions)
                coordinates = np.array([[a['Latitude'], a['Longitude']] for a in attractions])
                labels = np.empty(len(attractions), dtype=int)
                idx = 0
                for cluster_idx, cluster in enumerate(attraction_clusters):
                    for _ in cluster:
                        labels[idx] = cluster_idx
                        idx += 1
                if len(set(labels)) > 1:
                    score = silhouette_score(coordinates, labels)
                else:
                    score = np.nan
                silhouette_scores.append(score)
                location_names.append(location)

            # Calculate silhouette score for the entire itinerary (all attractions together)
            all_attractions = []
            all_labels = []
            cluster_counter = 0
            for location in sorted_locations:
                attractions = location_attractions[location]
                if len(attractions) < 2:
                    continue
                n_clusters = min(2, len(attractions))
                kmeans = TravelAgglomerative(n_clusters=n_clusters)
                attraction_clusters = kmeans.fit(attractions)
                for cluster_idx, cluster in enumerate(attraction_clusters):
                    for attraction in cluster:
                        all_attractions.append(attraction)
                        all_labels.append(cluster_counter + cluster_idx)
                cluster_counter += n_clusters
            if len(set(all_labels)) > 1:
                coordinates = np.array([[a['Latitude'], a['Longitude']] for a in all_attractions])
                overall_score = silhouette_score(coordinates, all_labels)
            else:
                overall_score = np.nan
            # Plot the overall silhouette score as a bar chart
            plt.figure(figsize=(5, 5))
            plt.bar(['Itinerary'], [overall_score], color='#4E79A7')
            plt.ylabel('Silhouette Score', fontsize=13)
            plt.title('Silhouette Score for Entire Itinerary', fontsize=15)
            plt.ylim(0, 1)
            if not np.isnan(overall_score):
                plt.text(0, overall_score + 0.02, f'{overall_score:.2f}', ha='center', va='bottom', fontsize=12)
            else:
                plt.text(0, 0.02, 'N/A', ha='center', va='bottom', fontsize=12)
            plt.tight_layout()
            plt.savefig('silhouette_score_itinerary.png')
            plt.close()

            return {
                'itinerary': daily_schedules,
                'all_attractions': all_attractions
            }

        except Exception as e:
            return {'error': str(e)}

# Initialize travel planner
travel_planner = SouthIndiaTravelPlanner()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary():
    try:
        data = request.get_json()
        print("Received data:", data)  # Add this line
        places = [p.strip() for p in data['places'].split(';') if p.strip()]
        duration = int(data['duration'])
        start_date = data['startDate']
        max_hours = int(data['maxHours'])

        result = travel_planner.generate_itinerary(
            places, duration, start_date, max_hours
        )

        print("Result:", result)  # And this line
        return jsonify(result)

    except Exception as e:
        print("Error:", e)  # And this line
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)