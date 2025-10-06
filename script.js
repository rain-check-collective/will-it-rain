document.addEventListener('DOMContentLoaded', () => {
  const weatherForm = document.getElementById('weatherForm');
  const yearSelect = document.getElementById('yearSelect');
  const monthSelect = document.getElementById('monthSelect');
  const daySelect = document.getElementById('daySelect');
  const weatherResultDiv = document.getElementById('weatherResult');
  const loadingSpinner = document.getElementById('loadingSpinner');

  // date range
  const minDate = new Date('1970-01-01T00:00:00Z'); // January 1, 1970
  const maxDate = new Date('2025-10-06T23:59:59Z'); // October 6, 2025

  // --- Populate Year Dropdown ---
  for (
    let year = maxDate.getFullYear();
    year >= minDate.getFullYear();
    year--
  ) {
    const option = document.createElement('option');
    option.value = String(year);
    option.textContent = String(year);
    yearSelect.appendChild(option);
  }

  // --- Populate Day Dropdown ---
  function populateDays() {
    // Clear existing days
    daySelect.innerHTML = '';

    const selectedYear = parseInt(yearSelect.value);
    const selectedMonth = parseInt(monthSelect.value);

    if (isNaN(selectedYear) || isNaN(selectedMonth)) {
      // If no year/month is selected yet, or invalid, disable days
      daySelect.disabled = true;
      return;
    }
    daySelect.disabled = false;

    // Get the number of days in the selected month/year
    // The day 0 of the next month is the last day of the current month
    const daysInMonth = new Date(selectedYear, selectedMonth, 0).getDate();

    for (let day = 1; day <= daysInMonth; day++) {
      const option = document.createElement('option');
      option.value = String(day).padStart(2, '0'); // Pad with leading zero for month/day
      option.textContent = String(day);
      daySelect.appendChild(option);
    }

    // Adjust for max date if the selected date is October 6, 2025
    if (
      selectedYear === maxDate.getFullYear() &&
      selectedMonth === maxDate.getMonth() + 1
    ) {
      const maxDay = maxDate.getDate();
      Array.from(daySelect.options).forEach((option) => {
        if (parseInt(option.value) > maxDay) {
          option.disabled = true;
        } else {
          option.disabled = false;
        }
      });
      // If selected day is beyond maxDay, reset to maxDay
      if (parseInt(daySelect.value) > maxDay) {
        daySelect.value = String(maxDay).padStart(2, '0');
      }
    } else {
      Array.from(daySelect.options).forEach(
        (option) => (option.disabled = false)
      );
    }

    // Adjust for min date if the selected date is January 1, 1970
    if (
      selectedYear === minDate.getFullYear() &&
      selectedMonth === minDate.getMonth() + 1
    ) {
      const minDay = minDate.getDate();
      Array.from(daySelect.options).forEach((option) => {
        if (parseInt(option.value) < minDay) {
          option.disabled = true;
        } else {
          option.disabled = false;
        }
      });
      if (parseInt(daySelect.value) < minDay) {
        daySelect.value = String(minDay).padStart(2, '0');
      }
    } else {
      Array.from(daySelect.options).forEach(
        (option) => (option.disabled = false)
      );
    }
  }

  // Event listeners for month/year changes
  yearSelect.addEventListener('change', populateDays);
  monthSelect.addEventListener('change', populateDays);

  // --- Set Defaults to KDCA on December 5, 2024 (matching BaseModel) ---
  cityStationSelect.value = 'KDCA'; // Set default station
  yearSelect.value = '2024'; // Set default year
  monthSelect.value = '12'; // Set default month (December)

  populateDays(); // Populate days based on the new default year/month

  // Now set the day after days are populated
  daySelect.value = '05';

  // --- Form Submission Handler ---
  weatherForm.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent default form submission

    weatherResultDiv.innerHTML = ''; // Clear previous results
    loadingSpinner.style.display = 'block'; // Show loading spinner

    const station = document.getElementById('cityStationSelect').value;
    const year = yearSelect.value;
    const month = monthSelect.value;
    const day = daySelect.value;

    // Construct the payload matching the WeatherRequest BaseModel
    const payload = {
      station: station,
      year: year,
      month: month,
      day: day,
    };

    try {
      const response = await fetch('http://localhost:8000/api/weather', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        // Read error message from backend if available
        const errorData = await response.json();
        throw new Error(
          errorData.detail || `HTTP error! Status: ${response.status}`
        );
      }

      const data = await response.json();

      const selectedStationText =
        cityStationSelect.options[cityStationSelect.selectedIndex].text;

      weatherResultDiv.innerHTML = `
                <h2>Climate Averages for ${selectedStationText} (${station}) on ${month}/${day}/${year}</h2>
                <p>Chance of Rain: <strong>${data.rain.toFixed(1)}%</strong></p>
                <p>Chance of High Temps (Avg. max temp > 80F/26.7C): <strong>${data.heat.toFixed(
                  1
                )}%</strong></p>
                <p>Chance of Low Temps (Avg. min temp < 32F/0C): <strong>${data.cold.toFixed(
                  1
                )}%</strong></p>
                <p>Chance of Windy Conditions (> 15 knots): <strong>${data.wind.toFixed(
                  1
                )}%</strong></p>
                <p>Chance of High Humidity (> 70%): <strong>${data.humidity.toFixed(
                  1
                )}%</strong></p>
            `;
    } catch (error) {
      console.error('Error fetching weather:', error);
      weatherResultDiv.innerHTML = `<p style="color: red;">Failed to fetch weather data: ${error.message}</p>`;
    } finally {
      loadingSpinner.style.display = 'none';
    }
  });
});
