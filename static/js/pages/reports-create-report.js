document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("use-location");
  const latInput = document.getElementById("id_latitude");
  const lngInput = document.getElementById("id_longitude");
  if (!button || !latInput || !lngInput) return;

  button.addEventListener("click", () => {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by this browser.");
      return;
    }

    button.disabled = true;
    button.textContent = "Getting location...";
    navigator.geolocation.getCurrentPosition(
      (position) => {
        latInput.value = position.coords.latitude.toFixed(6);
        lngInput.value = position.coords.longitude.toFixed(6);
        button.textContent = "Location captured";
      },
      () => {
        alert("Unable to capture your location. Please enter it manually.");
        button.textContent = "Use My Current Location";
      },
      { enableHighAccuracy: true, timeout: 8000 }
    );
  });
});
