# Consentify
🧠 Consentify — AI-powered Privacy Policy Analyzer &amp; Consent Verifier. Transform complex privacy policies into clear insights. Detect risks, track consent violations, and empower users to understand how their data is used — all in one intuitive dashboard.

Consentify is an MVP project designed to simplify and demystify privacy policies.
Using advanced AI models (Gemini + OpenAI), it scans, interprets, and summarizes terms & privacy policies to show:

What data is collected
How it’s used
Who it’s shared with
Whether user consent truly aligns with the policy
🚀 Features
✅ AI-Powered Policy Analysis — Automatically scans privacy policies and highlights risky or confusing sections.
✅ Consent Risk Detection — Flags data usage practices that go beyond user-granted permissions.
✅ Smart Summarization — Converts long, complex legal text into concise, human-readable summaries.
✅ Visual Risk Dashboard — Displays risk scores, compliance tags (e.g., GDPR, CCPA), and data-sharing levels.
✅ User Rights Check — Detects whether the document respects user rights like “Delete my data”, “Opt-out”, etc.
✅ MVP-Ready Frontend — Clean UI built for user testing and feedback collection.

🧠 How It Works
User uploads or pastes a Privacy Policy / Terms of Service.
The system parses and sends the text to the Gemini AI model.
The model:
Extracts and labels policy clauses (Data Collection, Usage, Third-party Sharing, Rights, etc.).
Detects potential risks or consent mismatches.
The backend compiles results and returns:
A risk summary
A section-wise explanation
A visual consent alignment score

⚙️ Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/Rudrakshsharmaa/Consentify
cd Consentify
2️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
# or if using npm for frontend
npm install
3️⃣ Set Up Environment Variables
Create a .env file and add your keys:
4️⃣ Run the App
bash
Copy code
python app.py
# or if frontend
npm run dev

🧪 Example Use Case
Upload this sample privacy policy:

“We collect your location data and share it with analytics partners to improve services…”

Consentify Output:

Risk Level: 🔴 High

Detected Issues: Third-party sharing without explicit opt-in

Recommendation: Add user consent confirmation before sharing data externally

🧩 Future Enhancements
🧾 Policy-to-Policy Comparison

🧑‍⚖️ Compliance Checker (GDPR / CCPA auto-validation)

🔒 Privacy-preserving AI mode (no raw text stored)

🌐 Browser Extension for real-time website checks

💡 Vision
To make digital consent transparent, actionable, and privacy-first.
