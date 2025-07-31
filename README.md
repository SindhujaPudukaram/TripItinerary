# 🌍 Travel Itinerary Planner – Smart Trip Optimization

> **Plan Smarter. Travel Better.**  
> A Machine Learning-powered travel itinerary generator that creates **optimized, cost-effective, and time-efficient multi-day trip plans** with **interactive map visualization**.  

![Python](https://img.shields.io/badge/Python-3.9-blue) 
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Enabled-green)
![Flask](https://img.shields.io/badge/Backend-Flask-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

- 🧠 **ML-Powered Planning:** Uses **K-Means clustering** & **distance-based optimization** to assign attractions to each day.  
- 🗺️ **Smart Scheduling:** Generates **day-wise itineraries** considering visit time, travel time, and food breaks.  
- 🔎 **Flexible Input:** Accepts **cities, states, or attractions** as input.  
- 📍 **Map Visualization:** Plots routes using **Leaflet interactive maps**.  
- ⚡ **Scalable & Lightweight:** Can adapt for **pan-India** or multi-country planning.  

---

## 🏗️ Tech Stack

**Backend:** Python (Flask)  
**ML & Data:** Pandas, Scikit-learn, NLP for place matching  
**Visualization:** Leaflet  
**Database:** CSV (POI dataset for South India)  
**Frontend:** HTML, CSS, JS (Optional integration for web interface)  

---

## 📊 How It Works

1. **Input:** User selects one or multiple places + number of days + maximum hours +  start date.  
2. **Data Processing:**  
   - NLP maps input to **tourist locations** in the dataset.  
   - **Clustering algorithm** groups attractions by proximity.  
3. **Schedule Generation:**  
   - Routes are **optimized for distance and time**.  
   - Day-wise itinerary is generated with **visit timings**.  
4. **Visualization:** Final itinerary is shown **with route map**.  

---

## 🚀 Demo (Sample Output)

```text
Day 1: Charminar → Chowmahalla Palace → Hussain Sagar
Day 2: Golconda Fort → Salar Jung Museum → Birla Mandir
