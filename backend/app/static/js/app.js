document.getElementById('simForm').addEventListener('submit', async (e) => {
    e.preventDefault();
  
    const form = e.target;
    const stop_loss_pct = form.stop_loss_pct.value;
    const take_profit_pct = form.take_profit_pct.value;
    const risk_per_trade_pct = form.risk_per_trade_pct.value;
  
    const url = `http://localhost:8000/api/simulate?stop_loss_pct=${stop_loss_pct}&take_profit_pct=${take_profit_pct}&risk_per_trade_pct=${risk_per_trade_pct}`;
  
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`Error ${res.status}`);
  
      const data = await res.json();
      console.log(data);
  
      document.getElementById('results').style.display = 'block';
      document.getElementById('finalEquity').textContent = data.final_equity.toFixed(2);
      document.getElementById('netProfit').textContent = data.net_profit_pct.toFixed(2) + '%';
      document.getElementById('totalTrades').textContent = data.total_trades;
  
      renderChart(data.equity_curve);
    } catch (err) {
      alert('Failed to fetch simulation: ' + err.message);
    }
  });
  
  let chartInstance = null;
  function renderChart(dataPoints) {
    const ctx = document.getElementById('equityChart').getContext('2d');
  
    if (chartInstance) {
      chartInstance.destroy();
    }
  
    chartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: dataPoints.map((_, i) => i + 1),
        datasets: [{
          label: 'Equity Curve',
          data: dataPoints,
          borderColor: 'rgb(33, 150, 243)',
          backgroundColor: 'rgba(33, 150, 243, 0.2)',
          fill: true,
          tension: 0.1,
        }]
      },
      options: {
        responsive: true,
        scales: {
          x: { title: { display: true, text: 'Trade Number' } },
          y: { title: { display: true, text: 'Equity' } }
        }
      }
    });
  }
  