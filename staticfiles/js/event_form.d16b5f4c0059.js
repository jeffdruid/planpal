function initAutocomplete() {
    const locationInput = document.getElementById('location');
    const autocomplete = new google.maps.places.Autocomplete(locationInput);

    autocomplete.addListener('place_changed', function() {
        const place = autocomplete.getPlace();
        const mapLink = document.getElementById('mapLink');
        if (place.geometry) {
            const location = place.formatted_address || place.name;
            mapLink.href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(location)}`;
            mapLink.style.display = 'inline';
        } else {
            mapLink.href = '#';
            mapLink.style.display = 'none';
        }
    });
}

function updateMapLink() {
    const location = document.getElementById('location').value;
    const mapLink = document.getElementById('mapLink');
    if (location) {
        mapLink.href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(location)}`;
        mapLink.style.display = 'inline';
    } else {
        mapLink.href = '#';
        mapLink.style.display = 'none';
    }
}

window.onload = function() {
    initAutocomplete();
    updateMapLink();
};
