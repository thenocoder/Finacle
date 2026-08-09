// ==========================================
// Expense Prediction Dashboard
// ==========================================

document.addEventListener("DOMContentLoaded", () => {

    initializePrediction();

});

function initializePrediction() {

    animateCards();

    animateValues();

}

// ==========================================
// Card Hover Animation
// ==========================================

function animateCards() {

    const cards = document.querySelectorAll(".card");

    cards.forEach(card => {

        card.addEventListener("mouseenter", () => {

            card.style.transform = "translateY(-5px)";

            card.style.transition = "0.3s";

        });

        card.addEventListener("mouseleave", () => {

            card.style.transform = "translateY(0px)";

        });

    });

}

// ==========================================
// Number Animation
// ==========================================

function animateValues() {

    const values = document.querySelectorAll(".prediction-value");

    values.forEach(value => {

        const text = value.textContent
            .replace("₹", "")
            .replace(/,/g, "")
            .trim();

        const target = parseFloat(text);

        if (isNaN(target)) {

            return;

        }

        let current = 0;

        const increment = target / 60;

        const timer = setInterval(() => {

            current += increment;

            if (current >= target) {

                current = target;

                clearInterval(timer);

            }

            value.textContent =
                "₹ " +
                current.toLocaleString("en-IN", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                });

        }, 20);

    });

}

// ==========================================
// Trend Badge Color
// ==========================================

const trend = document.getElementById("trendBadge");

if (trend) {

    const value = trend.innerText.trim();

    if (value === "Increasing") {

        trend.classList.add("text-danger");

    }

    else if (value === "Decreasing") {

        trend.classList.add("text-success");

    }

    else {

        trend.classList.add("text-primary");

    }

}
