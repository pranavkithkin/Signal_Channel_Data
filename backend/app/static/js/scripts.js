const runSimulationBtn = document.getElementById('runSimulationBtn');
const resultsDiv = document.getElementById('results');
const totalTradesSpan = document.getElementById('totalTrades');
const winningTradesSpan = document.getElementById('winningTrades');
const accuracySpan = document.getElementById('accuracy');
const netGainSpan = document.getElementById('netGain');
const equityChartCtx = document.getElementById('equityChart').getContext('2d');

let equityChart;  // Chart.js instance

async function runSimulation() {
  const stopLoss = document.getElementById('stopLoss').value;
  const takeProfit = document.getElementById('takeProfit').value;
  const riskPerTrade = document.getElementById('riskPerTrade').value;

  const url = `/api/simulate?stop_loss_pct=${stopLoss}&take_profit_pct=${takeProfit}&risk_per_trade_pct=${riskPerTrade}`;

  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Error: ${response.statusText}`);

    const data = await response.json();

    // Show results
    resultsDiv.classList.remove('hidden');
    totalTradesSpan.textContent = data.total_trades;
    winningTradesSpan.textContent = data.winning_trades;
    accuracySpan.textContent = data.accuracy;
    netGainSpan.textContent = data.net_gain_pct;

    drawEquityChart(data.equity_curve);
  } catch (err) {
    alert(`Failed to run simulation: ${err.message}`);
  }
}

function drawEquityChart(equityCurve) {
  if (equityChart) equityChart.destroy();

  equityChart = new Chart(equityChartCtx, {
    type: 'line',
    data: {
      labels: equityCurve.map((_, i) => i),
      datasets: [{
        label: 'Equity Curve',
        data: equityCurve,
        borderColor: 'green',
        fill: false,
        tension: 0.1,
      }]
    },
    options: {
      scales: {
        x: { title: { display: true, text: 'Trade Number' }},
        y: { title: { display: true, text: 'Equity' }},
      }
    }
  });
}

runSimulationBtn.addEventListener('click', runSimulation);
