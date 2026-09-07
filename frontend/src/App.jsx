import { useState } from 'react'
import './App.css'

function App() {
  const [activePage, setActivePage] = useState('dashboard')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleAnalyze = async (event) => {
    event.preventDefault()

    const formData = new FormData(event.currentTarget)

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
      setResult(null)

      const response = await fetch('/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })

      const prediction = await response.json()

      if (!response.ok) {
        throw new Error(prediction.error || 'Prediction failed')
      }

      setResult(prediction)
    } catch (error) {
      console.error(error)
      alert('Prediction failed: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const getRiskClass = (level) => {
    if (level === 'Critical' || level === 'High') return 'risk-danger'
    if (level === 'Medium') return 'risk-warning'
    return 'risk-safe'
  }

  return (
    <div className="app-shell">

      {/* ================= SIDEBAR ================= */}

      <aside className="sidebar">

        <div className="sidebar-brand">
          <div className="brand-mark">FL</div>

          <div>
            <h2>FraudLens</h2>
            <span>AI Investigation Platform</span>
          </div>
        </div>

        <div className="nav-heading">
          WORKSPACE
        </div>

        <nav className="nav-menu">

          <button
            className={`nav-item ${
              activePage === 'dashboard' ? 'active' : ''
            }`}
            onClick={() => setActivePage('dashboard')}
          >
            <span className="nav-icon">▦</span>
            Dashboard
          </button>

          <button
            className={`nav-item ${
              activePage === 'analyze' ? 'active' : ''
            }`}
            onClick={() => setActivePage('analyze')}
          >
            <span className="nav-icon">⌕</span>
            Analyze Transaction
          </button>

          <button className="nav-item disabled-nav">
            <span className="nav-icon">!</span>
            Alerts
            <span className="coming-soon">Soon</span>
          </button>

          <button className="nav-item disabled-nav">
            <span className="nav-icon">□</span>
            Cases
            <span className="coming-soon">Soon</span>
          </button>

          <button className="nav-item disabled-nav">
            <span className="nav-icon">◌</span>
            Analytics
            <span className="coming-soon">Soon</span>
          </button>

          <button className="nav-item disabled-nav">
            <span className="nav-icon">▤</span>
            Reports
            <span className="coming-soon">Soon</span>
          </button>

        </nav>

        <div className="sidebar-bottom">

          <div className="system-indicator">
            <span className="online-dot"></span>

            <div>
              <strong>System Online</strong>
              <span>AI modules operational</span>
            </div>
          </div>

          <div className="sidebar-version">
            FraudLens v1.0
          </div>

        </div>

      </aside>


      {/* ================= MAIN ================= */}

      <main className="main-content">

        {activePage === 'dashboard' ? (

          /* ================= DASHBOARD ================= */

          <>

            <header className="page-header">

              <div>
                <div className="eyebrow">
                  FRAUD INVESTIGATION
                </div>

                <h1>Dashboard</h1>

                <p>
                  Monitor transaction activity and AI-based fraud analysis.
                </p>
              </div>

              <button
                className="primary-button"
                onClick={() => setActivePage('analyze')}
              >
                + Analyze Transaction
              </button>

            </header>


            <section className="overview-strip">

              <div className="overview-item">
                <span>Total Transactions</span>
                <strong>0</strong>
                <small>Analyzed</small>
              </div>

              <div className="overview-item">
                <span>Fraud Detected</span>
                <strong>0</strong>
                <small>XGBoost classifications</small>
              </div>

              <div className="overview-item">
                <span>High Risk</span>
                <strong>0</strong>
                <small>Require investigation</small>
              </div>

              <div className="overview-item">
                <span>Active Alerts</span>
                <strong>0</strong>
                <small>Current warnings</small>
              </div>

            </section>


            <section className="dashboard-layout">

              <div className="dashboard-panel">

                <div className="panel-title">
                  <div>
                    <span>TRANSACTION MONITOR</span>
                    <h3>Recent Transactions</h3>
                  </div>
                </div>

                <div className="empty-dashboard">

                  <div className="empty-icon">
                    ⌕
                  </div>

                  <h3>No transactions analyzed</h3>

                  <p>
                    Start an analysis to see transaction results
                    and risk information here.
                  </p>

                  <button
                    className="secondary-action"
                    onClick={() => setActivePage('analyze')}
                  >
                    Analyze Transaction
                  </button>

                </div>

              </div>


              <div className="dashboard-panel">

                <div className="panel-title">
                  <div>
                    <span>AI ENGINE</span>
                    <h3>System Status</h3>
                  </div>
                </div>

                <div className="module-list">

                  <div className="module-row">
                    <span>XGBoost Detection</span>
                    <b>Operational</b>
                  </div>

                  <div className="module-row">
                    <span>Isolation Forest</span>
                    <b>Operational</b>
                  </div>

                  <div className="module-row">
                    <span>SHAP Explainability</span>
                    <b>Operational</b>
                  </div>

                  <div className="module-row">
                    <span>Risk Scoring</span>
                    <b>Operational</b>
                  </div>

                </div>

              </div>

            </section>

          </>

        ) : (

          /* ================= ANALYZE PAGE ================= */

          <>

            <header className="page-header">

              <div>
                <div className="eyebrow">
                  AI FRAUD ANALYSIS
                </div>

                <h1>Analyze Transaction</h1>

                <p>
                  Evaluate a transaction using FraudLens AI models.
                </p>
              </div>

              <button
                className="secondary-header-button"
                onClick={() => setActivePage('dashboard')}
              >
                ← Dashboard
              </button>

            </header>


            <section className="analysis-workspace">

              {/* INPUT PANEL */}

              <div className="input-panel">

                <div className="section-heading">
                  <div>
                    <span>TRANSACTION INPUT</span>
                    <h2>Transaction Details</h2>
                  </div>

                  <div className="input-count">
                    07 FEATURES
                  </div>
                </div>

                <form
                  className="transaction-form"
                  onSubmit={handleAnalyze}
                >

                  <div className="form-grid">

                    <div className="form-group">
                      <label>Transaction ID</label>
                      <input
                        type="number"
                        name="TransactionID"
                        placeholder="2987000"
                        required
                      />
                    </div>

                    <div className="form-group">
                      <label>Transaction Amount</label>
                      <input
                        type="number"
                        name="TransactionAmt"
                        placeholder="Enter amount"
                        required
                      />
                    </div>

                    <div className="form-group">
                      <label>Transaction Time</label>
                      <input
                        type="number"
                        name="TransactionDT"
                        placeholder="TransactionDT"
                        required
                      />
                    </div>

                    <div className="form-group">
                      <label>Card 1</label>
                      <input
                        type="number"
                        name="card1"
                        placeholder="Card identifier"
                        required
                      />
                    </div>

                    <div className="form-group">
                      <label>Card 2</label>
                      <input
                        type="number"
                        name="card2"
                        placeholder="Card information"
                        required
                      />
                    </div>

                    <div className="form-group">
                      <label>Address</label>
                      <input
                        type="number"
                        name="addr1"
                        placeholder="Address feature"
                        required
                      />
                    </div>

                    <div className="form-group">
                      <label>Distance</label>
                      <input
                        type="number"
                        name="dist1"
                        placeholder="Distance feature"
                        required
                      />
                    </div>

                  </div>


                  <div className="form-footer">

                    <span>
                      Input values are processed by the AI analysis pipeline.
                    </span>

                    <div>

                      <button
                        type="button"
                        className="clear-button"
                        onClick={(e) => {
                          e.currentTarget.form.reset()
                          setResult(null)
                        }}
                      >
                        Clear
                      </button>

                      <button
                        type="submit"
                        className="analyze-submit"
                        disabled={loading}
                      >
                        {loading
                          ? 'Analyzing...'
                          : 'Run AI Analysis →'}
                      </button>

                    </div>

                  </div>

                </form>

              </div>


              {/* RESULT PANEL */}

              {loading && (

                <div className="result-panel loading-panel">

                  <div className="loading-animation">
                    <div></div>
                  </div>

                  <span className="result-eyebrow">
                    PROCESSING TRANSACTION
                  </span>

                  <h2>Running AI Analysis</h2>

                  <p>
                    XGBoost, anomaly detection and explainability
                    modules are evaluating the transaction.
                  </p>

                </div>

              )}


              {result && !loading && (

                <div className="result-panel">

                  {/* RESULT TOP */}

                  <div className="result-top">

                    <div>
                      <span className="result-eyebrow">
                        ANALYSIS RESULT
                      </span>

                      <h2>Transaction Assessment</h2>
                    </div>

                    <div className="result-status-time">
                      <span className="status-dot"></span>
                      Analysis Complete
                    </div>

                  </div>


                  {/* DECISION */}

                  <div
                    className={
                      result.prediction === 1
                        ? 'decision-banner fraud-banner'
                        : 'decision-banner safe-banner'
                    }
                  >

                    <div className="decision-icon">
                      {result.prediction === 1 ? '!' : '✓'}
                    </div>

                    <div className="decision-text">

                      <span>
                        MODEL DECISION
                      </span>

                      <strong>
                        {result.prediction === 1
                          ? 'FRAUD DETECTED'
                          : 'LEGITIMATE TRANSACTION'}
                      </strong>

                      <p>
                        {result.prediction === 1
                          ? 'The transaction has been flagged by the fraud detection model.'
                          : 'The transaction was not classified as fraudulent by the detection model.'}
                      </p>

                    </div>

                  </div>


                  {/* PRIMARY METRICS */}

                  <div className="metrics-row">

                    <div className="metric">

                      <span>FRAUD PROBABILITY</span>

                      <strong>
                        {(result.fraud_probability * 100).toFixed(2)}
                        <small>%</small>
                      </strong>

                      <div className="metric-line">
                        <div
                          style={{
                            width: `${result.fraud_probability * 100}%`,
                          }}
                        ></div>
                      </div>

                      <p>XGBoost confidence</p>

                    </div>


                    <div className="metric">

                      <span>RISK SCORE</span>

                      <strong>
                        {result.risk?.risk_score ?? 'N/A'}
                      </strong>

                      <div className="metric-label">
                        <span
                          className={getRiskClass(
                            result.risk?.risk_level
                          )}
                        >
                          {result.risk?.risk_level || 'N/A'} RISK
                        </span>
                      </div>

                    </div>


                    <div className="metric">

                      <span>ANOMALY SCORE</span>

                      <strong>
                        {result.anomaly?.anomaly_score ?? 'N/A'}
                      </strong>

                      <div className="metric-label neutral-label">
                        ISOLATION FOREST
                      </div>

                    </div>

                  </div>


                  {/* EXPLANATION */}

                  {result.shap_explanation && (

                    <div className="explanation">

                      <div className="explanation-title">

                        <div>
                          <span>MODEL EXPLAINABILITY</span>
                          <h3>Why this decision?</h3>
                        </div>

                        <div className="shap-label">
                          SHAP
                        </div>

                      </div>


                      <div className="factor-table">

                        <div className="factor-table-header">
                          <span>#</span>
                          <span>FEATURE</span>
                          <span>IMPACT</span>
                        </div>


                        {result.shap_explanation
                          .slice(0, 5)
                          .map((item, index) => (

                            <div
                              className="factor-row"
                              key={index}
                            >

                              <span className="factor-index">
                                0{index + 1}
                              </span>

                              <strong>
                                {item.feature}
                              </strong>

                              <span
                                className={
                                  item.impact === 'increases_fraud_risk'
                                    ? 'impact-up'
                                    : 'impact-down'
                                }
                              >
                                {item.impact === 'increases_fraud_risk'
                                  ? '↑ Increases risk'
                                  : '↓ Decreases risk'}
                              </span>

                            </div>

                          ))}

                      </div>

                    </div>

                  )}


                  <div className="result-footer">
                    <span>
                      Analysis generated by FraudLens AI
                    </span>

                    <span>
                      XGBoost • Isolation Forest • SHAP
                    </span>
                  </div>

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