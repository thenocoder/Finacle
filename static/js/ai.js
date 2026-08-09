/* ===========================================================
   FINACLE AI ASSISTANT
   ai.js
   Production Sync
   Part 1
=========================================================== */

"use strict";

/* ===========================================================
   GLOBAL VARIABLES
=========================================================== */

let monthlyChart = null;
let categoryChart = null;

const dashboardData = window.dashboardData || {};

/* ===========================================================
   API ENDPOINTS
=========================================================== */

const API = window.AI_CONFIG || {

    chatUrl: "/ai/chat",

    dashboardUrl: "/ai/dashboard",

    historyUrl: "/ai/history",

    clearHistoryUrl: "/ai/clear-history",

    testUrl: "/ai/test"

};

/* ===========================================================
   DOM ELEMENTS
=========================================================== */

const chatBody =
    document.getElementById("chatBody");

const typingIndicator =
    document.getElementById("typingIndicator");

const userMessage =
    document.getElementById("userMessage");

const sendButton =
    document.getElementById("sendMessage");

const refreshButton =
    document.getElementById("refreshDashboard");

const clearHistoryButton =
    document.getElementById("clearHistory");

/* ===========================================================
   PAGE INITIALIZATION
=========================================================== */

document.addEventListener(

    "DOMContentLoaded",

    () => {

        initializeEvents();

        initializePromptButtons();

        initializeCharts();

        updateSummaryCards();

        loadHistory();

        scrollToBottom();

        console.log("✅ Finacle AI Initialized");

    }

);

/* ===========================================================
   INITIALIZE EVENTS
=========================================================== */

function initializeEvents() {

    if (sendButton) {

        sendButton.addEventListener(

            "click",

            sendCurrentMessage

        );

    }

    if (userMessage) {

        userMessage.addEventListener(

            "keydown",

            function (event) {

                if (

                    event.key === "Enter" &&

                    !event.shiftKey

                ) {

                    event.preventDefault();

                    sendCurrentMessage();

                }

            }

        );

    }

    if (refreshButton) {

        refreshButton.addEventListener(

            "click",

            refreshDashboard

        );

    }

    if (clearHistoryButton) {

        clearHistoryButton.addEventListener(

            "click",

            clearHistory

        );

    }

}

/* ===========================================================
   SEND CURRENT MESSAGE
=========================================================== */

function sendCurrentMessage() {

    if (!userMessage) return;

    const message = userMessage.value.trim();

    if (!message) return;

    userMessage.value = "";

    sendMessage(message);

}

/* ===========================================================
   UTILITIES
=========================================================== */

function formatCurrency(value) {

    return new Intl.NumberFormat(

        "en-IN",

        {

            style: "currency",

            currency: "INR",

            minimumFractionDigits: 2,

            maximumFractionDigits: 2

        }

    ).format(Number(value || 0));

}

function escapeHTML(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;

}

function scrollToBottom() {

    if (!chatBody) return;

    chatBody.scrollTop =

        chatBody.scrollHeight;

}

/* ===========================================================
   TYPING INDICATOR
=========================================================== */

function showTyping() {

    if (!typingIndicator) return;

    typingIndicator.classList.remove("d-none");

    scrollToBottom();

}

function hideTyping() {

    if (!typingIndicator) return;

    typingIndicator.classList.add("d-none");

}

/* ===========================================================
   TOAST
=========================================================== */

function showToast(

    message,

    type = "primary"

) {

    const toast =

        document.createElement("div");

    toast.className =

        `alert alert-${type}`;

    toast.style.position = "fixed";

    toast.style.right = "20px";

    toast.style.bottom = "20px";

    toast.style.zIndex = "9999";

    toast.style.minWidth = "300px";

    toast.innerHTML = message;

    document.body.appendChild(toast);

    setTimeout(

        () => toast.remove(),

        3000

    );

}
/* ===========================================================
   PART 2
   CHAT ENGINE
=========================================================== */

