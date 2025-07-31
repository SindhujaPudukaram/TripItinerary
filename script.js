document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('travelForm');
    const resultDiv = document.getElementById('result');

    // Set minimum date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('startDate').min = today;

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = {
            places: document.getElementById('places').value,
            startDate: document.getElementById('startDate').value,
            duration: document.getElementById('duration').value,
            maxHours: document.getElementById('maxHours').value
        };

        // Show loading state
        const submitBtn = form.querySelector('button[type="submit"]');
        const btnText = submitBtn.querySelector('.btn-text');
        const btnLoading = submitBtn.querySelector('.btn-loading');
        
        // Add loading class and show loading state
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;

        try {
            const response = await fetch('/generate_itinerary', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            if (data.error) {
                showError(data.error);
                return;
            }
            displayItinerary(data.itinerary);
            showSuccess('Your itinerary has been generated successfully!');
        } catch (error) {
            console.error('Error:', error);
            showError('An error occurred while generating the itinerary. Please try again.');
        } finally {
            // Reset button state
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }
    });
});

function getDayColor(dayIndex) {
    const colors = [
        '#FF5252', // Red
        '#4CAF50', // Green
        '#2196F3', // Blue
        '#FFC107', // Amber
        '#9C27B0', // Purple
        '#FF9800', // Orange
        '#795548'  // Brown
    ];
    return colors[dayIndex % colors.length];
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    return date.toLocaleDateString('en-US', options);
}

