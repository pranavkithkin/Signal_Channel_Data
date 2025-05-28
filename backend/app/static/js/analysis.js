let selectedSession = null;

async function loadAnalysis(sessionName) {
  if (!sessionName) return;
  selectedSession = sessionName;
  document.getElementById('analysisResults').innerText = "Loading analysis for " + sessionName + "...";
  await renderGainDistributionChart(sessionName, document.getElementById('gainDistRange').value);
  await renderDrawdownDistributionChart(sessionName, document.getElementById('drawdownDistRange').value);
  await renderSignalsTable(sessionName);
}

// --- Chart rendering functions ---

async function renderGainDistributionChart(sessionName, range) {
  if (!sessionName) return;
  range = range || 1;
  const res = await fetch(`/api/chart/${sessionName}/gain_distribution?range=${range}`);
  const data = await res.json();
  if (data.error) {
      alert(data.error);
      return;
  }
  const ctx = document.getElementById('gainDistChart').getContext('2d');
  if (window.gainDistChartInstance) {
      window.gainDistChartInstance.destroy();
  }
  window.gainDistChartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
          labels: data.map((_, i) => i + 1),
          datasets: [{
              label: 'Gain (%)',
              data: data,
              backgroundColor: '#2196f3'
          }]
      },
      options: {
          responsive: true,
          plugins: {
              legend: { display: false },
              title: { display: true, text: 'Gain Distribution' }
          },
          scales: {
              y: { beginAtZero: true }
          }
      }
  });
}

async function renderDrawdownDistributionChart(sessionName, range) {
  if (!sessionName) return;
  range = range || 1;
  const res = await fetch(`/api/chart/${sessionName}/drawdown_distribution?range=${range}`);
  const data = await res.json();
  if (data.error) {
    alert(data.error);
    return;
  }
  const ctx = document.getElementById('drawdownDistChart').getContext('2d');
  if (window.drawdownDistChartInstance) {
    window.drawdownDistChartInstance.destroy();
  }
  window.drawdownDistChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.coins,
      datasets: [{
        label: 'Drawdown (%)',
        data: data.drawdowns,
        backgroundColor: '#e57373'
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { display: true, text: 'Drawdown Distribution' },
        tooltip: {
          callbacks: {
            label: function(context) {
              const coin = context.label;
              const value = context.parsed.y;
              return `${coin}: ${value}%`;
            }
          }
        }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}

// --- Signals Table ---

async function renderSignalsTable(sessionName) {
  if (!sessionName) return;
  const res = await fetch(`/api/session/${sessionName}`);
  const data = await res.json();
  if (data.error) {
    document.getElementById('signalsTableContainer').style.display = 'none';
    return;
  }
  const tbody = document.querySelector('#signalsTable tbody');
  tbody.innerHTML = '';
  data.forEach(row => {
    // Parse date/time
    const dt = new Date(row.timestamp);
    const date = dt.toLocaleDateString();
    const time = dt.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    tbody.innerHTML += `
      <tr>
        <td>${date}</td>
        <td>${time}</td>
        <td>${row.coin || ''}</td>
        <td>${row.entry_price || ''}</td>
        <td>${row.TP_price || ''}</td>
        <td>${row.SL_price || ''}</td>
        <td>${row.outcome || ''}</td>
      </tr>
    `;
  });
  document.getElementById('signalsTableContainer').style.display = '';
}

// --- Placeholder button actions ---

function optimizeStopLoss() {
  alert("Stop-loss optimization not yet implemented.");
}

function suggestTargets() {
  alert("Target suggestion not yet implemented.");
}