/* ===========================================================
   MESSAGE TEMPLATES
=========================================================== */

function createUserMessage(message) {

    return `

        <div class="message user">

            <div class="message-content">

                ${escapeHTML(message)}

            </div>

        </div>

    `;

}


function createAIMessage(message) {

    let html = escapeHTML(message);

    if (window.marked) {

        html = marked.parse(message);

    }

    return `

        <div class="message assistant">

            <div class="assistant-avatar">

                <i class="bi bi-stars"></i>

            </div>

            <div class="message-content">

                ${html}

            </div>

        </div>

    `;

}


/* ===========================================================
   APPEND MESSAGES
=========================================================== */

function appendUserMessage(message) {

    if (!chatBody) return;

    chatBody.insertAdjacentHTML(

        "beforeend",

        createUserMessage(message)

    );

    scrollToBottom();

}


function appendAIMessage(message) {

    if (!chatBody) return;

    chatBody.insertAdjacentHTML(

        "beforeend",

        createAIMessage(message)

    );

    scrollToBottom();

}


/* ===========================================================
   SEND MESSAGE
=========================================================== */

async function sendMessage(message) {

    appendUserMessage(message);

    showTyping();

    if (sendButton) {

        sendButton.disabled = true;

    }

    try {

        const response = await fetch(

            API.chatUrl,

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    message: message

                })

            }

        );

        const result = await response.json();

        hideTyping();

        if (result.success) {

            appendAIMessage(result.response);

            await loadHistory();

        }

        else {

            appendAIMessage(

                result.message ||

                "Unable to process your request."

            );

        }

    }

    catch (error) {

        hideTyping();

        appendAIMessage(

`❌ Unable to connect to the AI server.

Reason:

${escapeHTML(error.message)}`

        );

    }

    finally {

        if (sendButton) {

            sendButton.disabled = false;

        }

        if (userMessage) {

            userMessage.focus();

        }

    }

}


/* ===========================================================
   QUICK PROMPTS
=========================================================== */

function initializePromptButtons() {

    const buttons =

        document.querySelectorAll(".prompt-btn");

    buttons.forEach(button => {

        button.addEventListener(

            "click",

            function () {

                const prompt =

                    this.textContent.trim();

                if (!prompt) return;

                sendMessage(prompt);

            }

        );

    });

}


/* ===========================================================
   CHAT HISTORY
=========================================================== */

async function loadHistory() {

    try {

        const response =

            await fetch(API.historyUrl);

        const result =

            await response.json();

        if (!result.success) {

            return;

        }

        const table =

            document.getElementById("historyTable");

        if (!table) {

            return;

        }

        table.innerHTML = "";

        if (result.history.length === 0) {

            table.innerHTML = `

                <tr>

                    <td colspan="3"

                        class="text-center py-5">

                        No conversation history

                    </td>

                </tr>

            `;

            return;

        }

        result.history.forEach(item => {

            table.insertAdjacentHTML(

                "beforeend",

                `

<tr>

<td>

${item.created_at}

</td>

<td>

${escapeHTML(item.prompt)}

</td>

<td>

${escapeHTML(item.response.substring(0,220))}

${item.response.length > 220 ? "..." : ""}

</td>

</tr>

`

            );

        });

    }

    catch (error) {

        console.error(

            "History Error:",

            error

        );

    }

}


/* ===========================================================
   CLEAR HISTORY
=========================================================== */

async function clearHistory() {

    if (

        !confirm(

            "Are you sure you want to clear your AI conversation history?"

        )

    ) {

        return;

    }

    try {

        const response =

            await fetch(

                API.clearHistoryUrl,

                {

                    method: "POST"

                }

            );

        const result =

            await response.json();

        if (result.success) {

            showToast(

                result.message,

                "success"

            );

            await loadHistory();

        }

    }

    catch (error) {

        showToast(

            error.message,

            "danger"

        );

    }

}
/* ===========================================================
   PART 3
   DASHBOARD + CHARTS
=========================================================== */

