let trendChart = null;
let channelChart = null;


/* -----------------------------
   Utility Functions
----------------------------- */

function formatNumber(value) {
    const number = Number(value || 0);

    return new Intl.NumberFormat("en-IN", {
        maximumFractionDigits: 0
    }).format(number);
}


function formatCurrency(value) {
    const number = Number(value || 0);

    if (number >= 10000000) {
        return "₹" + (number / 10000000).toFixed(2) + " Cr";
    }

    if (number >= 100000) {
        return "₹" + (number / 100000).toFixed(2) + " L";
    }

    return "₹" + formatNumber(number);
}


function formatRevenue(value) {
    const number = Number(value || 0);

    if (number >= 1000000000) {
        return "₹" + (number / 1000000000).toFixed(2) + "B";
    }

    if (number >= 1000000) {
        return "₹" + (number / 1000000).toFixed(2) + "M";
    }

    return formatCurrency(number);
}


/* -----------------------------
   Dashboard KPI
----------------------------- */

async function loadDashboard() {

    const response = await fetch("/api/dashboard");

    if (!response.ok) {
        throw new Error("Dashboard API request failed.");
    }

    const data = await response.json();

    document.getElementById("campaigns").textContent =
        formatNumber(data.campaigns);

    document.getElementById("active-campaigns").textContent =
        formatNumber(data.active_campaigns);

    document.getElementById("spend").textContent =
        formatCurrency(data.spend);

    document.getElementById("roas").textContent =
        data.roas + "x";

    document.getElementById("revenue").textContent =
        formatRevenue(data.revenue);

    document.getElementById("impressions").textContent =
        formatNumber(data.impressions);

    document.getElementById("clicks").textContent =
        formatNumber(data.clicks);

    document.getElementById("ctr").textContent =
        data.ctr + "%";

    document.getElementById("cpc").textContent =
        "₹" + data.cpc;

    document.getElementById("advertisers").textContent =
        formatNumber(data.advertisers);
}


/* -----------------------------
   Performance Trends
----------------------------- */

async function loadTrendChart() {

    const response = await fetch("/api/analytics/trends");

    if (!response.ok) {
        throw new Error("Trend API request failed.");
    }

    const data = await response.json();

    const labels = data.map(item => item.date);

    const revenue = data.map(item => Number(item.revenue));
    const spend = data.map(item => Number(item.spend));

    const ctx = document
        .getElementById("trendChart")
        .getContext("2d");

    if (trendChart) {
        trendChart.destroy();
    }

    trendChart = new Chart(ctx, {

        type: "line",

        data: {
            labels: labels,

            datasets: [
                {
                    label: "Revenue",

                    data: revenue,

                    borderColor: "#7c5cff",

                    backgroundColor: "rgba(124, 92, 255, 0.10)",

                    fill: true,

                    tension: 0.35,

                    pointRadius: 0,

                    borderWidth: 2
                },

                {
                    label: "Spend",

                    data: spend,

                    borderColor: "#4fd1c5",

                    backgroundColor: "transparent",

                    fill: false,

                    tension: 0.35,

                    pointRadius: 0,

                    borderWidth: 1.5
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
                    display: true,

                    labels: {
                        color: "#8993a5",
                        font: {
                            size: 10
                        }
                    }
                }

            },

            scales: {

                x: {
                    grid: {
                        display: false
                    },

                    ticks: {
                        color: "#5f6879",
                        maxTicksLimit: 8,
                        font: {
                            size: 9
                        }
                    }
                },

                y: {
                    grid: {
                        color: "rgba(255,255,255,0.04)"
                    },

                    ticks: {

                        color: "#5f6879",

                        font: {
                            size: 9
                        },

                        callback: function(value) {

                            if (value >= 1000000000) {
                                return "₹" +
                                    (value / 1000000000).toFixed(1) +
                                    "B";
                            }

                            if (value >= 1000000) {
                                return "₹" +
                                    (value / 1000000).toFixed(0) +
                                    "M";
                            }

                            return value;
                        }
                    }
                }

            }
        }
    });
}


/* -----------------------------
   Channel Chart
----------------------------- */

