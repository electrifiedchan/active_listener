import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [emotion, setEmotion] = useState("initializing...")
  const [systemStatus, setSystemStatus] = useState("OFFLINE")
  const [logs, setLogs] = useState([])

  // Helper to add logs
  const addLog = (message) => {
    setLogs(prev => [`[${new Date().toLocaleTimeString()}] ${message}`, ...prev].slice(0, 5))
  }

  useEffect(() => {
    // 1. Check Backend Connection & Get Emotion
    const interval = setInterval(() => {
      fetch('http://localhost:5000/emotion')
        .then(res => res.json())
        .then(data => {
          setSystemStatus("ONLINE")
          if (data.emotion && data.emotion !== emotion) {
            setEmotion(data.emotion)
            addLog(`Emotion detected: ${data.emotion.toUpperCase()}`)
          }
        })
        .catch(() => {
          setSystemStatus("DISCONNECTED")
          setEmotion("---")
        })
    }, 1000)

    return () => clearInterval(interval)
  }, [emotion])

  return (
    <div className="container">
      {/* HEADER */}
      <header>
        <h1 className="title" data-text="EQ-VISION">EQ-VISION</h1>
        <p className="subtitle">_ REAL-TIME EMOTION INTELLIGENCE SYSTEM // V1.0</p>
      </header>

      <main className="main-content">
        {/* LEFT: VIDEO FEED */}
        <div className="video-section">
          <div className="scanner-overlay">
            {/* Direct Feed from Python Backend */}
            <img 
              src="http://localhost:5000/video_feed" 
              alt="Live Feed" 
              className="video-feed" 
              onError={(e) => {
                e.target.style.display = 'none'; 
                // You could show a placeholder image here if you want
              }}
            />
            <div className="face-brackets"></div>
          </div>
          <div className="status-bar">
            <span className="status-dot" style={{backgroundColor: systemStatus === "ONLINE" ? "#0f0" : "#f00"}}></span>
            SYSTEM STATUS: {systemStatus}
          </div>
        </div>

        {/* RIGHT: DATA DASHBOARD */}
        <div className="dashboard">
          
          {/* CURRENT EMOTION CARD */}
          <div className="card emotion-card">
            <h3>CURRENT STATE</h3>
            <h2 className={`emotion-text ${emotion === "happy" ? "text-green" : emotion === "sad" ? "text-blue" : "text-white"}`}>
              {emotion.toUpperCase()}
            </h2>
            <div className="confidence-bar">
              <div className="fill" style={{width: systemStatus === "ONLINE" ? "92%" : "0%"}}></div>
            </div>
            <p className="confidence-label">CONFIDENCE: 92%</p>
          </div>

          {/* LOGS PANEL */}
          <div className="card logs-card">
            <h3>SYSTEM LOGS</h3>
            <div className="logs-window">
              {logs.map((log, i) => (
                <p key={i} className="log-entry">{log}</p>
              ))}
              {logs.length === 0 && <p className="log-entry">Waiting for input...</p>}
            </div>
          </div>

          {/* FOOTER METRICS */}
          <div className="metrics-grid">
            <div className="metric-box">
              <span className="label">CPU</span>
              <span className="value">12%</span>
            </div>
            <div className="metric-box">
              <span className="label">LATENCY</span>
              <span className="value">45ms</span>
            </div>
            <div className="metric-box">
              <span className="label">VOICE</span>
              <span className="value">ACTIVE</span>
            </div>
          </div>

        </div>
      </main>
    </div>
  )
}

export default App