/* ===========================================================
   CHART DATA HELPERS
=========================================================== */

function getMonthlyChartData() {

    const income = dashboardData.monthly_income || {};
    const expense = dashboardData.monthly_expense || {};

    return {

        labels: Object.keys(income),

        income: Object.values(income),

        expense: Object.values(expense)

    };

}

function getCategoryChartData() {

    const categories = dashboardData.category_breakdown || {};

    return {

        labels: Object.keys(categories),

        values: Object.values(categories)

    };

}

/* ===========================================================
   MONTHLY TREND CHART
=========================================================== */

function initializeMonthlyChart() {

    const canvas = document.getElementById("monthlyTrendChart");

    if (!canvas || typeof Chart === "undefined") {

        return;

    }

    const data = getMonthlyChartData();

    if (monthlyChart) {

        monthlyChart.destroy();

    }

    monthlyChart = new Chart(canvas, {

        type: "line",

        data: {

            labels: data.labels,

            datasets: [

                {

                    label: "Income",

                    data: data.income,

                    borderWidth: 3,

                    tension: 0.35,

                    fill: false

                },

                {

                    label: "Expense",

                    data: data.expense,

                    borderWidth: 3,

                    tension: 0.35,

                    fill: false

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

                    position: "bottom"

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

/* ===========================================================
   CATEGORY CHART
=========================================================== */

function initializeCategoryChart() {

    const canvas = document.getElementById("categoryChart");

    if (!canvas || typeof Chart === "undefined") {

        return;

    }

    const data = getCategoryChartData();

    if (categoryChart) {

        categoryChart.destroy();

    }

    categoryChart = new Chart(canvas, {

        type: "doughnut",

        data: {

            labels: data.labels,

            datasets: [

                {

                    data: data.values,

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

/* ===========================================================
   INITIALIZE CHARTS
=========================================================== */

function initializeCharts() {

    initializeMonthlyChart();

    initializeCategoryChart();

}

/* ===========================================================
   SUMMARY CARD HELPERS
=========================================================== */

function setElement(id, value) {

    const element = document.getElementById(id);

    if (!element) {

        return;

    }

    element.innerHTML = value;

}

/* ===========================================================
   UPDATE SUMMARY CARDS
=========================================================== */

function updateSummaryCards() {

    const summary = dashboardData.summary;

    if (!summary) {

        return;

    }

    setElement(

        "healthScore",

        `${summary.health_score}<small>/100</small>`

    );

    setElement(

        "predictionValue",

        formatCurrency(

            dashboardData.prediction?.predicted_expense || 0

        )

    );

    setElement(

        "savingRate",

        `${summary.savings_rate}%`

    );

    setElement(

        "topCategory",

        summary.top_category || "N/A"

    );

    setElement(

        "totalIncome",

        formatCurrency(summary.income)

    );

    setElement(

        "totalExpense",

        formatCurrency(summary.expense)

    );

    setElement(

        "balance",

        formatCurrency(summary.balance)

    );

    const largest = document.getElementById("largestExpense");

    if (largest) {

        largest.innerHTML = `

            ${summary.largest_expense || "N/A"}

            <br>

            <small class="text-muted">

                ${formatCurrency(summary.largest_expense_amount)}

            </small>

        `;

    }

    if (dashboardData.trend) {

        setElement(

            "expenseTrend",

            dashboardData.trend.trend

        );

        setElement(

            "trendPercent",

            `${dashboardData.trend.percentage}%`

        );

    }

    setElement(

        "dailyAverage",

        formatCurrency(

            dashboardData.average_daily_spending || 0

        )

    );

}

/* ===========================================================
   UPDATE CHARTS
=========================================================== */

function updateCharts() {

    if (monthlyChart) {

        const monthly = getMonthlyChartData();

        monthlyChart.data.labels = monthly.labels;

        monthlyChart.data.datasets[0].data = monthly.income;

        monthlyChart.data.datasets[1].data = monthly.expense;

        monthlyChart.update();

    }

    if (categoryChart) {

        const category = getCategoryChartData();

        categoryChart.data.labels = category.labels;

        categoryChart.data.datasets[0].data = category.values;

        categoryChart.update();

    }

}

/* ===========================================================
   REFRESH DASHBOARD
=========================================================== */

async function refreshDashboard() {

    if (refreshButton) {

        refreshButton.disabled = true;

        refreshButton.innerHTML =

            `<i class="bi bi-arrow-repeat"></i> Refreshing...`;

    }

    try {

        const response = await fetch(API.dashboardUrl);

        const data = await response.json();

        Object.assign(dashboardData, data);

        updateSummaryCards();

        updateCharts();

        showToast(

            "Dashboard updated successfully.",

            "success"

        );

    }

    catch (error) {

        console.error(error);

        showToast(

            "Unable to refresh dashboard.",

            "danger"

        );

    }

    finally {

        if (refreshButton) {

            refreshButton.disabled = false;

            refreshButton.innerHTML =

                `<i class="bi bi-arrow-repeat"></i> Refresh Analysis`;

        }

    }

}

/* ===========================================================
   AUTO REFRESH
=========================================================== */

const dashboardRefreshInterval = setInterval(

    refreshDashboard,

    60000

);
/* ===========================================================
   PART 4
   FINAL UTILITIES & INITIALIZATION
=========================================================== */

/* ===========================================================
   EXPORT CHAT
=========================================================== */

function exportChat() {

    if (!chatBody) return;

    const messages = Array.from(

        chatBody.querySelectorAll(".message-content")

    )

    .map(item => item.innerText)

    .join("\n\n----------------------------------------\n\n");

    const blob = new Blob(

        [messages],

        {

            type: "text/plain;charset=utf-8"

        }

    );

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;

    link.download =

        `Finacle_AI_Chat_${new Date().toISOString().slice(0,10)}.txt`;

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

    URL.revokeObjectURL(url);

    showToast(

        "Conversation exported successfully.",

        "success"

    );

}

/* ===========================================================
   COPY MESSAGE
=========================================================== */

async function copyMessage(text) {

    try {

        await navigator.clipboard.writeText(text);

        showToast(

            "Copied to clipboard.",

            "success"

        );

    }

    catch (error) {

        console.error(error);

    }

}

/* ===========================================================
   OPTIONAL BUTTONS
=========================================================== */

const exportButton =

    document.getElementById("exportChat");

if (exportButton) {

    exportButton.addEventListener(

        "click",

        exportChat

    );

}

/* ===========================================================
   CONNECTION TEST
=========================================================== */

async function testConnection() {

    try {

        const response =

            await fetch(API.testUrl);

        const result =

            await response.json();

        console.log(

            "AI Status:",

            result

        );

    }

    catch (error) {

        console.error(

            "Unable to connect to AI service.",

            error

        );

    }

}

/* ===========================================================
   STARTUP TASKS
=========================================================== */

testConnection();

/* ===========================================================
   GLOBAL FUNCTIONS
=========================================================== */

window.refreshDashboard = refreshDashboard;

window.clearHistory = clearHistory;

window.exportChat = exportChat;

window.copyMessage = copyMessage;

/* ===========================================================
   END OF FILE
=========================================================== */

console.log(

`

=========================================================

          FINACLE AI ASSISTANT LOADED

=========================================================

Modules Loaded

✓ Chat Engine

✓ Gemini Integration

✓ Dashboard Analytics

✓ Summary Cards

✓ Monthly Trend Chart

✓ Category Chart

✓ Prompt Buttons

✓ Conversation History

✓ Auto Refresh

✓ Export Chat

✓ Keyboard Shortcuts

Status : READY

=========================================================

`

);
