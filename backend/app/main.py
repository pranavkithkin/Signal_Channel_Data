from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
from datetime import datetime
from services.extract_signals import extract_signals_from_channel
from services.plot_backtest_stats import (
    get_equity_curve_data,
    get_win_loss_data,
    get_gain_distribution_data,
    get_drawdown_distribution_data,
    get_coin_performance_data
)

app = Flask(__name__, static_folder="static", template_folder="templates")

# Directory for storing session CSVs
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
SESSIONS_DIR = os.path.join(APP_ROOT, "data", "sessions")
REQUIRED_COLUMNS = ['timestamp', 'coin', 'direction', 'raw_message']

def list_sessions():
    sessions = []
    print("Looking for sessions in:", SESSIONS_DIR)
    print("Files found:", os.listdir(SESSIONS_DIR))
    if not os.path.exists(SESSIONS_DIR):
        os.makedirs(SESSIONS_DIR)
    for fname in os.listdir(SESSIONS_DIR):
        if fname.endswith(".csv"):
            fpath = os.path.join(SESSIONS_DIR, fname)
            stat = os.stat(fpath)
            sessions.append({
                "name": fname.replace(".csv", ""),
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "path": fpath
            })
    sessions.sort(key=lambda x: x["modified"], reverse=True)
    print("Sessions found:", [s["name"] for s in sessions])
    return sessions

@app.template_filter('datetimeformat')
def datetimeformat(value):
    """Format timestamps for display in templates."""
    return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M')

# --- Navigation Routes ---

@app.route("/")
def home():
    sessions = list_sessions()
    return render_template("index.html", sessions=sessions)

@app.route("/working")
def working():
    sessions = list_sessions()
    return render_template("working.html", sessions=sessions)

@app.route("/analysis")
def analysis():
    sessions = list_sessions()
    return render_template("analysis.html", sessions=sessions)

# --- API Endpoints ---

@app.route("/api/extract_signals", methods=["POST"])
def extract_signals_api():
    try:
        channel_id = int(request.form["channel_id"])
        access_hash = int(request.form["access_hash"])
        months_back = int(request.form["months_back"])
        session_name = request.form.get("session_name")
        # Use a unique session name for Telethon session file
        telethon_session = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}" if not session_name else session_name

        signals_df = extract_signals_from_channel(channel_id, access_hash, months_back, session_name=telethon_session)
        if signals_df is None or signals_df.empty:
            return jsonify({"error": "No signals extracted."}), 400
        session_path = os.path.join(SESSIONS_DIR, f"{telethon_session}.csv")
        signals_df.to_csv(session_path, index=False)
        return jsonify({"message": "Signals extracted and session saved.", "session_name": telethon_session})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/sessions")
def get_sessions():
    sessions = list_sessions()
    # Format timestamps for frontend
    for s in sessions:
        s["created"] = datetimeformat(s["created"])
        s["modified"] = datetimeformat(s["modified"])
    return jsonify(sessions)

@app.route("/api/session/<session_name>")
def get_session_data(session_name):
    session_path = os.path.join(SESSIONS_DIR, f"{session_name}.csv")
    if not os.path.exists(session_path):
        return jsonify({"error": "Session not found."}), 404
    df = pd.read_csv(session_path)
    # Check if session is cleaned
    is_cleaned = all(col in df.columns for col in REQUIRED_COLUMNS)
    if not is_cleaned:
        return jsonify({"error": "Session is not cleaned. Please clean it before analysis."}), 400
    return jsonify(df.to_dict(orient="records"))

@app.route("/api/chart/<session_name>/equity_curve")
def api_equity_curve(session_name):
    session_path = os.path.join(SESSIONS_DIR, f"{session_name}.csv")
    if not os.path.exists(session_path):
        return jsonify({"error": "Session not found."}), 404
    df = pd.read_csv(session_path)
    return jsonify(get_equity_curve_data(df))

@app.route("/api/chart/<session_name>/win_loss")
def api_win_loss(session_name):
    session_path = os.path.join(SESSIONS_DIR, f"{session_name}.csv")
    if not os.path.exists(session_path):
        return jsonify({"error": "Session not found."}), 404
    df = pd.read_csv(session_path)
    return jsonify(get_win_loss_data(df))

@app.route("/api/chart/<session_name>/gain_distribution")
def api_gain_distribution(session_name):
    session_path = os.path.join(SESSIONS_DIR, f"{session_name}.csv")
    if not os.path.exists(session_path):
        return jsonify({"error": "Session not found."}), 404
    df = pd.read_csv(session_path)
    return jsonify(get_gain_distribution_data(df))

@app.route("/api/chart/<session_name>/drawdown_distribution")
def api_drawdown_distribution(session_name):
    session_path = os.path.join(SESSIONS_DIR, f"{session_name}.csv")
    if not os.path.exists(session_path):
        return jsonify({"error": "Session not found."}), 404
    df = pd.read_csv(session_path)
    return jsonify(get_drawdown_distribution_data(df))

@app.route("/api/chart/<session_name>/coin_performance")
def api_coin_performance(session_name):
    session_path = os.path.join(SESSIONS_DIR, f"{session_name}.csv")
    if not os.path.exists(session_path):
        return jsonify({"error": "Session not found."}), 404
    df = pd.read_csv(session_path)
    return jsonify(get_coin_performance_data(df))

# --- Placeholder for future analysis endpoints ---
# @app.route("/api/stop_loss_optimization", methods=["POST"])
# def stop_loss_optimization():
#     # Implement stop-loss optimization logic here
#     pass

# @app.route("/api/target_suggestion", methods=["POST"])
# def target_suggestion():
#     # Implement target suggestion logic here
#     pass

if __name__ == "__main__":
    app.run(debug=True, port=5000)