"use strict";

/* ==========================================================
                    FINACLE REPORTS
========================================================== */

/* ==========================================================
                    CHART INSTANCES
========================================================== */

let cashflowChart = null;
let expensePieChart = null;
let monthlyTrendChart = null;
let allocationChart = null;

/* ==========================================================
                    PAGE READY
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    initializeCharts();

    initializeCards();

    console.log("Finacle Reports Dashboard Loaded");

});

/* ==========================================================
                    INITIALIZE ALL
========================================================== */

function initializeCharts() {

    initializeCashflowChart();

    initializeExpenseChart();

    initializeMonthlyTrend();

    initializeAllocationChart();

}

/* ==========================================================
                    HELPERS
========================================================== */

function canvas(id) {

    return document.getElementById(id);

}

function chartExists(chart) {

    return chart !== null;

}

function destroyChart(chart) {

    if (chartExists(chart)) {

        chart.destroy();

    }

}

function defaultColors() {

    return [

        "#0d6efd",
        "#198754",
        "#ffc107",
        "#dc3545",
        "#6f42c1",
        "#20c997",
        "#fd7e14",
        "#6610f2",
        "#0dcaf0",
        "#adb5bd"

    ];

}

function createChart(id, config) {

    const element = canvas(id);

    if (!element) {

        console.warn(id + " canvas not found.");

        return null;

    }

    if (typeof Chart === "undefined") {

        console.warn("Chart.js not loaded.");

        return null;

    }

    return new Chart(element, config);

}

/* ==========================================================
                    CASHFLOW
========================================================== */

function initializeCashflowChart() {

    if (typeof cashflowData === "undefined") {

        return;

    }

    destroyChart(cashflowChart);

    cashflowChart = createChart("cashflowChart", {

        type: "doughnut",

        data: {

            labels: [

                "Income",

                "Expense"

            ],

            datasets: [

                {

                    data: [

                        cashflowData.income,

                        cashflowData.expense

                    ],

                    backgroundColor: [

                        "#198754",

                        "#dc3545"

                    ],

                    borderWidth: 2

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    });

}

/* ==========================================================
                    EXPENSE PIE
========================================================== */

function initializeExpenseChart() {

    if (typeof categoryData === "undefined") {

        return;

    }

    destroyChart(expensePieChart);

    expensePieChart = createChart("expensePieChart", {

        type: "pie",

        data: {

            labels: categoryData.map(item => item.category),

            datasets: [

                {

                    data: categoryData.map(item => item.amount),

                    backgroundColor: defaultColors(),

                    borderWidth: 2

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    });

}
/* ==========================================================
                    MONTHLY TREND
========================================================== */

function initializeMonthlyTrend() {

    if (typeof monthlyTrendData === "undefined") {

        return;

    }

    destroyChart(monthlyTrendChart);

    monthlyTrendChart = createChart("monthlyTrendChart", {

        type: "bar",

        data: {

            labels: monthlyTrendData.map(item => item.month),

            datasets: [

                {

                    label: "Income",

                    data: monthlyTrendData.map(item => item.income),

                    backgroundColor: "#198754",

                    borderRadius: 6

                },

                {

                    label: "Expense",

                    data: monthlyTrendData.map(item => item.expense),

                    backgroundColor: "#dc3545",

                    borderRadius: 6

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

                }

            },

            scales: {

                y: {

                    beginAtZero: true

                }

            }

        }

    });

}

/* ==========================================================
                SMART ALLOCATION
========================================================== */

function initializeAllocationChart() {

    if (typeof allocationData === "undefined") {

        return;

    }

    destroyChart(allocationChart);

    allocationChart = createChart("allocationChart", {

        type: "polarArea",

        data: {

            labels: allocationData.map(item => item.category),

            datasets: [

                {

                    data: allocationData.map(item => item.amount),

                    backgroundColor: defaultColors(),

                    borderWidth: 2

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    });

}

/* ==========================================================
                    CARD EFFECTS
========================================================== */

function initializeCards() {

    document.querySelectorAll(".dashboard-card").forEach(card => {

        card.style.transition =
            "all .25s ease";

        card.addEventListener("mouseenter", () => {

            card.style.transform = "translateY(-5px)";

            card.style.boxShadow =
                "0 18px 40px rgba(0,0,0,.12)";

        });

        card.addEventListener("mouseleave", () => {

            card.style.transform = "translateY(0)";

            card.style.boxShadow = "";

        });

    });

}

/* ==========================================================
                    REFRESH
========================================================== */

function refreshCharts() {

    if (cashflowChart) {

        cashflowChart.update();

    }

    if (expensePieChart) {

        expensePieChart.update();

    }

    if (monthlyTrendChart) {

        monthlyTrendChart.update();

    }

    if (allocationChart) {

        allocationChart.update();

    }

}

/* ==========================================================
                    WINDOW RESIZE
========================================================== */

window.addEventListener("resize", () => {

    refreshCharts();

});

/* ==========================================================
                    GLOBAL ACCESS
========================================================== */

window.refreshReportCharts = refreshCharts;

/* ==========================================================
                    STARTUP LOG
========================================================== */

console.log(`

=========================================================

            FINACLE REPORTS READY

=========================================================

✓ Cash Flow Chart

✓ Expense Distribution

✓ Monthly Trend

✓ Smart Allocation

✓ Card Animations

✓ Responsive Layout

Status : READY

=========================================================

`);