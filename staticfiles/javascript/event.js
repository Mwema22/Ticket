function initMap() {
    if (window.eventLocation) {
        const { lat, lng, name, address } = window.eventLocation;

        const map = new google.maps.Map(document.getElementById("eventMap"), {
            center: { lat: lat, lng: lng },
            zoom: 14,
        });

        const marker = new google.maps.Marker({
            position: { lat: lat, lng: lng },
            map: map,
            title: name,
        });

        const infoWindow = new google.maps.InfoWindow({
            content: `<strong>${name}</strong><br>${address}`,
        });

        infoWindow.open(map, marker);
    }
}