function displayItinerary(itinerary) {
    const resultSection = document.getElementById('result');
    const container = document.getElementById('itinerary');
    
    resultSection.classList.remove('hidden');
    container.innerHTML = '';

    // Add summary header with proper styling
    const summaryDiv = document.createElement('div');
    summaryDiv.className = 'itinerary-summary';
    summaryDiv.innerHTML = `
        <h2>Your ${itinerary.length}-Day South India Adventure</h2>
        <p>Journey crafted for ${itinerary.length} unforgettable day${itinerary.length > 1 ? 's' : ''} starting from ${formatDate(itinerary[0].date)}</p>
    `;
    container.appendChild(summaryDiv);

    itinerary.forEach((day, dayIndex) => {
        // Create day container
        const dayDiv = document.createElement('div');
        dayDiv.className = 'day-container';
        
        // Create map container for this day
        const mapId = `map-day-${dayIndex}`;
        const mapDiv = document.createElement('div');
        mapDiv.id = mapId;
        mapDiv.className = 'day-map';
        
        // Add day content with proper structure
        dayDiv.innerHTML = `
            <div class="day-header">
                <h3><i class="fas fa-calendar-day"></i> Day ${day.day} - ${formatDate(day.date)}</h3>
                <div class="day-info">
                    <div class="attraction-count">
                        <i class="fas fa-map-marked-alt"></i>
                        ${day.attractions.length} attraction${day.attractions.length > 1 ? 's' : ''}
                    </div>
                    <div class="total-time">
                        <i class="fas fa-clock"></i>
                        ${Math.floor(day.total_time / 60)}h ${day.total_time % 60}m total
                    </div>
                </div>
            </div>
            <div class="attractions-list">
                ${day.attractions.map((a, index) => `
                    <div class="attraction">
                        <div class="attraction-header">
                            <div class="attraction-number">${index + 1}</div>
                            <div class="attraction-main">
                                <div class="attraction-name">${a.Name}</div>
                                <div class="attraction-details">
                                    <span><i class="fas fa-location-dot"></i> ${a.City}, ${a.State}</span>
                                    <span><i class="fas fa-tag"></i> ${a.Category}</span>
                                    <span><i class="fas fa-star"></i> ${a.Rating}</span>
                                    <span><i class="fas fa-clock"></i> ${a["Estimated Visit Time (mins)"]} mins</span>
                                </div>
                            </div>
                        </div>
                        ${a.Description ? `<div class="attraction-description">${a.Description}</div>` : ''}
                        ${index < day.attractions.length - 1 ? 
                            '<div class="travel-time"><i class="fas fa-car"></i> Travel time to next attraction included</div>' : ''}
                        <div class="food-time"><i class="fas fa-utensils"></i> 60 mins allocated for food & rest</div>
                    </div>
                `).join('')}
            </div>
            <div class="time-summary">
                <div class="time-row">
                    <strong><i class="fas fa-chart-pie"></i> Time Breakdown:</strong>
                </div>
                <div class="time-breakdown">
                    <div class="time-item">
                        <i class="fas fa-eye"></i>
                        Sightseeing: ${Math.floor(day.visit_time / 60)}h ${day.visit_time % 60}m
                    </div>
                    <div class="time-item">
                        <i class="fas fa-route"></i>
                        Travel: ${Math.floor(day.travel_time / 60)}h ${day.travel_time % 60}m
                    </div>
                    <div class="time-item">
                        <i class="fas fa-coffee"></i>
                        Food & Rest: ${Math.floor(day.food_time / 60)}h ${day.food_time % 60}m
                    </div>
                </div>
            </div>
        `;

        // Insert map div after the day header
        const dayHeader = dayDiv.querySelector('.day-header');
        dayHeader.after(mapDiv);
        container.appendChild(dayDiv);

        // Initialize map for this day
        const dayMap = L.map(mapId, {
            center: [12.9716, 77.5946],
            zoom: 6
        });

        // Add tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(dayMap);

        // Add markers for this day's attractions
        const color = getDayColor(dayIndex);
        const markers = [];

        day.attractions.forEach((attraction, index) => {
            // Create marker
            const marker = L.circleMarker([attraction.Latitude, attraction.Longitude], {
                radius: 10,
                fillColor: color,
                color: 'white',
                weight: 3,
                opacity: 1,
                fillOpacity: 0.9
            }).addTo(dayMap);

            // Add number label
            const label = L.marker([attraction.Latitude, attraction.Longitude], {
                icon: L.divIcon({
                    className: 'number-label',
                    html: `<div style="background: linear-gradient(135deg, ${color} 0%, ${color}dd 100%); width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px; border: 2px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">${index + 1}</div>`,
                    iconSize: [28, 28]
                })
            }).addTo(dayMap);

            // Add popup with enhanced styling
            const popupContent = `
                <div class="map-info-window">
                    <h3>${attraction.Name}</h3>
                    <p><i class="fas fa-location-dot"></i> ${attraction.City}, ${attraction.State}</p>
                    <p><i class="fas fa-tag"></i> ${attraction.Category} | <i class="fas fa-star"></i> ${attraction.Rating}</p>
                    <p><i class="fas fa-clock"></i> ${attraction["Estimated Visit Time (mins)"]} minutes</p>
                    ${attraction.Description ? `<p class="description">${attraction.Description}</p>` : ''}
                </div>
            `;
            marker.bindPopup(popupContent);
            label.bindPopup(popupContent);

            markers.push(marker, label);
        });

        // Draw lines between attractions with enhanced styling
        if (day.attractions.length > 1) {
            const points = day.attractions.map(a => [a.Latitude, a.Longitude]);
            const line = L.polyline(points, {
                color: color,
                weight: 4,
                opacity: 0.8,
                dashArray: '12, 8',
                lineJoin: 'round',
                lineCap: 'round'
            }).addTo(dayMap);
            markers.push(line);

            // Add directional arrows with improved styling
            for (let i = 0; i < points.length - 1; i++) {
                const start = points[i];
                const end = points[i + 1];
                const midPoint = [
                    (start[0] + end[0]) / 2,
                    (start[1] + end[1]) / 2
                ];

                // Calculate angle for arrow rotation
                const angle = Math.atan2(end[1] - start[1], end[0] - start[0]) * 180 / Math.PI;

                const arrow = L.marker(midPoint, {
                    icon: L.divIcon({
                        className: 'route-arrow',
                        html: `<div style="color: ${color}; font-size: 20px; font-weight: bold; transform: rotate(${angle}deg); text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">→</div>`,
                        iconSize: [24, 24]
                    })
                }).addTo(dayMap);
                
                markers.push(arrow);
            }
        }

        // Fit map to show all markers with proper padding
        if (markers.length > 0) {
            const group = new L.featureGroup(markers.filter(m => m instanceof L.CircleMarker || m instanceof L.Marker));
            if (group.getLayers().length > 0) {
                dayMap.fitBounds(group.getBounds().pad(0.15));
            }
        }

        // Ensure map renders properly
        setTimeout(() => {
            dayMap.invalidateSize();
        }, 150);
    });

    // Smooth scroll to results
    resultSection.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
}

// Enhanced utility functions
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(errorDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => {
                if (errorDiv.parentNode) {
                    document.body.removeChild(errorDiv);
                }
            }, 300);
        }
    }, 5000);
}

function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(successDiv);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (successDiv.parentNode) {
            successDiv.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => {
                if (successDiv.parentNode) {
                    document.body.removeChild(successDiv);
                }
            }, 300);
        }
    }, 3000);
}

// Scroll to top function for FAB
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Add smooth scroll behavior to FAB when results are visible
window.addEventListener('scroll', function() {
    const fab = document.querySelector('.fab');
    const resultSection = document.getElementById('result');
    
    if (fab && !resultSection.classList.contains('hidden')) {
        if (window.scrollY > 300) {
            fab.style.opacity = '1';
            fab.style.transform = 'scale(1)';
        } else {
            fab.style.opacity = '0.7';
            fab.style.transform = 'scale(0.9)';
        }
    }
});

// Enhanced form interactions
document.addEventListener('DOMContentLoaded', function() {
    // Add focus effects to inputs
    const inputs = document.querySelectorAll('input[type="text"], input[type="date"], input[type="number"]');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
    
    // Add hover effects to form groups
    const formGroups = document.querySelectorAll('.form-group');
    formGroups.forEach(group => {
        group.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        group.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});