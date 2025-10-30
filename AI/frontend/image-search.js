const API_BASE_URL = 'http://localhost:8000';

let map;
let markers = [];
let routeLine = null;
let uploadedImage = null;
let selectedPlaces = new Set();
let similarPlacesData = [];

// Initialize map
function initMap() {
    map = L.map('map').setView([19.9105, 99.8406], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
}

// Handle file upload
const uploadZone = document.getElementById('upload-zone');
const fileInput = document.getElementById('file-input');
const previewContainer = document.getElementById('preview-container');
const previewImage = document.getElementById('preview-image');

uploadZone.addEventListener('click', () => fileInput.click());

uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.classList.add('dragover');
});

uploadZone.addEventListener('dragleave', () => {
    uploadZone.classList.remove('dragover');
});

uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('dragover');

    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        handleImageUpload(file);
    }
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleImageUpload(file);
    }
});

function handleImageUpload(file) {
    uploadedImage = file;

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewContainer.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

// Search for similar places
document.getElementById('search-btn').addEventListener('click', async () => {
    if (!uploadedImage) {
        alert('Please upload an image first');
        return;
    }

    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('similar-places').style.display = 'none';
    document.getElementById('search-btn').disabled = true;

    try {
        // Create FormData
        const formData = new FormData();
        formData.append('image', uploadedImage);
        formData.append('top_k', 5);

        // Call image search API
        const response = await fetch(`${API_BASE_URL}/api/image-search`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to search for similar places');
        }

        const data = await response.json();
        similarPlacesData = data.results;
        displaySimilarPlaces(data.results);

    } catch (error) {
        console.error('Error searching:', error);
        alert(`Error: ${error.message}`);
    } finally {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('search-btn').disabled = false;
    }
});

// Display similar places
function displaySimilarPlaces(places) {
    const listDiv = document.getElementById('similar-places-list');
    listDiv.innerHTML = '';

    places.forEach((place, index) => {
        const placeDiv = document.createElement('div');
        placeDiv.className = 'similar-place-item';
        placeDiv.dataset.index = index;

        // Get first photo or placeholder
        let photoUrl = 'https://via.placeholder.com/100x100/667eea/ffffff?text=' +
                       encodeURIComponent(place.keyword || 'Place');

        if (place.photos && place.photos.length > 0) {
            const firstPhoto = place.photos[0];
            if (firstPhoto && (firstPhoto.startsWith('http://') || firstPhoto.startsWith('https://'))) {
                photoUrl = firstPhoto;
            }
        }

        placeDiv.innerHTML = `
            <img src="${photoUrl}"
                 alt="${place.name}"
                 class="similar-place-thumb"
                 onerror="this.src='https://via.placeholder.com/100x100/667eea/ffffff?text=No+Image'">
            <div class="similar-place-info">
                <h4>${place.name}</h4>
                <p style="color: #666; margin: 4px 0;">${place.keyword}</p>
                <p style="color: #888; font-size: 0.9rem;">⭐ ${place.rating}/5 (${place.user_ratings_total} reviews)</p>
                <span class="similarity-score">${Math.round(place.similarity * 100)}% Match</span>
            </div>
        `;

        // Click to toggle selection
        placeDiv.addEventListener('click', () => {
            if (selectedPlaces.has(index)) {
                selectedPlaces.delete(index);
                placeDiv.classList.remove('selected');
            } else {
                selectedPlaces.add(index);
                placeDiv.classList.add('selected');
            }

            // Update selected summary
            updateSelectedSummary();

            // Enable/disable plan button
            document.getElementById('plan-trip-btn').disabled = selectedPlaces.size === 0;
        });

        listDiv.appendChild(placeDiv);
    });

    document.getElementById('similar-places').style.display = 'block';

    // Show places on map
    displayPlacesOnMap(places);
}

// Update selected places summary
function updateSelectedSummary() {
    const summaryDiv = document.getElementById('selected-summary');
    const countSpan = document.getElementById('selected-count');
    const listDiv = document.getElementById('selected-list');

    if (selectedPlaces.size === 0) {
        summaryDiv.style.display = 'none';
        return;
    }

    summaryDiv.style.display = 'block';
    countSpan.textContent = selectedPlaces.size;

    // Build list
    const selectedArray = Array.from(selectedPlaces).sort((a, b) => a - b);
    const listHTML = selectedArray.map((index, order) => {
        const place = similarPlacesData[index];
        return `
            <div style="padding: 8px; margin: 4px 0; background: white; border-radius: 6px; border-left: 3px solid #667eea;">
                <strong>${order + 1}. ${place.name}</strong> (${place.keyword})
                <div style="font-size: 0.85rem; color: #888; margin-top: 2px;">
                    ⭐ ${place.rating}/5 • ${Math.round(place.similarity * 100)}% Match
                </div>
            </div>
        `;
    }).join('');

    listDiv.innerHTML = listHTML;
}

// Display places on map
function displayPlacesOnMap(places) {
    // Clear existing markers
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];

    const bounds = [];

    places.forEach((place, index) => {
        const marker = L.marker([place.lat, place.lng], {
            icon: L.divIcon({
                className: 'place-marker',
                html: `<div style="background: #667eea; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">${index + 1}</div>`
            })
        }).addTo(map);

        marker.bindPopup(`
            <b>${place.name}</b><br>
            ${place.keyword}<br>
            Rating: ${place.rating}/5<br>
            Similarity: ${Math.round(place.similarity * 100)}%
        `);

        markers.push(marker);
        bounds.push([place.lat, place.lng]);
    });

    // Fit map to show all markers
    if (bounds.length > 0) {
        map.fitBounds(bounds, { padding: [50, 50] });
    }
}

// Plan trip with selected places
document.getElementById('plan-trip-btn').addEventListener('click', async () => {
    if (selectedPlaces.size === 0) {
        alert('Please select at least one place');
        return;
    }

    const startLat = parseFloat(document.getElementById('start_lat').value);
    const startLng = parseFloat(document.getElementById('start_lng').value);

    // Get selected place IDs
    const selectedPlaceIds = Array.from(selectedPlaces).map(index =>
        similarPlacesData[index].place_id
    );

    // Show loading
    document.getElementById('loading').style.display = 'block';

    try {
        // Call trip planning API with selected places
        const response = await fetch(`${API_BASE_URL}/api/plan-trip-from-places`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                start_lat: startLat,
                start_lng: startLng,
                place_ids: selectedPlaceIds
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to plan trip');
        }

        const tripData = await response.json();
        displayTripResults(tripData);
        displayRouteOnMap(tripData, startLat, startLng);

    } catch (error) {
        console.error('Error planning trip:', error);
        alert(`Error: ${error.message}`);
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
});

// Display trip results
function displayTripResults(tripData) {
    const summaryDiv = document.getElementById('trip-summary');
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

    document.getElementById('trip-results').style.display = 'block';
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

    tripData.route.forEach((place) => {
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
});
