document.addEventListener("DOMContentLoaded", function () {
  const barColors = [
    "#1D537D", // Dark Blue
    "#632516", // Dark Red
    "#3626a7", // Dark Purple
    "#0d0106", // Very Dark Brown
    "#657ed4", // Light Blue
    "#6c756b", // Olive Green
    "#4B1D59", // Deep Pink
    "#db7f67", // Soft Orange
  ];

  // Function to convert hex color to RGBA (with transparency)
  function hexToRgba(hex, alpha = 0.8) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`; // Reduced transparency
  }

  // Job Group Chart (Bar Chart)
  const jobGroupChart = new Chart(document.getElementById("jobGroupChart"), {
    type: "bar",
    data: {
      labels: jobGroupLabels, // Labels for job groups
      datasets: [
        {
          label: "Number of Employees",
          data: jobGroupCounts, // Data for the number of employees
          backgroundColor: barColors.map((color) => hexToRgba(color, 0.8)), // Less transparent
          borderColor: barColors.map((color) => hexToRgba(color, 1)), // Solid border (no transparency)
          borderWidth: 1,
        },
      ],
    },
    options: getChartOptions("Job Groups", "Number of Employees", false),
  });

  // Branch Distribution Chart (Bar Chart)
  const branchChart = new Chart(document.getElementById("branchChart"), {
    type: "bar",
    data: {
      labels: branchLabels,
      datasets: [
        {
          label: "Number of Employees",
          data: branchCounts,
          backgroundColor: barColors.map((color) => hexToRgba(color, 0.8)),
          borderColor: barColors.map((color) => hexToRgba(color, 1)),
          borderWidth: 1,
        },
      ],
    },
    options: getChartOptions("Branches", "Number of Employees", false),
  });

  // Department Distribution Chart (Bar Chart)
  const departmentChart = new Chart(
    document.getElementById("departmentChart"),
    {
      type: "bar",
      data: {
        labels: departmentLabels, // Labels for departments
        datasets: [
          {
            label: "Number of Employees",
            data: departmentCounts, // Data for number of employees
            backgroundColor: barColors.map((color) => hexToRgba(color, 0.8)),
            borderColor: barColors.map((color) => hexToRgba(color, 1)),
            borderWidth: 1,
          },
        ],
      },
      options: getChartOptions("Departments", "Number of Employees", false),
    },
  );

  // Salary Distribution by Job Group (Line Chart)
  const salaryGroupChart = new Chart(
    document.getElementById("salaryGroupChart"),
    {
      type: "line",
      data: {
        labels: salaryGroupLabels, // Labels for job groups
        datasets: [
          {
            label: "Net Salary by Job Group",
            data: netSalaryValues, // Data for net salaries
            fill: false,
            borderColor: "#4B1D59", // Deep Pink color for Net Salary
            tension: 0.4,
            borderWidth: 2,
          },
          {
            label: "Base Salary by Job Group",
            data: baseSalaryValues, // Data for base salaries
            fill: false,
            borderColor: "#1D537D", // Dark Blue color for Base Salary
            tension: 0.4,
            borderWidth: 2,
          },
        ],
      },
      options: getChartOptions("Job Groups", "Salary Amount", true),
    },
  );

  // Function to generate chart options
  function getChartOptions(xLabel, yLabel, showLegend = true) {
    return {
      responsive: true,
      plugins: {
        legend: { display: showLegend }, // Control legend visibility
        tooltip: {
          callbacks: {
            label: function (context) {
              // Format numbers with commas in tooltips
              return (
                context.dataset.label + ": " + context.raw.toLocaleString()
              );
            },
          },
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: xLabel,
            font: { weight: "bold" },
          },
          ticks: {
            font: { weight: "bold" },
          },
        },
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: yLabel,
            font: { weight: "bold" },
          },
          ticks: {
            precision: 0, // No decimals
            font: { weight: "bold" },
            callback: function (value) {
              return value.toLocaleString(); // Format numbers with commas
            },
          },
        },
      },
    };
  }

  // Chart Switching Logic (Excluding the Salary Distribution Chart)
  const chartSelector = document.getElementById("chartSelector");
  const switchableCharts = document.querySelectorAll(
    ".chart:not(#salaryGroupChart)",
  ); // Exclude salary chart

  chartSelector.addEventListener("change", function () {
    const selectedChartId = this.value;

    switchableCharts.forEach((chart) => {
      if (chart.id === selectedChartId) {
        chart.classList.remove("d-none");
      } else {
        chart.classList.add("d-none");
      }
    });
  });

  // Ensure the salary chart is always visible
  const salaryChart = document.getElementById("salaryGroupChart");
  salaryChart.classList.remove("d-none");
});
