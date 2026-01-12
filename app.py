from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import joblib

app = FastAPI()

model = joblib.load("student_score_model.pkl")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>Student Score Prediction</h2>
    <p>Go to <a href="/ui">/ui</a> for input form, or <a href="/docs">/docs</a> for Swagger UI.</p>
    """

@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Student Score Prediction</title>
      <style>
        :root{
          --bg: #0b1220;
          --card: rgba(255,255,255,0.08);
          --card2: rgba(255,255,255,0.06);
          --text: rgba(255,255,255,0.92);
          --muted: rgba(255,255,255,0.65);
          --border: rgba(255,255,255,0.14);
          --shadow: 0 18px 60px rgba(0,0,0,0.45);
          --radius: 16px;
        }

        * { box-sizing: border-box; }
        body{
          margin:0;
          font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
          background:
            radial-gradient(900px 600px at 10% 10%, rgba(56,189,248,0.25), transparent 60%),
            radial-gradient(900px 600px at 90% 20%, rgba(99,102,241,0.25), transparent 55%),
            radial-gradient(900px 600px at 40% 90%, rgba(34,197,94,0.18), transparent 60%),
            var(--bg);
          color: var(--text);
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 28px;
        }

        .container{
          width: min(980px, 100%);
          display: grid;
          grid-template-columns: 1.1fr 0.9fr;
          gap: 18px;
        }

        @media (max-width: 860px){
          .container{ grid-template-columns: 1fr; }
        }

        .card{
          background: linear-gradient(180deg, var(--card), var(--card2));
          border: 1px solid var(--border);
          border-radius: var(--radius);
          box-shadow: var(--shadow);
          overflow: hidden;
          backdrop-filter: blur(10px);
        }

        .header{
          padding: 18px 18px 14px 18px;
          border-bottom: 1px solid var(--border);
        }

        .title{
          font-size: 20px;
          font-weight: 700;
          letter-spacing: 0.2px;
          margin: 0 0 6px 0;
        }

        .subtitle{
          margin: 0;
          color: var(--muted);
          font-size: 13px;
          line-height: 1.35;
        }

        .content{ padding: 18px; }

        .grid{
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 14px;
        }

        @media (max-width: 520px){
          .grid{ grid-template-columns: 1fr; }
        }

        label{
          display: block;
          font-size: 12px;
          color: var(--muted);
          margin-bottom: 6px;
        }

        .input{
          width: 100%;
          padding: 12px 12px;
          border-radius: 12px;
          border: 1px solid var(--border);
          background: rgba(255,255,255,0.06);
          color: var(--text);
          outline: none;
          transition: border 120ms ease, background 120ms ease;
        }

        .input:focus{
          border-color: rgba(56,189,248,0.7);
          background: rgba(255,255,255,0.09);
        }

        .row{
          margin-top: 16px;
          display:flex;
          gap: 10px;
          flex-wrap: wrap;
          align-items: center;
          justify-content: space-between;
        }

        .btn{
          appearance: none;
          border: 1px solid rgba(56,189,248,0.35);
          background: linear-gradient(180deg, rgba(56,189,248,0.25), rgba(99,102,241,0.18));
          color: var(--text);
          padding: 11px 14px;
          border-radius: 12px;
          font-weight: 650;
          cursor: pointer;
          transition: transform 80ms ease, opacity 120ms ease, border 120ms ease;
          min-width: 160px;
        }

        .btn:hover{ transform: translateY(-1px); border-color: rgba(56,189,248,0.55); }
        .btn:active{ transform: translateY(0px); opacity: 0.92; }
        .btn:disabled{ opacity: 0.55; cursor: not-allowed; transform: none; }

        .ghost{
          border: 1px solid var(--border);
          background: rgba(255,255,255,0.05);
          min-width: 140px;
        }

        .hint{
          color: var(--muted);
          font-size: 12px;
        }

        .resultBox{
          padding: 14px;
          border-radius: 14px;
          border: 1px solid var(--border);
          background: rgba(255,255,255,0.06);
        }

        .big{
          font-size: 34px;
          font-weight: 800;
          margin: 2px 0 6px 0;
          letter-spacing: 0.2px;
        }

        .pill{
          display: inline-flex;
          align-items: center;
          gap: 8px;
          padding: 8px 10px;
          border-radius: 999px;
          background: rgba(255,255,255,0.06);
          border: 1px solid var(--border);
          font-size: 12px;
          color: var(--muted);
        }

        .ok{ color: rgba(34,197,94,0.95); }
        .bad{ color: rgba(239,68,68,0.95); }

        .footerLinks{
          margin-top: 12px;
          display:flex;
          gap: 12px;
          flex-wrap: wrap;
        }
        a{ color: rgba(56,189,248,0.95); text-decoration: none; }
        a:hover{ text-decoration: underline; }

        .toast{
          margin-top: 12px;
          font-size: 12px;
          color: var(--muted);
          min-height: 18px;
        }
      </style>
    </head>

    <body>
      <div class="container">
        <!-- Left: Form -->
        <div class="card">
          <div class="header">
            <h1 class="title">Student Score Prediction</h1>
            <p class="subtitle">
              Enter study and sleep habits, plus absence days. The model returns a predicted final score (0–10).
            </p>
          </div>

          <div class="content">
            <div class="grid">
              <div>
                <label for="study_hours">Study hours (per day)</label>
                <input id="study_hours" class="input" type="number" step="0.1" min="0" max="24" value="6">
              </div>

              <div>
                <label for="sleep_hours">Sleep hours (per day)</label>
                <input id="sleep_hours" class="input" type="number" step="0.1" min="0" max="24" value="7">
              </div>

              <div style="grid-column: 1 / -1;">
                <label for="absence_days">Absence days (per term)</label>
                <input id="absence_days" class="input" type="number" step="1" min="0" max="60" value="2">
              </div>
            </div>

            <div class="row">
              <button id="predictBtn" class="btn" onclick="predict()">Predict</button>
              <button class="btn ghost" onclick="resetForm()">Reset</button>
              <div class="hint">Tip: try changing absence days to see impact.</div>
            </div>

            <div class="toast" id="toast"></div>

            <div class="footerLinks">
              <span class="pill">API: <code>/predict</code></span>
              <a href="/docs" target="_blank" rel="noreferrer">Open Swagger Docs</a>
              <a href="/" target="_blank" rel="noreferrer">Home</a>
            </div>
          </div>
        </div>

        <!-- Right: Result -->
        <div class="card">
          <div class="header">
            <h2 class="title" style="font-size:16px; margin:0 0 6px 0;">Prediction</h2>
            <p class="subtitle">Output from your saved model (<code>student_score_model.pkl</code>).</p>
          </div>

          <div class="content">
            <div class="resultBox">
              <div class="pill" id="statusPill">Status: <span class="ok">Ready</span></div>
              <div class="big" id="scoreText">—</div>
              <div class="subtitle" id="detailText">Enter inputs and click Predict.</div>
            </div>
          </div>
        </div>
      </div>

      <script>
        function setToast(msg, isError=false){
          const el = document.getElementById("toast");
          el.innerHTML = isError ? ('<span class="bad">' + msg + '</span>') : msg;
        }

        function setLoading(isLoading){
          const btn = document.getElementById("predictBtn");
          btn.disabled = isLoading;
          btn.innerText = isLoading ? "Predicting..." : "Predict";
          const pill = document.getElementById("statusPill");
          pill.innerHTML = "Status: " + (isLoading ? "<span>Running</span>" : "<span class='ok'>Ready</span>");
        }

        function resetForm(){
          document.getElementById("study_hours").value = 6;
          document.getElementById("sleep_hours").value = 7;
          document.getElementById("absence_days").value = 2;
          document.getElementById("scoreText").innerText = "—";
          document.getElementById("detailText").innerText = "Enter inputs and click Predict.";
          document.getElementById("statusPill").innerHTML = "Status: <span class='ok'>Ready</span>";
          setToast("");
        }

        function validateInputs(study, sleep, absence){
          if (Number.isNaN(study) || Number.isNaN(sleep) || Number.isNaN(absence)) {
            return "Please enter valid numbers.";
          }
          if (study < 0 || study > 24) return "Study hours should be between 0 and 24.";
          if (sleep < 0 || sleep > 24) return "Sleep hours should be between 0 and 24.";
          if (!Number.isInteger(absence) || absence < 0 || absence > 60) {
            return "Absence days should be an integer between 0 and 60.";
          }
          return null;
        }

        async function predict() {
          const study = Number(document.getElementById("study_hours").value);
          const sleep = Number(document.getElementById("sleep_hours").value);
          const absence = Number(document.getElementById("absence_days").value);

          const err = validateInputs(study, sleep, absence);
          if (err){
            setToast(err, true);
            return;
          }

          setToast("");
          setLoading(true);

          try{
            const res = await fetch("/predict", {
              method: "POST",
              headers: {"Content-Type": "application/json"},
              body: JSON.stringify({study_hours: study, sleep_hours: sleep, absence_days: absence})
            });

            const data = await res.json();

            if (!res.ok){
              document.getElementById("scoreText").innerText = "Error";
              document.getElementById("detailText").innerText = JSON.stringify(data);
              setToast("Request failed. Check server logs.", true);
              document.getElementById("statusPill").innerHTML = "Status: <span class='bad'>Error</span>";
              return;
            }

            document.getElementById("scoreText").innerText = data.predicted_score;
            document.getElementById("detailText").innerText =
              `Using inputs: study=${study}, sleep=${sleep}, absence=${absence}`;

            document.getElementById("statusPill").innerHTML = "Status: <span class='ok'>Success</span>";
          } catch (e){
            document.getElementById("scoreText").innerText = "Error";
            document.getElementById("detailText").innerText = String(e);
            setToast("Cannot reach /predict. Is the server running?", true);
            document.getElementById("statusPill").innerHTML = "Status: <span class='bad'>Error</span>";
          } finally {
            setLoading(false);
          }
        }
      </script>
    </body>
    </html>
    """


@app.post("/predict")
def predict_score(data: dict):
    study_hours = float(data["study_hours"])
    sleep_hours = float(data["sleep_hours"])
    absence_days = int(data["absence_days"])

    pred = model.predict([[study_hours, sleep_hours, absence_days]])
    return {"predicted_score": round(pred[0], 2)}
