// ======================================================
// Future Financial Simulator
// ======================================================

document.addEventListener("DOMContentLoaded", () => {

    if (typeof projectionData === "undefined") {
        return;
    }

    const years = projectionData.map(item => item.year);

    const invested = projectionData.map(item => item.invested);

    const portfolio = projectionData.map(item => item.value);

    const profit = projectionData.map(item => item.profit);

    const canvas = document.getElementById("growthChart");

    if (!canvas) {
        return;
    }

    new Chart(canvas, {

        type: "line",

        data: {

            labels: years,

            datasets: [

                {
                    label: "Portfolio Value",

                    data: portfolio,

                    borderColor: "#0d6efd",

                    backgroundColor: "rgba(13,110,253,0.15)",

                    fill: true,

                    tension: 0.35,

                    borderWidth: 3,

                    pointRadius: 4,

                    pointHoverRadius: 6
                },

                {
                    label: "Amount Invested",

                    data: invested,

                    borderColor: "#198754",

                    backgroundColor: "transparent",

                    fill: false,

                    borderDash: [6, 4],

                    borderWidth: 2,

                    pointRadius: 3
                },

                {
                    label: "Profit",

                    data: profit,

                    borderColor: "#ffc107",

                    backgroundColor: "transparent",

                    fill: false,

                    borderWidth: 2,

                    pointRadius: 3
                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            interaction: {

                mode: "index",

                intersect: false

            },

            plugins: {

                legend: {

                    position: "top"

                },

                tooltip: {

                    callbacks: {

                        label: function(context) {

                            return context.dataset.label +
                                   ": ₹" +
                                   Number(context.raw).toLocaleString(
                                       "en-IN",
                                       {
                                           minimumFractionDigits: 2,
                                           maximumFractionDigits: 2
                                       }
                                   );
                        }

                    }

                }

            },

            scales: {

                y: {

                    beginAtZero: true,

                    ticks: {

                        callback: function(value) {

                            return "₹" + Number(value).toLocaleString("en-IN");

                        }

                    }

                }

            }

        }

    });

});