# AI-Powered Pension Life Certificate Assistance & Resubmission System

A beginner-friendly Python GenAI project using Streamlit, SQLite, and the current Google Gen AI SDK (`google-genai`). This application simulates the submission and verification of an annual pensioner Life Certificate, handles data mismatches, and uses Google Gemini to explain rejections and guide users through corrected resubmissions.

## Project Highlights
* **Real-life pension use case:** Simulates submission, verification, and rejection based on PPO (Pension Payment Order) or bank detail mismatches.
* **AI Assistance:** Uses the latest Google Gemini SDK to explain rejection reasons in simple language and answer general pension-related queries.
* **Notifications:** Prepares WhatsApp-style alerts and sends actual email notifications (via Gmail SMTP) upon rejection.
* **Database Tracking:** Uses SQLite to store registered master records and maintain a history of all submissions and resubmissions.

## Technology Stack
* **Frontend UI:** Streamlit
* **Backend & Logic:** Python 3.11+
* **Database:** SQLite (`sqlite3`) and Pandas (for data display)
* **AI Integration:** Google Gemini (`google-genai` package)
* **Utilities:** `python-dotenv` for environment variables, `smtplib` for email delivery

## Project Structure
```text
LifeCertificateAI/
├── app.py
├── database.py
├── seed_data.py
├── pensioner_service.py
├── verification_service.py
├── certificate_service.py
├── gemini_service.py
├── notification_service.py
├── email_service.py
├── requirements.txt
├── .env
├── .gitignore
└── database/
    └── pension.db (created automatically)
```

## Setup and Installation

**1. Create and activate a virtual environment**
```bash
mkdir LifeCertificateAI
cd LifeCertificateAI
python -m venv venv

# Windows CMD activation:
venv\Scripts\activate
# Windows PowerShell activation:
venv\Scripts\Activate.ps1
```

**2. Install required packages**
Create a `requirements.txt` file containing `streamlit`, `pandas`, `python-dotenv`, and `google-genai`. Then run:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install --upgrade google-genai
```

**3. Configure Environment Variables**
Create a `.env` file in the project root directory and add your API keys and email credentials:
```env
GEMINI_API_KEY=PASTE_YOUR_GOOGLE_AI_STUDIO_KEY_HERE
GEMINI_MODEL=gemini-3.8-flash
SENDER_EMAIL=yourgmail@gmail.com
SENDER_APP_PASSWORD=your_google_app_password
```
*Note: Use a Google App Password for the `SENDER_APP_PASSWORD`; do not use your normal Gmail password. Keep this file private and never commit it to version control.*

## Running the Application

Execute the following commands in order from your activated virtual environment:

1. **Create the database and tables:** 
   ```bash
   python database.py
   ```
2. **Insert fictional demo pensioner records:** 
   ```bash
   python seed_data.py
   ```
3. **Launch the Streamlit web interface:** 
   ```bash
   streamlit run app.py
   ```
   *The application will normally open in your browser at `http://localhost:8501`.*

## Testing Scenarios

You can test the application using the following dummy records:

| Test Scenario | PPO Number | Account Number | IFSC Code | Expected Demo Result |
| :--- | :--- | :--- | :--- | :--- |
| **Correct Details** | `PPO202400123` | `123456789012` | `SBIN0001234` | APPROVED |
| **Wrong PPO** | `PPO202400132` | `123456789012` | `SBIN0001234` | REJECTED PPO mismatch |
| **Wrong Account** | `PPO202400123` | `123456789999` | `SBIN0001234` | REJECTED account mismatch |

**Resubmission Flow:** Submit incorrect details to generate a rejection record, then return to the submission form, enter the correct details, and submit again. You can then navigate to the "AI Rejection Explanation" tab to ask Gemini to explain the earlier failure.

## Important Disclaimers & Production Safeguards

* **Educational Use Only:** This is a learning/demo application and is not connected to a government pension portal, bank verification network, or official Life Certificate service. 
* **Not Official Verification:** A demo APPROVED result is an evaluation of local dummy data and does not establish legal eligibility or represent official bank approval.
* **Data Privacy:** Do not store full real bank account or identity data in an unsecured demo database. Real-world deployments require user authentication, HTTPS, encrypted fields, and authorized APIs.
* **Simulated Systems:** The WhatsApp integration in this demo generates simulated text; real delivery requires an approved WhatsApp Business Platform integration.
