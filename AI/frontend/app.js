const API_BASE_URL = 'http://localhost:8000';

let map;
let markers = [];
let routeLine = null;

// Initialize map
function initMap() {
    map = L.map('map').setView([19.9105, 99.8406], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
}

// Load themes
async function loadThemes() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/themes`);
        const data = await response.json();

        const themeSelect = document.getElementById('theme');
        themeSelect.innerHTML = '';

        data.themes.forEach(theme => {
            const option = document.createElement('option');
            option.value = theme.id;
            option.textContent = `${theme.icon} ${theme.name} - ${theme.name_th}`;
            themeSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading themes:', error);
        alert('Failed to load themes. Make sure the API server is running.');
    }
}

// Toggle mode
document.getElementById('mode').addEventListener('change', (e) => {
    const mode = e.target.value;
    const themeGroup = document.getElementById('theme-group');
    const placeGroup = document.getElementById('place-group');

    if (mode === 'theme') {
        themeGroup.style.display = 'block';
        placeGroup.style.display = 'none';
    } else {
        themeGroup.style.display = 'none';
        placeGroup.style.display = 'block';
    }
});

// Plan trip
document.getElementById('plan-btn').addEventListener('click', async () => {
    const startLat = parseFloat(document.getElementById('start_lat').value);
    const startLng = parseFloat(document.getElementById('start_lng').value);
    const mode = document.getElementById('mode').value;
    const numStops = parseInt(document.getElementById('num_stops').value);
    const maxDistance = parseFloat(document.getElementById('max_distance').value);

    let value;
    if (mode === 'theme') {
        value = document.getElementById('theme').value;
    } else {
        value = document.getElementById('place_name').value;
    }

    if (!value) {
        alert('Please select a theme or enter a place name');
        return;
    }

    const requestData = {
        start_lat: startLat,
        start_lng: startLng,
        mode: mode,
        value: value,
        num_stops: numStops,
        max_distance_km: maxDistance
    };

    // Show loading
    document.getElementById('plan-btn').disabled = true;
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';

    try {
        const response = await fetch(`${API_BASE_URL}/api/plan-trip`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to plan trip');
        }

        const tripData = await response.json();
        displayResults(tripData);
        displayRouteOnMap(tripData, startLat, startLng);

    } catch (error) {
        console.error('Error planning trip:', error);
        alert(`Error: ${error.message}`);
    } finally {
        document.getElementById('plan-btn').disabled = false;
        document.getElementById('loading').style.display = 'none';
    }
});

// Display results
function displayResults(tripData) {
    const resultsDiv = document.getElementById('results');
    const summaryDiv = document.getElementById('summary');

    const summary = tripData.summary;

    // Build narrative HTML (convert markdown-like to HTML)
    let narrativeHtml = '';
    if (summary.narrative) {
        narrativeHtml = `
            <div class="narrative-summary" style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 12px;
                margin-bottom: 20px;
                white-space: pre-line;
                font-family: 'Sarabun', 'Noto Sans Thai', sans-serif;
                line-height: 1.8;
            ">
                ${summary.narrative.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}
            </div>
        `;
    }

    summaryDiv.innerHTML = `
        ${narrativeHtml}
        <div class="summary-item">
            <span class="summary-label">Total Stops</span>
            <span class="summary-value">${summary.total_stops}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Total Distance</span>
            <span class="summary-value">${summary.total_distance_km} km</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Estimated Time</span>
            <span class="summary-value">${summary.estimated_time_hours} hrs</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Total Carbon</span>
            <span class="summary-value">${summary.total_carbon_kg} kg CO2</span>
        </div>
        <div class="eco-score">
            <h4>Eco Score</h4>
            <div class="score">${summary.eco_score}/10</div>
            <p style="margin-top: 5px; font-size: 0.9rem;">
                ${summary.carbon_reduction_percent}% Carbon Reduction
            </p>
        </div>
    `;

    resultsDiv.style.display = 'block';
}

// Display route on map
function displayRouteOnMap(tripData, startLat, startLng) {
    // Clear existing markers and route
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];
    if (routeLine) {
        map.removeLayer(routeLine);
    }

    // Add start marker
    const startMarker = L.marker([startLat, startLng], {
        icon: L.divIcon({
            className: 'start-marker',
            html: '<div style="background: #667eea; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">S</div>'
        })
    }).addTo(map);
    startMarker.bindPopup('<b>Start Location</b>');
    markers.push(startMarker);

    // Add route markers
    const coordinates = [[startLat, startLng]];
    const routeListDiv = document.getElementById('route-list');
    routeListDiv.innerHTML = '<h3>Route Details</h3>';

    tripData.route.forEach((place, index) => {
        coordinates.push([place.lat, place.lng]);

        // Add marker
        const marker = L.marker([place.lat, place.lng], {
            icon: L.divIcon({
                className: 'route-marker',
                html: `<div style="background: #764ba2; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">${place.stop_number}</div>`
            })
        }).addTo(map);

        marker.bindPopup(`
            <b>${place.name}</b><br>
            ${place.keyword}<br>
            Rating: ${place.rating}/5<br>
            Distance: ${place.distance_from_prev_km} km<br>
            Carbon: ${place.carbon_kg} kg CO2
        `);

        markers.push(marker);

        // Add to route list
        const routeItem = document.createElement('div');
        routeItem.className = 'route-item';

        // Build photos HTML with placeholders
        let photosHTML = '';
        if (place.photos && place.photos.length > 0) {
            photosHTML = '<div class="place-photos">';
            place.photos.slice(0, 3).forEach((photo, idx) => {
                // Use placeholder if photo path is invalid or not a full URL
                const photoUrl = photo && (photo.startsWith('http://') || photo.startsWith('https://'))
                    ? photo
                    : `https://via.placeholder.com/400x300/667eea/ffffff?text=${encodeURIComponent(place.keyword || 'Place')}`;

                photosHTML += `<img src="${photoUrl}" alt="${place.name}" class="place-photo" onerror="this.src='https://via.placeholder.com/400x300/667eea/ffffff?text=No+Image'">`;
            });
            photosHTML += '</div>';
        } else {
            // Show single placeholder if no photos
            photosHTML = `
                <div class="place-photos single">
                    <img src="https://via.placeholder.com/400x300/667eea/ffffff?text=${encodeURIComponent(place.keyword || 'Place')}"
                         alt="${place.name}"
                         class="place-photo">
                </div>
            `;
        }

        routeItem.innerHTML = `
            <h4>
                <span class="badge">${place.stop_number}</span>
                ${place.name}
            </h4>
            ${photosHTML}
            <p><strong>Keyword:</strong> ${place.keyword}</p>
            <p><strong>Rating:</strong> ⭐ ${place.rating}/5 (${place.user_ratings_total} reviews)</p>
            <p><strong>Distance from previous:</strong> ${place.distance_from_prev_km} km</p>
            <p><strong>Total distance from start:</strong> ${place.distance_from_start_km} km</p>
            ${place.phone ? `<p><strong>Phone:</strong> ${place.phone}</p>` : ''}
            <div class="carbon-info">
                🌱 Carbon: <span>${place.carbon_kg} kg CO2</span>
            </div>
        `;
        routeListDiv.appendChild(routeItem);
    });

    // Draw route line
    routeLine = L.polyline(coordinates, {
        color: '#764ba2',
        weight: 4,
        opacity: 0.7
    }).addTo(map);

    // Fit map to route
    map.fitBounds(routeLine.getBounds(), { padding: [50, 50] });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initMap();
    loadThemes();
});
