from flask import Flask, request, jsonify, render_template_string
import os
import google.generativeai as genai
from flask_cors import CORS
from dotenv import load_dotenv
import json, re

# ---------------- Setup ----------------
load_dotenv()
genai.configure(api_key="AIzaSyDrTCqks5M8MXjdBnLfagCelAn6dfyzQVE")

app = Flask(__name__)
CORS(app)

# ---------------- Template ----------------
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Consentify — Privacy Risk Scanner</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    * { box-sizing: border-box; font-family: 'Poppins', sans-serif; }

    body {
      margin: 0; padding: 0;
      background-color: #b4b873;
      display: flex; justify-content: center; align-items: center;
      min-height: 100vh;
      transition: 0.4s ease background-color, color;
      overflow-x: hidden;
    }
    body.dark { background-color: #1a1a1a; color: #e5e5e5; }

    .bg-icon {
      position: absolute;
      opacity: 0.08;
      filter: drop-shadow(0 0 3px #4a6f41);
      z-index: 0;
      pointer-events: none;
      animation: float 6s ease-in-out infinite alternate;
    }
    .bg-icon.lock { top: 10%; left: 10%; font-size: 80px; }
    .bg-icon.shield { bottom: 8%; right: 10%; font-size: 90px; animation-delay: 2s; }
    .bg-icon.brain { top: 60%; left: 5%; font-size: 100px; animation-delay: 1s; }
    @keyframes float { from { transform: translateY(0); } to { transform: translateY(15px); } }

    .card {
      position: relative;
      background-color: #fdf7e2;
      border-radius: 20px;
      padding: 40px 30px;
      width: 90%; max-width: 850px;
      z-index: 10;
      box-shadow: 0 10px 25px rgba(0,0,0,0.25);
      overflow: hidden;
      animation: fadeIn 1s ease;
    }
    body.dark .card { background-color: #2a2a2a; color: #f1f1f1; }

    @keyframes fadeIn { from {opacity: 0; transform: translateY(15px);} to {opacity: 1; transform: translateY(0);} }

    .header {
      display: flex; align-items: center; justify-content: center;
      gap: 12px; flex-direction: column;
    }
    .header h1 {
      font-family: 'Georgia', serif;
      font-size: 2.8rem;
      color: #1f3d23;
      margin: 0;
      display: flex; align-items: center; gap: 6px;
    }
    .header p { font-size: 1rem; color: #374151; text-align: center; margin: 6px 0 20px; }
    body.dark .header h1 { color: #d8e0cf; }
    body.dark .header p { color: #d3d3d3; }

    .theme-toggle {
      position: absolute;
      top: 20px; right: 20px;
      background: #3f613a;
      color: #fff; border: none;
      border-radius: 50%;
      width: 38px; height: 38px;
      font-size: 18px; cursor: pointer;
      transition: 0.3s;
    }
    .theme-toggle:hover { transform: rotate(20deg); background: #284628; }

    textarea {
      width: 100%;
      min-height: 180px;
      border: 2px solid #d6cfa5;
      border-radius: 10px;
      padding: 12px;
      font-size: 15px;
      background-color: #fffdf5;
      resize: vertical;
      transition: 0.2s ease;
    }
    body.dark textarea { background-color: #3c3c3c; color: #fff; border-color: #555; }
    textarea:focus { outline: none; border-color: #476b43; box-shadow: 0 0 5px rgba(71,107,67,0.4); }

    button.analyze {
      margin-top: 18px;
      padding: 12px 20px;
      background-color: #3f613a;
      border: none;
      color: #fff;
      font-weight: bold;
      border-radius: 8px;
      font-size: 15px;
      cursor: pointer;
      width: 100%;
      transition: 0.3s ease;
      display: flex; align-items: center; justify-content: center;
      gap: 8px;
    }
    button.analyze:hover { background-color: #264526; transform: translateY(-2px); }

    .loader { display: none; text-align: center; margin-top: 20px; }
    .dot {
      height: 10px; width: 10px; margin: 0 4px;
      background-color: #3f613a;
      border-radius: 50%; display: inline-block;
      animation: bounce 1.4s infinite ease-in-out both;
    }
    @keyframes bounce {
      0%, 80%, 100% { transform: scale(0); }
      40% { transform: scale(1); }
    }
    .dot:nth-child(1) { animation-delay: -0.32s; }
    .dot:nth-child(2) { animation-delay: -0.16s; }

    .result {
      margin-top: 25px;
      background: #fffef6;
      padding: 20px;
      border-radius: 12px;
      border: 1px solid #e0d6a5;
      display: none;
      box-shadow: 0 0 15px rgba(63,97,58,0.2);
    }
    body.dark .result { background: #2e2e2e; border-color: #444; }

    .badge { display: inline-block; padding: 6px 14px; border-radius: 20px; font-weight: 600; color: white; }
    .badge.green { background: #3f613a; }
    .badge.yellow { background: #eab308; color: #222; }
    .badge.red { background: #b91c1c; }

    .tooltip { position: relative; display: inline-block; cursor: help; color: #476b43; margin-left: 5px; font-weight: bold; }
    .tooltip .tooltip-text {
      visibility: hidden;
      width: 200px; background-color: #333; color: #fff;
      text-align: left; border-radius: 6px; padding: 8px;
      position: absolute; bottom: 125%; left: 50%;
      margin-left: -100px; opacity: 0; transition: opacity 0.3s;
    }
    .tooltip:hover .tooltip-text { visibility: visible; opacity: 1; }

    .gauge {
      width: 120px; height: 120px; border-radius: 50%;
      margin: 15px auto;
      background: conic-gradient(#3f613a var(--val, 0%), #ddd 0);
      display: flex; align-items: center; justify-content: center;
      color: #1f3d23; font-weight: bold; font-size: 20px;
    }

    .tags {
      margin-top: 10px; display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;
    }
    .tag {
      background: #e0e8c3;
      border-radius: 14px;
      padding: 5px 12px;
      font-size: 13px; color: #1f3d23;
      display: flex; align-items: center; gap: 5px;
    }
    body.dark .tag { background: #444; color: #cce9ba; }
  </style>
</head>
<body>
  <div class="bg-icon lock">🔒</div>
  <div class="bg-icon shield">🛡️</div>
  <div class="bg-icon brain">🧠</div>

  <div class="card">
    <button class="theme-toggle" id="themeBtn">🌙</button>

    <div class="header">
      <h1>Consentify 🌿</h1>
      <p>AI-powered Privacy Risk Scanner for Terms of Service & Privacy Policies</p>
    </div>

    <textarea id="policy" placeholder="📜 Paste Privacy Policy or ToS here..."></textarea>
    <button class="analyze" id="analyzeBtn"><i>🔍</i> Analyze</button>

    <div class="loader" id="loader">
      <span class="dot"></span><span class="dot"></span><span class="dot"></span>
      <p style="color:#3f613a; font-size:14px; margin-top:6px;">Analyzing with Gemini...</p>
    </div>

    <div class="result" id="result"></div>
  </div>

  <script>
    const btn = document.getElementById('analyzeBtn');
    const loader = document.getElementById('loader');
    const resultDiv = document.getElementById('result');
    const textarea = document.getElementById('policy');
    const themeBtn = document.getElementById('themeBtn');

    themeBtn.addEventListener('click', () => {
      document.body.classList.toggle('dark');
      themeBtn.textContent = document.body.classList.contains('dark') ? '☀️' : '🌙';
    });

    btn.addEventListener('click', async () => {
      const text = textarea.value.trim();
      if (!text) { alert('Please paste a privacy policy first!'); return; }

      loader.style.display = 'block';
      resultDiv.style.display = 'none';

      const res = await fetch('/analyze', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({text})
      });
      const data = await res.json();

      loader.style.display = 'none';
      resultDiv.style.display = 'block';

      let badgeClass = 'green';
      if (data.score >= 70) badgeClass = 'red';
      else if (data.score >= 30) badgeClass = 'yellow';

      const keywords = data.summary.join(' ').split(' ')
        .filter((w,i,a)=>w.length>5 && a.indexOf(w)===i).slice(0,5);

      resultDiv.innerHTML = `
        <h3>Risk Score:
          <span class="badge ${badgeClass}">${data.score}</span>
          <span class="tooltip">👀
            <span class="tooltip-text">
              0–30 → Safe<br>
              31–69 → Moderate Risk<br>
              70+ → High Risk
            </span>
          </span>
        </h3>

        <div class="gauge" style="--val:${data.score}%">${data.score}%</div>

        <div class="tags">
          ${keywords.map(k=>`<span class='tag'><i></i>${k}</span>`).join('')}
        </div>

        <h4>📋 Summary</h4>
        <ul>${data.summary.map(s => `<li>${s}</li>`).join('')}</ul>

        <h4>🚨 Risky Clauses</h4>
        <ol>${data.highlights.map(h => `<li>${h.sentence} — <i>${h.reason}</i></li>`).join('')}</ol>

        ${data.note ? `<div class="note">${data.note}</div>` : ''}
      `;
    });
  </script>
</body>
</html>
"""

# ---------------- Routes ----------------
@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_PAGE)

@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.json.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    return jsonify(analyze_text_with_gemini(text))

# ---------------- Gemini Analyzer ----------------
def analyze_text_with_gemini(text: str):
    prompt = f"""
    You are a privacy policy risk analyzer.
    Respond ONLY with valid JSON in the following format:

    {{
      "summary": ["point1", "point2", "point3"],
      "highlights": [
        {{"sentence":"...", "reason":"..."}}
      ],
      "score": 0-100
    }}

    Policy Text:
    {text}
    """

    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)
        raw = response.text if hasattr(response, "text") else response.candidates[0].content.parts[0].text
        raw = raw.replace("```json", "").replace("```", "").strip()

        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            raw = match.group(0)

        return json.loads(raw)

    except Exception as e:
        return {
            "summary": ["May collect personal data", "Shares data with partners", "Lacks retention clarity"],
            "highlights": [
                {"sentence": "We may share your data with third parties.", "reason": "Unclear data sharing scope"},
                {"sentence": "We store your data indefinitely.", "reason": "No retention limit"}
            ],
            "score": 68,
            "note": f"⚠️ Used fallback (Gemini JSON error: {e})"
        }

# ---------------- Run ----------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)