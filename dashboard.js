document.addEventListener("DOMContentLoaded", function () {

    // ===============================
    // Income vs Expense Bar Chart
    // ===============================

    const incomeCanvas = document.getElementById("incomeExpenseChart");

    if (incomeCanvas) {

        new Chart(incomeCanvas, {

            type: "bar",

            data: {

                labels: monthLabels,

                datasets: [

                    {
                        label: "Income",

                        data: monthlyIncome,

                        backgroundColor: "rgba(34,197,94,0.85)",

                        borderRadius: 12,

                        borderSkipped: false,

                        maxBarThickness: 40

                    },

                    {
                        label: "Expense",

                        data: monthlyExpense,

                        backgroundColor: "rgba(239,68,68,0.85)",

                        borderRadius: 12,

                        borderSkipped: false,

                        maxBarThickness: 40

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

                        position: "top",

                        labels: {

                            usePointStyle: true,

                            pointStyle: "circle",

                            padding: 20,

                            font: {

                                size: 13,

                                weight: "600"

                            }

                        }

                    }

                },

                scales: {

                    y: {

                        beginAtZero: true,

                        grid: {

                            color: "#edf2f7"

                        },

                        ticks: {

                            callback: function(value){

                                return "₹ " + value;

                            }

                        }

                    },

                    x: {

                        grid: {

                            display: false

                        }

                    }

                },

                animation: {

                    duration: 1200

                }

            }

        });

    }

    // ===============================
    // Expense Pie Chart
    // ===============================

    const pieCanvas = document.getElementById("categoryChart");

    if (pieCanvas) {

        new Chart(pieCanvas, {

            type: "doughnut",

            data: {

                labels: categoryLabels,

                datasets: [

                    {

                        data: categoryAmounts,

                        borderWidth: 0,

                        hoverOffset: 18,

                        backgroundColor: [

                            "#2563EB",

                            "#10B981",

                            "#F59E0B",

                            "#EF4444",

                            "#8B5CF6",

                            "#06B6D4",

                            "#EC4899",

                            "#14B8A6",

                            "#F97316",

                            "#64748B"

                        ]

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                cutout: "65%",

                plugins: {

                    legend: {

                        position: "bottom",

                        labels: {

                            padding: 18,

                            usePointStyle: true,

                            pointStyle: "circle"

                        }

                    }

                },

                animation: {

                    animateRotate: true,

                    animateScale: true,

                    duration: 1500

                }

            }

        });

    }

});