async function loadChannelChart() {

    const response =
        await fetch("/api/analytics/channel-performance");

    if (!response.ok) {
        throw new Error("Channel API request failed.");
    }

    const data = await response.json();

    const labels = data.map(item => item.channel);

    const spend = data.map(item => Number(item.spend));

    const ctx = document
        .getElementById("channelChart")
        .getContext("2d");

    if (channelChart) {
        channelChart.destroy();
    }

    channelChart = new Chart(ctx, {

        type: "doughnut",

        data: {

            labels: labels,

            datasets: [
                {
                    data: spend,

                    backgroundColor: [
                        "#7c5cff",
                        "#4fd1c5",
                        "#5c8cff",
                        "#d47cff",
                        "#ff8c69",
                        "#69a7ff",
                        "#7fdc8b"
                    ],

                    borderColor: "#10151f",

                    borderWidth: 3
                }
            ]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            cutout: "68%",

            plugins: {

                legend: {

                    position: "bottom",

                    labels: {
                        color: "#8993a5",
                        boxWidth: 10,
                        padding: 12,
                        font: {
                            size: 9
                        }
                    }
                }

            }
        }
    });
}


/* -----------------------------
   Campaign Performance
----------------------------- */

async function loadCampaigns() {

    const response =
        await fetch("/api/analytics/campaign-performance");

    if (!response.ok) {
        throw new Error("Campaign API request failed.");
    }

    const data = await response.json();

    const table =
        document.getElementById("campaign-table-body");

    table.innerHTML = "";

    data.slice(0, 10).forEach(campaign => {

        const status =
            String(campaign.status || "").toLowerCase();

        let statusClass = "status-completed";

        if (status === "active") {
            statusClass = "status-active";
        }

        if (status === "paused") {
            statusClass = "status-paused";
        }

        if (status === "scheduled") {
            statusClass = "status-scheduled";
        }

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>
                <strong>${campaign.campaign_name}</strong>
            </td>

            <td>
                <span class="status-pill ${statusClass}">
                    ${campaign.status}
                </span>
            </td>

            <td>
                ${campaign.ctr}%
            </td>

            <td>
                ${formatCurrency(campaign.spend)}
            </td>

            <td>
                ${formatRevenue(campaign.revenue)}
            </td>

            <td>
                <strong>${campaign.roas}x</strong>
            </td>
        `;

        table.appendChild(row);
    });


    const campaignList =
        document.getElementById("campaign-list");

    campaignList.innerHTML = "";

    data.slice(0, 5).forEach((campaign, index) => {

        const row = document.createElement("div");

        row.className = "campaign-row";

        row.innerHTML = `
            <div>
                <div class="campaign-name">
                    ${index + 1}. ${campaign.campaign_name}
                </div>
            </div>

            <div class="campaign-value">
                ${formatRevenue(campaign.revenue)}
            </div>
        `;

        campaignList.appendChild(row);
    });
}


/* -----------------------------
   Location Performance
----------------------------- */

async function loadLocations() {

    const response =
        await fetch("/api/analytics/location-performance");

    if (!response.ok) {
        throw new Error("Location API request failed.");
    }

    const data = await response.json();

    const container =
        document.getElementById("location-list");

    container.innerHTML = "";

    const maxRevenue =
        Math.max(...data.map(item => Number(item.revenue)));

    data.slice(0, 6).forEach(location => {

        const percentage =
            (Number(location.revenue) / maxRevenue) * 100;

        const row =
            document.createElement("div");

        row.className = "location-row";

        row.innerHTML = `
            <div>
                <div class="location-name">
                    ${location.city}, ${location.state}
                </div>

                <div class="location-bar">
                    <span style="width:${percentage}%"></span>
                </div>
            </div>

            <div class="location-value">
                ${formatRevenue(location.revenue)}
            </div>
        `;

        container.appendChild(row);
    });
}


/* -----------------------------
   Application
----------------------------- */

async function initializeDashboard() {

    try {

        await Promise.all([
            loadDashboard(),
            loadTrendChart(),
            loadChannelChart(),
            loadCampaigns(),
            loadLocations()
        ]);

        console.log("Aurelytix dashboard loaded successfully.");

    } catch (error) {

        console.error(
            "Aurelytix dashboard initialization failed:",
            error
        );

    }
}


document.addEventListener(
    "DOMContentLoaded",
    initializeDashboard
);