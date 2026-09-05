import { useState } from 'react'
import './App.css'

function App() {
  const [activePage, setActivePage] = useState('dashboard')
  const [result, setResult] = useState(null)
const [loading, setLoading] = useState(false)

const handleAnalyze = async (event) => {
  event.preventDefault()

  const formData = new FormData(event.target)

  const data = {
    TransactionID: Number(formData.get('TransactionID')),
    TransactionAmt: Number(formData.get('TransactionAmt')),
    TransactionDT: Number(formData.get('TransactionDT')),
    card1: Number(formData.get('card1')),
    card2: Number(formData.get('card2')),
    addr1: Number(formData.get('addr1')),
    dist1: Number(formData.get('dist1')),
  }

  try {
    setLoading(true)

    const response = await fetch('/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })

    const prediction = await response.json()
    setResult(prediction)

    console.log('Prediction result:', prediction)
  } catch (error) {
    console.error('Prediction error:', error)
  } finally {
    setLoading(false)
  }
}

  return (
    <div className="dashboard-layout">

      {/* LEFT SIDEBAR */}
      <aside className="sidebar">

        <div className="brand">
          <div className="brand-icon">FL</div>

          <div>
            <h2>FraudLens</h2>
            <p>Investigation Platform</p>
          </div>
        </div>

        <nav className="nav-menu">

          <button
            className={`nav-item ${
              activePage === 'dashboard' ? 'active' : ''
            }`}
            onClick={() => setActivePage('dashboard')}
          >
            Dashboard
          </button>

          <button
            className={`nav-item ${
              activePage === 'analyze' ? 'active' : ''
            }`}
            onClick={() => setActivePage('analyze')}
          >
            Analyze Transaction
          </button>

          <button className="nav-item">
            Alerts
          </button>

          <button className="nav-item">
            Cases
          </button>

          <button className="nav-item">
            Analytics
          </button>

          <button className="nav-item">
            Reports
          </button>

        </nav>

        <div className="sidebar-footer">
          <p>FraudLens AI System</p>
          <span>● System Online</span>
        </div>

      </aside>

      {/* MAIN CONTENT */}
      <main className="main-content">

        {activePage === 'dashboard' ? (

          <>
            {/* DASHBOARD HEADER */}
            <header className="topbar">

              <div>
                <p className="page-label">
                  FRAUD INVESTIGATION
                </p>

                <h1>Dashboard</h1>

                <p className="page-description">
                  Monitor transactions, fraud risks and investigation activity.
                </p>
              </div>

              <button
                className="analyze-button"
                onClick={() => setActivePage('analyze')}
              >
                + Analyze Transaction
              </button>

            </header>

            {/* DASHBOARD CARDS */}
            <section className="stats-grid">

              <div className="stat-card">
                <p>Total Transactions</p>
                <h2>0</h2>
                <span>Transactions analyzed</span>
              </div>

              <div className="stat-card">
                <p>Fraud Detected</p>
                <h2>0</h2>
                <span>Flagged by XGBoost</span>
              </div>

              <div className="stat-card">
                <p>High Risk</p>
                <h2>0</h2>
                <span>Require investigation</span>
              </div>

              <div className="stat-card">
                <p>Active Alerts</p>
                <h2>0</h2>
                <span>Current warnings</span>
              </div>

            </section>

            {/* LOWER DASHBOARD */}
            <section className="dashboard-grid">

              <div className="panel recent-transactions">

                <div className="panel-header">
                  <div>
                    <h3>Recent Transactions</h3>
                    <p>
                      Latest transactions analyzed by FraudLens
                    </p>
                  </div>
                </div>

                <div className="empty-state">
                  <h4>No transactions analyzed yet</h4>

                  <p>
                    Analyze a transaction to view fraud probability,
                    anomaly status and risk level.
                  </p>

                  <button
                    onClick={() => setActivePage('analyze')}
                  >
                    Analyze First Transaction
                  </button>
                </div>

              </div>

              <div className="panel system-status">

                <div className="panel-header">
                  <div>
                    <h3>AI System Status</h3>
                    <p>FraudLens backend modules</p>
                  </div>
                </div>

                <div className="status-list">

                  <div className="status-row">
                    <span>XGBoost Fraud Detection</span>
                    <strong>Ready</strong>
                  </div>

                  <div className="status-row">
                    <span>Isolation Forest</span>
                    <strong>Ready</strong>
                  </div>

                  <div className="status-row">
                    <span>SHAP Explainability</span>
                    <strong>Ready</strong>
                  </div>

                  <div className="status-row">
                    <span>Dynamic Risk Scoring</span>
                    <strong>Ready</strong>
                  </div>

                </div>

              </div>

            </section>
          </>

        ) : (

          <>
            {/* ANALYZE TRANSACTION PAGE */}
            <header className="topbar">

              <div>
                <p className="page-label">
                  AI FRAUD ANALYSIS
                </p>

                <h1>Analyze Transaction</h1>

                <p className="page-description">
                  Enter transaction information for AI-based fraud analysis.
                </p>
              </div>

              <button
                className="analyze-button"
                onClick={() => setActivePage('dashboard')}
              >
                ← Back to Dashboard
              </button>

            </header>

            <section className="panel analyze-panel">

              <div className="panel-header">
                <div>
                  <h3>Transaction Details</h3>

                  <p>
                    Provide the transaction information required
                    for fraud prediction.
                  </p>
                </div>
              </div>

              <form className="transaction-form" onSubmit={handleAnalyze}> 

                <div className="form-grid">

                  <div className="form-group">
  <label>Transaction ID</label>
  <input
    type="number"
    name="TransactionID"
    placeholder="Example: 2987000"
  />
</div>

<div className="form-group">
  <label>Transaction Amount</label>
  <input
    type="number"
    name="TransactionAmt"
    placeholder="Enter amount"
  />
</div>
                  <div className="form-group">
                    <label>Transaction Time</label>

                    <input
                      type="number"
                      name="TransactionDT"
                      placeholder="TransactionDT"
                    />
                  </div>

                  <div className="form-group">
                    <label>Card 1</label>

                    <input
                      type="number"
                      name="card1"
                      placeholder="Card identifier"
                    />
                  </div>

                  <div className="form-group">
                    <label>Card 2</label>

                    <input
                      type="number"
                      name="card2"
                      placeholder="Card information"
                    />
                  </div>

                  <div className="form-group">
                    <label>Address</label>

                    <input
                      type="number"
                      name="addr1"
                      placeholder="Address feature"
                    />
                  </div>

                  <div className="form-group">
                    <label>Distance</label>

                    <input
                      type="number"
                      name="dist1"
                      placeholder="Distance feature"
                    />
                  </div>

                  

                </div>

                <div className="form-actions">

                  <button
  type="button"
  className="secondary-button"
  onClick={(e) => {
    e.currentTarget.form.reset()
    setResult(null)
  }}
>
  Clear
</button> 

                  <button
                    type="submit"
                    className="analyze-button"
                  >
                    Analyze Transaction
                  </button>

                </div>

              </form>
              {loading && (
  <div className="prediction-result">
    <h3>Analyzing Transaction...</h3>
  </div>
)}

{result && (
  <div className="prediction-result">
    <h3>Prediction Result</h3>

    <p>
      <strong>Status: </strong>
      <span className={result.prediction === 1 ? "status-fraud" : "status-legitimate"}>
  {result.prediction === 1 ? "Fraud Detected" : "Legitimate Transaction"}
</span> 
    </p>

    <p>
      <strong>Fraud Probability: </strong>
      {(result.fraud_probability * 100).toFixed(2)}%
    </p>

    <p>
  <strong>Risk Level: </strong>
  <span
  className={
    result.fraud_probability >= 0.7
      ? "risk-high"
      : result.fraud_probability >= 0.3
      ? "risk-medium"
      : "risk-low"
  }
>
  {result.fraud_probability >= 0.7
    ? "High Risk"
    : result.fraud_probability >= 0.3
    ? "Medium Risk"
    : "Low Risk"}
</span> 
   
</p>

  </div>
)}
            </section>
          </>

        )}

      </main>

    </div>
  )
}

export default App