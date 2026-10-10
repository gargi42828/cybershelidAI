# 🛡️ CyberShield AI

### AI-Powered Cybersecurity Threat Detection Platform

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB.svg)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1.svg)](https://www.postgresql.org/)
[![Machine
Learning](https://img.shields.io/badge/AI-Machine%20Learning-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-Educational-green.svg)](#-license)

------------------------------------------------------------------------

## 📌 Project Overview

**CyberShield AI** is an AI-powered cybersecurity web application
designed to help identify potentially malicious URLs and provide a clear
view of scan results. It combines a machine-learning phishing detection
model with a FastAPI backend, a React dashboard, and a PostgreSQL
database.

The implemented workflow allows users to create an account, submit URLs
for analysis, review the predicted classification and risk level, and
view scan history and dashboard statistics.

> **Project status:** The phishing URL detection, authentication,
> scan-history/statistics APIs, and frontend integration are part of the
> current project implementation. Additional modules listed under Future
> Enhancements should be considered planned until they have been
> implemented and tested.

------------------------------------------------------------------------

## 🎯 Objective

The primary objective of CyberShield AI is to make basic cybersecurity
analysis more accessible by integrating machine learning with a
full-stack web application. The project aims to demonstrate how
suspicious URL patterns can be analyzed, how scan records can be managed
securely, and how results can be presented through an intuitive
dashboard.

------------------------------------------------------------------------

## 🚀 Key Features

-   🔍 **Phishing URL Detection** --- Classifies submitted URLs as
    *Phishing* or *Legitimate* using a trained ML model.
-   ⚠️ **Risk Assessment** --- Displays a risk level associated with the
    scan result.
-   🔐 **User Authentication** --- Provides registration and login
    functionality.
-   📊 **Security Dashboard** --- Summarizes scan activity and detection
    statistics.
-   🧾 **Scan History** --- Retrieves saved scan records for the
    authenticated user.
-   🧠 **Machine Learning Integration** --- Loads a trained model for
    URL classification.
-   🔌 **REST API** --- Uses FastAPI to connect the frontend, model, and
    database.
-   🗄️ **Database Integration** --- Uses PostgreSQL to persist user and
    scan information.
-   📘 **Interactive API Documentation** --- Supports endpoint testing
    through Swagger UI.
-   ⚛️ **React Web Interface** --- Provides the user-facing interface
    and dashboard.

------------------------------------------------------------------------

## 🏗️ Technical Architecture

### 🔹 System Workflow

1.  The user signs in to the web application.
2.  The user submits a URL for analysis.
3.  The React frontend sends the request to the FastAPI backend.
4.  The backend validates the input and prepares the features expected
    by the trained ML model.
5.  The model predicts whether the URL appears phishing-related or
    legitimate.
6.  The scan workflow assigns a risk level and records the result when
    configured.
7.  The dashboard retrieves scan history and statistics from the
    backend.

``` text
                 ┌──────────────────────┐
                 │        User          │
                 └──────────┬───────────┘
                            │
                 ┌──────────▼───────────┐
                 │ React + Vite Frontend│
                 └──────────┬───────────┘
                            │ HTTP / Axios
                 ┌──────────▼───────────┐
                 │    FastAPI Backend   │
                 └──────┬─────────┬─────┘
                        │         │
             ┌──────────▼──┐  ┌───▼────────────┐
             │ Trained ML  │  │  PostgreSQL    │
             │ Phishing    │  │ Users & Scans  │
             │ Model       │  └───┬────────────┘
             └──────┬──────┘      │
                    └──────┬──────┘
                 ┌─────────▼──────────┐
                 │ Prediction, Risk & │
                 │ Dashboard Results  │
                 └────────────────────┘
```

### 🔹 Backend

-   Built using **FastAPI**.
-   Provides authentication, URL scanning, scan history, and dashboard
    statistics endpoints.
-   Exposes interactive API documentation through Swagger UI.

### 🔹 Frontend

-   Built with **React and Vite**.
-   Uses **Axios** to communicate with the backend.
-   Presents authentication pages and dashboard information.

### 🔹 Database

-   Uses **PostgreSQL**.
-   Stores user information and scan records according to the configured
    schema.
-   Provides historical data for dashboard statistics.

------------------------------------------------------------------------

## 🧠 Machine Learning Model

The phishing detection module uses a trained classification model to
analyze features extracted from a submitted URL.

### 🔹 Model Workflow

-   **Input:** A URL submitted by the user.
-   **Feature extraction:** The backend prepares the URL features
    expected by the trained model.
-   **Prediction:** The model returns a classification.
-   **Risk mapping:** The application maps the prediction to a risk
    level.
-   **Output:** The result is returned to the frontend and can be stored
    for history and analytics.

### 🔹 Model Files

The model directory may include files such as:

``` text
ml_models/
├── phishing_url_model.joblib
└── phishing_model.joblib
```

Use the filename actually loaded by your current backend code. Include
the model file in GitHub only if it exists in your project and you are
permitted to redistribute it.

### 🔹 Model Evaluation

Evaluate the model on held-out test data and document:

-   Accuracy
-   Precision
-   Recall
-   F1-score
-   Confusion matrix

A model prediction is a warning signal, not a guarantee that a website
is safe or malicious. Report only metrics measured using your actual
evaluation code and test set.

------------------------------------------------------------------------

## 📊 Dataset Information

The phishing detection model was trained using a URL dataset with
labeled examples and URL-derived features.

-   **Task:** Binary URL classification
-   **Classes:** Phishing and legitimate
-   **Input:** URL-derived features
-   **Output:** Predicted class and application risk level

The training dataset used during development had approximately **235,795
rows and 55 columns** before the later feature/model workflow was
refined. The model workflow has also used a 28-feature version, so
verify which dataset and feature set correspond to the model file in
your final repository.

Add the dataset name, original source, license, preprocessing steps, and
train/test split details here. Do not upload restricted datasets or
sensitive records.

------------------------------------------------------------------------

## 📷 Project Output and Screenshots

Add screenshots of the **actual running CyberShield AI application** to
`docs/screenshots/`. These images help reviewers understand the
interface and verify the implemented workflow.

### 🔐 1. Login / Registration Page

![CyberShield AI Login Page](docs/screenshots/login.png)

*Capture the login or registration page.*

### 📊 2. Security Dashboard

![CyberShield AI Dashboard](docs/screenshots/dashboard.png)

*Capture the dashboard with the actual scan statistics returned by your
backend.*

### 🚨 3. Phishing URL Detection

![Phishing URL Detection Result](docs/screenshots/phishing-result.png)

*Capture a test URL classified as phishing, including the risk level
shown by the application.*

### ✅ 4. Legitimate URL Detection

![Legitimate URL Detection
Result](docs/screenshots/legitimate-result.png)

*Capture a legitimate URL prediction from your running application.*

### 🧾 5. Scan History and Statistics

![Scan History and Statistics](docs/screenshots/scan-history.png)

*Capture the scan-history page or the API response showing saved scan
statistics.*

### 🔌 6. FastAPI Swagger Documentation

![CyberShield AI API Documentation](docs/screenshots/api-docs.png)

*Capture the API documentation at `http://127.0.0.1:8000/docs` while the
backend is running.*

**How to add the screenshots**

Create this folder in your project:

``` text
docs/
└── screenshots/
    ├── login.png
    ├── dashboard.png
    ├── phishing-result.png
    ├── legitimate-result.png
    ├── scan-history.png
    └── api-docs.png
```

Save your real screenshots using these filenames. GitHub displays the
images only when the files exist at the referenced paths and are
committed to the repository. Remove any image line for a screenshot you
have not added yet. Never include passwords, JWT tokens, secret keys, or
private user data in screenshots.

------------------------------------------------------------------------

## 🛠️ Installation & Setup

### 🔹 Prerequisites

Ensure that you have installed:

-   Python compatible with the project's dependencies
-   Node.js and npm
-   PostgreSQL
-   Git

### 1️⃣ Clone the Repository

Replace the URL below with your actual GitHub repository URL.

``` bash
git clone https://github.com/YOUR-USERNAME/CyberShield-AI.git
cd CyberShield-AI
```

### 2️⃣ Set Up the Python Environment

Run these commands from the project root in Windows PowerShell:

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies from the requirements file, if present:

``` powershell
pip install -r requirements.txt
```

If the backend has its own requirements file, use that file's actual
path instead.

### 3️⃣ Configure Environment Variables

Create a local `.env` file using the variable names required by your
backend. For example:

``` env
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/cybershield
SECRET_KEY=<your-long-random-secret>
```

These are examples only. Confirm the exact variable names in your code.
Keep `.env` out of GitHub and never publish real passwords or secrets.

### 4️⃣ Configure PostgreSQL

-   Start the PostgreSQL service.
-   Create the `cybershield` database if it does not already exist.
-   Create the required tables or run your project's database
    initialization/migration scripts.
-   Confirm that the backend can connect using the configured database
    credentials.

### 5️⃣ Run the FastAPI Backend

For a project whose entry point is `backend/app/main.py`, run this from
the project root:

``` powershell
uvicorn backend.app.main:app --reload
```

Adjust the import path if your actual entry point differs.

Once the backend starts, open:

-   **API base URL:** `http://127.0.0.1:8000`
-   **Swagger UI:** `http://127.0.0.1:8000/docs`
-   **ReDoc:** `http://127.0.0.1:8000/redoc`

### 6️⃣ Run the React Frontend

Open a second terminal:

``` powershell
cd frontend
npm install
npm run dev
```

Open the local address printed by Vite, commonly
`http://localhost:5173`.

### 7️⃣ Test the Application

1.  Register a test user.
2.  Sign in with the test account.
3.  Submit a URL using the scan interface.
4.  Check the predicted class and risk level.
5.  Review the scan history and dashboard statistics.
6.  Capture screenshots for this README.

If the scan endpoint returns `422 Unprocessable Entity`, check the
request body and required field names in Swagger UI and make sure the
frontend sends the expected schema.

------------------------------------------------------------------------

## 🔌 API Endpoints

The endpoints below reflect the routes used in the current project
workflow. Confirm the final methods and schemas in Swagger UI at
`/docs`.

  Method   Endpoint           Description
  -------- ------------------ ------------------------------------------------
  `POST`   `/auth/register`   Register a user
  `POST`   `/auth/login`      Authenticate a user
  `POST`   `/scan/`           Submit a URL scan, if configured at this route
  `GET`    `/scan/history`    Retrieve scan history
  `GET`    `/scan/stats`      Retrieve dashboard statistics
  `GET`    `/health`          Health check, if enabled
  `GET`    `/docs`            Interactive Swagger API documentation

Some endpoints require authentication. Use the authorization method and
request schema shown in the live API documentation.

------------------------------------------------------------------------

## 📈 Example Output

During development, example test scenarios included:

  Test scenario                          Example result
  -------------------------------------- -----------------------
  `https://www.google.com`               Legitimate / Low risk
  A payment-service lookalike test URL   Phishing / High risk

These are illustrative development examples, not guaranteed outputs for
every URL. Replace them with verified examples from the final running
application. Do not visit suspicious URLs just to test the model.

------------------------------------------------------------------------

## 🔒 Security Measures

-   Store passwords using a secure password-hashing method.
-   Keep database credentials and signing secrets in environment
    variables.
-   Never commit `.env`, access tokens, or private data.
-   Verify authentication and user-level authorization on protected
    endpoints.
-   Validate submitted URLs and handle malformed inputs safely.
-   Avoid logging passwords, tokens, and other sensitive information.
-   Use HTTPS, rate limiting, secure production settings, and
    appropriate database permissions before deployment.
-   Treat ML predictions as assessments rather than definitive security
    guarantees.

------------------------------------------------------------------------

## 🔮 Future Enhancements

The following modules are possible extensions. Mark them as complete
only after implementation and testing.

-   🦠 **Malware Detection** --- Analyze suspicious files using a
    suitable, safely designed pipeline.
-   👤 **Login Anomaly Detection** --- Identify unusual login patterns.
-   🌐 **Intrusion Detection** --- Analyze network events for suspicious
    activity.
-   📡 **Network Monitoring** --- Add monitoring and alerting
    capabilities.
-   🔑 **Password Strength Analysis** --- Provide password-strength
    feedback without storing plaintext passwords.
-   📉 **Advanced Analytics** --- Add visual reports, filtering, and
    export options.
-   🐳 **Docker Deployment** --- Package the application and its
    services.
-   ☁️ **Cloud Deployment and CI/CD** --- Automate testing and
    deployment.

------------------------------------------------------------------------

## 💻 Tech Stack

  Category               Technology
  ---------------------- -------------------------
  Programming language   Python
  Frontend               React, Vite, JavaScript
  Backend                FastAPI
  Machine learning       Python ML pipeline
  Model persistence      Joblib
  Database               PostgreSQL
  HTTP client            Axios
  API documentation      Swagger UI / ReDoc
  Development tools      VS Code, Git

Update this list to match the exact libraries and versions used in the
final implementation.

------------------------------------------------------------------------

## 👩‍💻 Author

**Gargi Verma**\
Aspiring Machine Learning Engineer\
**Project:** CyberShield AI --- Capstone Project

------------------------------------------------------------------------

## 📜 License

This project is intended for educational and research purposes. Before
publishing the repository, add a formal license file if you want to
grant others specific rights to reuse or distribute your code. Also
verify the license terms for datasets, dependencies, and model files.

------------------------------------------------------------------------

## ⭐ Show Your Support

If you find this project useful:

-   ⭐ Star the repository
-   🍴 Fork the project
-   🛠️ Suggest improvements or contribute

------------------------------------------------------------------------


