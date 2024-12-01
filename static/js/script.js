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
