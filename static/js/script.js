document.addEventListener("DOMContentLoaded", function () {
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

  var userEnergyUsage = null,
    userWaste = null,
    userBusinessTravel = null;

  if (userFinalData && userFinalData[0]) {
    userEnergyUsage = userFinalData[0].energy_usage || 0;
    userWaste = userFinalData[0].waste || 0;
    userBusinessTravel = userFinalData[0].business_travel || 0;

    console.log(userEnergyUsage);
    console.log(userWaste);
    console.log(userBusinessTravel);

    // Proceed with chart rendering or other operations
  } else {
    console.warn("No user data available");
    // Handle cases when no user data is present (e.g., show default values in the chart)
  }


  // Max values
  const maxEnergyUsage = stats.energy_usage.max;
  const maxWaste = stats.waste.max;
  const maxBusinessTravel = stats.business_travel.max;

  // Min values
  const minEnergyUsage = stats.energy_usage.min;
  const minWaste = stats.waste.min;
  const minBusinessTravel = stats.business_travel.min;

  // avrage values
  const avgEnergyUsage = stats.energy_usage.avg;
  const avgWaste = stats.waste.avg;
  const avgBusinessTravel = stats.business_travel.avg;

  const ctx = document.getElementById("myChart");

  const datasets = [];

  // Add user's data if available
  if (userEnergyUsage && userWaste && userBusinessTravel) {
    datasets.push({
      label: "Your Value",
      data: [userEnergyUsage, userWaste, userBusinessTravel],
      backgroundColor: [
        "rgba(54, 162, 235, 0.8)", // Blue for user's value
        "rgba(54, 162, 235, 0.8)",
        "rgba(54, 162, 235, 0.8)",
      ],
      borderColor: [
        "rgb(54, 162, 235)",
        "rgb(54, 162, 235)",
        "rgb(54, 162, 235)",
      ],
      borderWidth: 3,
    });
  }

  // Add max records data
  datasets.push({
    label: "Max Records",
    data: [maxEnergyUsage, maxWaste, maxBusinessTravel],
    backgroundColor: [
      "rgba(255, 99, 132, 0.8)", // Red for max
      "rgba(255, 99, 132, 0.8)",
      "rgba(255, 99, 132, 0.8)",
    ],
    borderColor: [
      "rgb(255, 99, 132)",
      "rgb(255, 99, 132)",
      "rgb(255, 99, 132)",
    ],
    borderWidth: 3,
  });

  if (!userEnergyUsage && !userBusinessTravel) {
    datasets.push({
      label: "Average Records",
      data: [avgEnergyUsage, avgWaste, avgBusinessTravel],
      backgroundColor: [
        "rgba(255, 159, 64, 0.8)", // Orange for average
        "rgba(255, 159, 64, 0.8)",
        "rgba(255, 159, 64, 0.8)",
      ],
      borderColor: [
        "rgb(255, 159, 64)",
        "rgb(255, 159, 64)",
        "rgb(255, 159, 64)",
      ],
      borderWidth: 3,
    });
  }
  // Add average records data

  // Add min records data
  datasets.push({
    label: "Min Records",
    data: [minEnergyUsage, minWaste, minBusinessTravel],
    backgroundColor: [
      "rgba(75, 192, 192, 0.8)", // Green for min
      "rgba(75, 192, 192, 0.8)",
      "rgba(75, 192, 192, 0.8)",
    ],
    borderColor: [
      "rgb(75, 192, 192)",
      "rgb(75, 192, 192)",
      "rgb(75, 192, 192)",
    ],
    borderWidth: 3,
  });

  // Initialize the chart
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Energy Usage", "Waste", "Travel"],
      datasets: datasets,
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
});
