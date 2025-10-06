// Add event listener for Enter key on input
document.getElementById('cityInput').addEventListener('keypress', function (e) {
  if (e.key === 'Enter') {
    searchCity();
  }
});

function searchCity(cityName = null) {
  // Get city from input or parameter
  const city = cityName || document.getElementById('cityInput').value.trim();

  if (!city) {
    showError('Please enter a city name');
    return;
  }

  // Show loading spinner and hide other elements
  document.getElementById('loadingSpinner').style.display = 'block';
  document.getElementById('weatherCard').style.display = 'none';
  document.getElementById('errorAlert').style.display = 'none';

  fetchWeather(city);
}

async function fetchWeather(city) {
  try {
    const response = await fetch(
      `http://localhost:5000/get_precip?city=${encodeURIComponent(city)}`
    );
    const data = await response.json();

    if (response.ok) {
      updateWeatherUI(data);
    } else {
      throw new Error(data.error || 'Failed to fetch weather data');
    }
  } catch (error) {
    showError(error.message);
  } finally {
    document.getElementById('loadingSpinner').style.display = 'none';
  }
}

function updateWeatherUI(data) {
  // Show weather card
  document.getElementById('weatherCard').style.display = 'block';

  // Update weather information
  document.getElementById('cityName').textContent = data.city;
  document.getElementById('temperature').textContent = `${Math.round(
    data.temperature
  )}°C`;
  document.getElementById('humidity').textContent = `${data.humidity}%`;
  document.getElementById('description').textContent = capitalize(
    data.description
  );
  document.getElementById('feelsLike').textContent = `Feels like: ${Math.round(
    data.feels_like
  )}°C`;
  document.getElementById(
    'windSpeed'
  ).textContent = `Wind: ${data.wind_speed} m/s`;

  // Update weather icon
  document.getElementById(
    'weatherIcon'
  ).src = `http://openweathermap.org/img/wn/${data.icon}@2x.png`;

  // Update last update time
  const now = new Date();
  document.getElementById(
    'lastUpdate'
  ).textContent = `Last updated: ${now.toLocaleTimeString()}`;
}

function showError(message) {
  document.getElementById('errorAlert').style.display = 'block';
  document.getElementById('errorMessage').textContent = message;
  document.getElementById('weatherCard').style.display = 'none';
  document.getElementById('loadingSpinner').style.display = 'none';
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

// Initial weather fetch for Los Angeles
searchCity('Los Angeles');
