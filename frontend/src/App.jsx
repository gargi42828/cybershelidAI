import { useEffect, useState } from "react";
import axios from "axios";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [showSignup, setShowSignup] = useState(false);

  // Login states
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");

  // Signup states
  const [signupUsername, setSignupUsername] = useState("");
  const [signupEmail, setSignupEmail] = useState("");
  const [signupPassword, setSignupPassword] = useState("");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Dashboard states
  const [stats, setStats] = useState({
    total_scans: 0,
    phishing_detected: 0,
    legitimate_urls: 0,
    high_risk: 0,
    medium_risk: 0,
    low_risk: 0,
  });

  const [history, setHistory] = useState([]);
  const [scanInput, setScanInput] = useState("");
  const [scanResult, setScanResult] = useState(null);
  const [scanLoading, setScanLoading] = useState(false);

  const getAuthHeaders = () => ({
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  // ---------------- LOGIN ----------------
  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);
      setError("");
      setMessage("");

      const formData = new URLSearchParams();

      formData.append("username", loginEmail);
      formData.append("password", loginPassword);

      const response = await axios.post(
        `${API_URL}/auth/login`,
        formData,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      const accessToken = response.data.access_token;

      localStorage.setItem("token", accessToken);
      setToken(accessToken);

      setLoginEmail("");
      setLoginPassword("");
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Invalid email or password."
      );
    } finally {
      setLoading(false);
    }
  };

  // ---------------- SIGNUP ----------------
  const handleSignup = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);
      setError("");
      setMessage("");

      const response = await axios.post(
        `${API_URL}/auth/register`,
        {
          username: signupUsername,
          email: signupEmail,
          password: signupPassword,
        }
      );

      if (response.status === 201) {
        setMessage(
          "Account created successfully! Please sign in."
        );

        setSignupUsername("");
        setSignupEmail("");
        setSignupPassword("");

        setTimeout(() => {
          setShowSignup(false);
          setMessage("");
        }, 1500);
      }
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Unable to create account."
      );
    } finally {
      setLoading(false);
    }
  };

  // ---------------- LOAD DASHBOARD ----------------
  const loadDashboard = async () => {
    try {
      setError("");

      const headers = getAuthHeaders();

      const [statsResponse, historyResponse] =
        await Promise.all([
          axios.get(
            `${API_URL}/scan/statistics`,
            headers
          ),
          axios.get(
            `${API_URL}/scan/history`,
            headers
          ),
        ]);

      setStats(statsResponse.data);

      const historyData = historyResponse.data;

      setHistory(
        Array.isArray(historyData)
          ? historyData
          : historyData.scans || []
      );
    } catch (err) {
      console.error(err);

      if (err.response?.status === 401) {
        localStorage.removeItem("token");
        setToken(null);
      } else {
        setError(
          "Unable to load dashboard data."
        );
      }
    }
  };

  useEffect(() => {
    if (token) {
      loadDashboard();
    }
  }, [token]);

  // ---------------- SCAN ----------------
  const handleScan = async (e) => {
    e.preventDefault();

    if (!scanInput.trim()) {
      setError("Please enter a URL.");
      return;
    }

    try {
      setScanLoading(true);
      setError("");
      setScanResult(null);

      const response = await axios.post(
        `${API_URL}/scan/`,
        {
          input_text: scanInput,
        },
        getAuthHeaders()
      );

      setScanResult(response.data);
      setScanInput("");

      await loadDashboard();
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Scan failed."
      );
    } finally {
      setScanLoading(false);
    }
  };

  // ---------------- LOGOUT ----------------
  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);

    setStats({
      total_scans: 0,
      phishing_detected: 0,
      legitimate_urls: 0,
      high_risk: 0,
      medium_risk: 0,
      low_risk: 0,
    });

    setHistory([]);
  };

  // ================= LOGIN / SIGNUP PAGE =================

  if (!token) {
    return (
      <div className="auth-page">
        <div className="auth-card">

          <div className="auth-logo">
            🛡️
          </div>

          <h1>CyberShield AI</h1>

          <p className="auth-subtitle">
            Intelligent Cyber Security Platform
          </p>

          {showSignup ? (
            <>
              <h2>Create Account</h2>

              <form onSubmit={handleSignup}>

                <label>Username</label>

                <input
                  type="text"
                  placeholder="Enter username"
                  value={signupUsername}
                  onChange={(e) =>
                    setSignupUsername(
                      e.target.value
                    )
                  }
                  required
                />

                <label>Email</label>

                <input
                  type="email"
                  placeholder="Enter email"
                  value={signupEmail}
                  onChange={(e) =>
                    setSignupEmail(
                      e.target.value
                    )
                  }
                  required
                />

                <label>Password</label>

                <input
                  type="password"
                  placeholder="Create password"
                  value={signupPassword}
                  onChange={(e) =>
                    setSignupPassword(
                      e.target.value
                    )
                  }
                  required
                />

                {error && (
                  <div className="error-message">
                    ⚠️ {error}
                  </div>
                )}

                {message && (
                  <div className="success-message">
                    ✅ {message}
                  </div>
                )}

                <button
                  type="submit"
                  disabled={loading}
                  className="auth-button"
                >
                  {loading
                    ? "Creating Account..."
                    : "Sign Up"}
                </button>

              </form>

              <p className="switch-auth">
                Already have an account?

                <button
                  className="link-button"
                  onClick={() => {
                    setShowSignup(false);
                    setError("");
                    setMessage("");
                  }}
                >
                  Sign In
                </button>
              </p>
            </>
          ) : (
            <>
              <h2>Welcome Back</h2>

              <form onSubmit={handleLogin}>

                <label>Email</label>

                <input
                  type="email"
                  placeholder="Enter your email"
                  value={loginEmail}
                  onChange={(e) =>
                    setLoginEmail(
                      e.target.value
                    )
                  }
                  required
                />

                <label>Password</label>

                <input
                  type="password"
                  placeholder="Enter your password"
                  value={loginPassword}
                  onChange={(e) =>
                    setLoginPassword(
                      e.target.value
                    )
                  }
                  required
                />

                {error && (
                  <div className="error-message">
                    ⚠️ {error}
                  </div>
                )}

                <button
                  type="submit"
                  disabled={loading}
                  className="auth-button"
                >
                  {loading
                    ? "Signing In..."
                    : "Sign In"}
                </button>

              </form>

              <p className="switch-auth">
                Don't have an account?

                <button
                  className="link-button"
                  onClick={() => {
                    setShowSignup(true);
                    setError("");
                  }}
                >
                  Sign Up
                </button>
              </p>
            </>
          )}

        </div>
      </div>
    );
  }

  // ================= DASHBOARD =================

  const chartData = [
    {
      name: "High Risk",
      value: stats.high_risk,
    },
    {
      name: "Medium Risk",
      value: stats.medium_risk,
    },
    {
      name: "Low Risk",
      value: stats.low_risk,
    },
  ].filter(
    (item) => item.value > 0
  );

  return (
    <div className="dashboard">

      {/* ================= TOP BAR ================= */}

      <header className="topbar">

        <div>
          <h1>
            🛡️ CyberShield AI
          </h1>

          <span>
            AI Security System v1.0
          </span>
        </div>

        <button
          className="logout-button"
          onClick={handleLogout}
        >
          Logout
        </button>

      </header>

      <main className="main-content">

        {/* ================= TITLE ================= */}

        <div className="dashboard-title">

          <div>

            <h2>
              Security Dashboard
            </h2>

            <p>
              Monitor and analyze your
              security threats in real time.
            </p>

          </div>

          <div className="system-status">
            ● System Online
          </div>

        </div>

        {/* ================= ERROR ================= */}

        {error && (
          <div className="error-message dashboard-error">
            ⚠️ {error}
          </div>
        )}

        {/* ================= STATISTICS ================= */}

        <div className="stats-grid">

          <div className="stat-card">
            <span>
              Total Scans
            </span>

            <strong>
              {stats.total_scans}
            </strong>
          </div>

          <div className="stat-card">
            <span>
              Phishing Detected
            </span>

            <strong>
              {stats.phishing_detected}
            </strong>
          </div>

          <div className="stat-card">
            <span>
              Legitimate URLs
            </span>

            <strong>
              {stats.legitimate_urls}
            </strong>
          </div>

          <div className="stat-card">
            <span>
              High Risk
            </span>

            <strong>
              {stats.high_risk}
            </strong>
          </div>

        </div>

        {/* ================= SCANNER + CHART ================= */}

        <div className="content-grid">

          {/* ================= SCANNER ================= */}

          <section className="scanner-card">

            <h2>
              🔍 Security Scanner
            </h2>

            <p>
              Enter a URL to analyze it
              for phishing threats.
            </p>

            <form onSubmit={handleScan}>

              <input
                type="text"
                placeholder="https://example.com"
                value={scanInput}
                onChange={(e) =>
                  setScanInput(
                    e.target.value
                  )
                }
              />

              <button
                type="submit"
                disabled={scanLoading}
              >
                {scanLoading
                  ? "Scanning..."
                  : "Scan URL"}
              </button>

            </form>

            {scanResult && (
              <div className="scan-result">

                <h3>
                  Scan Result
                </h3>

                <p>
                  <strong>
                    Threat:
                  </strong>{" "}
                  {scanResult.threat_type}
                </p>

                <p>
                  <strong>
                    Risk:
                  </strong>{" "}
                  {scanResult.risk_level}
                </p>

                <p>
                  <strong>
                    Confidence:
                  </strong>{" "}
                  {scanResult.confidence}
                </p>

              </div>
            )}

          </section>

          {/* ================= PIE CHART ================= */}

          <section className="chart-card">

            <h2>
              📊 Risk Distribution
            </h2>

            {chartData.length > 0 ? (

              <ResponsiveContainer
                width="100%"
                height={300}
              >

                <PieChart>

                  <Pie
                    data={chartData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="45%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    label
                  >

                    {chartData.map(
                      (entry, index) => {

                        let color =
                          "#22c55e";

                        if (
                          entry.name ===
                          "High Risk"
                        ) {
                          color =
                            "#ef4444";
                        }

                        if (
                          entry.name ===
                          "Medium Risk"
                        ) {
                          color =
                            "#f59e0b";
                        }

                        if (
                          entry.name ===
                          "Low Risk"
                        ) {
                          color =
                            "#22c55e";
                        }

                        return (
                          <Cell
                            key={`cell-${index}`}
                            fill={color}
                          />
                        );
                      }
                    )}

                  </Pie>

                  <Tooltip />

                  <Legend />

                </PieChart>

              </ResponsiveContainer>

            ) : (

              <p>
                No scan data available.
              </p>

            )}

          </section>

        </div>

        {/* ================= HISTORY ================= */}

        <section className="history-card">

          <h2>
            🕒 Recent Scans
          </h2>

          {history.length === 0 ? (

            <p>
              No scans available.
            </p>

          ) : (

            <div className="history-list">

              {history.map((scan) => (

                <div
                  className="history-item"
                  key={scan.scan_id || scan.id}
                >

                  <div>

                    <strong>
                      {scan.input_text}
                    </strong>

                    <small>
                      {scan.threat_type}
                      {" • "}
                      {scan.risk_level}
                    </small>

                  </div>

                  <span>
                    {scan.confidence ||
                      "N/A"}
                  </span>

                </div>

              ))}

            </div>

          )}

        </section>

      </main>

    </div>
  );
}

export default App;
