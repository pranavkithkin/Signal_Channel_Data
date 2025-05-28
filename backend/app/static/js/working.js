async function loadSession(sessionName) {
    if (!sessionName) return;
    const res = await fetch(`/api/session/${sessionName}`);
    const data = await res.json();

    const sessionDataDiv = document.getElementById('sessionData');
    sessionDataDiv.innerText = ""; // Clear previous content

    if (data.error) {
        sessionDataDiv.innerText = data.error;
        sessionDataDiv.style.color = "red";
        return;
    }

    sessionDataDiv.style.color = "black";
    sessionDataDiv.innerText = JSON.stringify(data.slice(0, 5), null, 2) + (data.length > 5 ? '\n...' : '');

    // Render the equity curve chart
    await renderEquityCurve(sessionName);

    // Render the win/loss chart
    await renderWinLossChart(sessionName);
}

async function renderEquityCurve(sessionName) {
    const res = await fetch(`/api/chart/${sessionName}/equity_curve`);
    const data = await res.json();
    const ctx = document.getElementById('equityChart').getContext('2d');
    if (window.equityChartInstance) {
        window.equityChartInstance.destroy();
    }
    window.equityChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.timestamps,
            datasets: [{
                label: 'Equity Curve',
                data: data.equity,
                borderColor: 'blue',
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { display: true, title: { display: true, text: 'Date' } },
                y: { display: true, title: { display: true, text: 'Account Value ($)' } }
            }
        }
    });
}

async function renderWinLossChart(sessionName) {
    const res = await fetch(`/api/chart/${sessionName}/win_loss`);
    const data = await res.json();
    const ctx = document.getElementById('winLossChart').getContext('2d');
    if (window.winLossChartInstance) {
        window.winLossChartInstance.destroy();
    }
    const labels = Object.keys(data);
    const colors = labels.map(label => label === 'Win' ? '#4caf50' : '#f44336');
    window.winLossChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Count',
                data: Object.values(data),
                backgroundColor: colors
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                title: { display: true, text: 'Win/Loss Breakdown' }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}