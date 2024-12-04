document
  .getElementById("carbonFootprintForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent default form submission

    // Gather form data
    const transportation = document.getElementById("transportation").value;
    const milesTravelled = parseFloat(
      document.getElementById("milesTravelled").value
    );
    const electricityUsage = parseFloat(
      document.getElementById("electricityUsage").value
    );
    const gasUsage = parseFloat(document.getElementById("gasUsage").value);
    const waste = parseFloat(document.getElementById("waste").value);

    // Perform calculations (example logic, replace with actual calculation formula)
    const footprint =
      milesTravelled * 0.21 +
      electricityUsage * 0.45 +
      gasUsage * 2.5 +
      waste * 1.2;

    // Display the result (optional)
    alert(
      `Your estimated carbon footprint is ${footprint.toFixed(
        2
      )} kg CO2 per month.`
    );
  });


function addTransportationField() {
  const transportationDetails = document.getElementById(
    "transportationDetails"
  );
  const newField = document.createElement("div");
  newField.className = "dynamic-input";
  newField.innerHTML = `
                <input type="number" name="milesTravelled[]" min="0" placeholder="Miles Travelled" required class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500">
                <button type="button" class="remove-btn" onclick="removeField(this)">Remove</button>
            `;
  transportationDetails.appendChild(newField);
}

function removeField(button) {
  button.parentElement.remove();
}

var themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
var themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');

// Change the icons inside the button based on previous settings
if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    themeToggleLightIcon.classList.remove('hidden');
} else {
    themeToggleDarkIcon.classList.remove('hidden');
}

var themeToggleBtn = document.getElementById('theme-toggle');

themeToggleBtn.addEventListener('click', function() {

    // toggle icons inside button
    themeToggleDarkIcon.classList.toggle('hidden');
    themeToggleLightIcon.classList.toggle('hidden');

    // if set via local storage previously
    if (localStorage.getItem('color-theme')) {
        if (localStorage.getItem('color-theme') === 'light') {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        }

    // if NOT set via local storage previously
    } else {
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        }
    }
    
});
