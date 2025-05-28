document.getElementById('extractForm').onsubmit = async function(e) {
    e.preventDefault();
    const form = e.target;
    const data = new FormData(form);
    const res = await fetch(form.action, { method: 'POST', body: data });
    const json = await res.json();
    document.getElementById('extractResult').innerText = json.message || json.error;
  };