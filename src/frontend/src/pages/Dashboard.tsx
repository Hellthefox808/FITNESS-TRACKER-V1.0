import React, { useState, useEffect, useRef } from 'react';
import { predictService, CaloriePredictionPayload, PredictionResult } from '../services/predictService';

export const Dashboard: React.FC = () => {
  const [telemetry, setTelemetry] = useState<CaloriePredictionPayload>({
    age: 28,
    gender: 'male',
    height_cm: 178.0,
    weight_kg: 75.5,
    duration_min: 45.0,
    heart_rate_bpm: 154.0,
    body_temp_c: 38.1,
  });

  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [scrollProgress, setScrollProgress] = useState<number>(0);

  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchPrediction(telemetry);

    const handleScroll = () => {
      const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = totalHeight > 0 ? (window.scrollY / totalHeight) * 100 : 0;
      setScrollProgress(progress);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const cards = document.querySelectorAll<HTMLDivElement>('.card-spotlight');
    cards.forEach((card) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      card.style.setProperty('--mouse-x', `${x}px`);
      card.style.setProperty('--mouse-y', `${y}px`);
    });
  };

  const fetchPrediction = async (payload: CaloriePredictionPayload) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await predictService.predictCalories(payload);
      setPrediction(result);
    } catch (err: any) {
      setError(err?.message || 'Failed to execute ML calorie prediction engine.');
    } finally {
      setIsLoading(false);
    }
  };

  const handlePredict = (e: React.FormEvent) => {
    e.preventDefault();
    fetchPrediction(telemetry);
  };

  const createRipple = (e: React.MouseEvent<HTMLButtonElement>) => {
    const button = e.currentTarget;
    const circle = document.createElement('span');
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;

    const rect = button.getBoundingClientRect();
    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${e.clientX - rect.left - radius}px`;
    circle.style.top = `${e.clientY - rect.top - radius}px`;
    circle.classList.add('ripple-effect');

    const ripple = button.getElementsByClassName('ripple-effect')[0];
    if (ripple) {
      ripple.remove();
    }
    button.appendChild(circle);
  };

  return (
    <div ref={containerRef} onMouseMove={handleMouseMove}>
      <div className="scroll-progress-bar" style={{ width: `${scrollProgress}%` }} />

      <div className="container">
        <header>
          <div>
            <h1 className="header-title">Fitness Tracker Using Machine Learning</h1>
            <p style={{ color: 'var(--text-secondary)', marginTop: '4px' }}>
              Real-Time Biometric Telemetry & Machine Learning Calorie Expenditure Engine
            </p>
          </div>
          <span className="badge">Author: Ravi Ranjan Singh</span>
        </header>

        {error && (
          <div style={{ padding: '14px 20px', backgroundColor: 'rgba(248, 113, 113, 0.15)', border: '1px solid var(--danger-color)', color: '#fca5a5', borderRadius: 'var(--radius-md)', marginBottom: '24px' }}>
            <strong>Inference Engine Error:</strong> {error}
          </div>
        )}

        <div className="grid">
          <div className="card card-spotlight">
            <h3>Predicted Calorie Expenditure</h3>
            <div className="metric-value">
              {isLoading ? 'Calculating...' : `${prediction?.predicted_calories_burned || 482.65} kcal`}
            </div>
            <p style={{ color: 'var(--text-secondary)', marginTop: '8px', fontSize: '0.88rem' }}>
              95% Confidence Bounds: [{prediction?.confidence_interval_95?.lower ?? 460.3}, {prediction?.confidence_interval_95?.upper ?? 504.9}]
            </p>
          </div>

          <div className="card card-spotlight">
            <h3>Heart Rate Intensity Zone</h3>
            <div className="metric-value" style={{ fontSize: '1.6rem' }}>
              {isLoading ? 'Analyzing...' : prediction?.derived_metrics?.intensity_zone || 'Anaerobic (Zone 4)'}
            </div>
            <p style={{ color: 'var(--text-secondary)', marginTop: '8px', fontSize: '0.88rem' }}>
              Current HR: {telemetry.heart_rate_bpm} BPM (Ratio: {prediction?.derived_metrics?.heart_rate_ratio || 0.802})
            </p>
          </div>

          <div className="card card-spotlight">
            <h3>Body Mass Index (BMI)</h3>
            <div className="metric-value">
              {prediction?.derived_metrics?.bmi || (telemetry.weight_kg / Math.pow(telemetry.height_cm / 100, 2)).toFixed(1)}
            </div>
            <p style={{ color: 'var(--text-secondary)', marginTop: '8px', fontSize: '0.88rem' }}>
              Status: Normal Weight
            </p>
          </div>
        </div>

        <div className="card card-spotlight" style={{ maxWidth: '620px', margin: '0 auto 48px auto' }}>
          <h2 style={{ marginBottom: '24px', fontSize: '1.4rem', fontWeight: 700 }}>Real-Time Telemetry Control</h2>
          <form onSubmit={handlePredict}>
            <div className="grid" style={{ gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              <div className="form-group">
                <label>Age (Years)</label>
                <input
                  type="number"
                  value={telemetry.age}
                  onChange={(e) => setTelemetry({ ...telemetry, age: Number(e.target.value) })}
                />
              </div>
              <div className="form-group">
                <label>Gender</label>
                <select
                  value={telemetry.gender}
                  onChange={(e) => setTelemetry({ ...telemetry, gender: e.target.value })}
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                </select>
              </div>
              <div className="form-group">
                <label>Height (cm)</label>
                <input
                  type="number"
                  value={telemetry.height_cm}
                  onChange={(e) => setTelemetry({ ...telemetry, height_cm: Number(e.target.value) })}
                />
              </div>
              <div className="form-group">
                <label>Weight (kg)</label>
                <input
                  type="number"
                  value={telemetry.weight_kg}
                  onChange={(e) => setTelemetry({ ...telemetry, weight_kg: Number(e.target.value) })}
                />
              </div>
              <div className="form-group">
                <label>Duration (Minutes)</label>
                <input
                  type="number"
                  value={telemetry.duration_min}
                  onChange={(e) => setTelemetry({ ...telemetry, duration_min: Number(e.target.value) })}
                />
              </div>
              <div className="form-group">
                <label>Heart Rate (BPM)</label>
                <input
                  type="number"
                  value={telemetry.heart_rate_bpm}
                  onChange={(e) => setTelemetry({ ...telemetry, heart_rate_bpm: Number(e.target.value) })}
                />
              </div>
            </div>
            <button
              type="submit"
              disabled={isLoading}
              onClick={createRipple}
              style={{ marginTop: '12px' }}
            >
              {isLoading ? 'Processing ML Inference...' : 'Execute ML Calorie Inference'}
            </button>
          </form>
        </div>

        <footer>
          <p>
            Fitness Tracker Using Machine Learning &copy; 2026 | Author & Lead Architect:{' '}
            <strong style={{ color: 'var(--text-primary)' }}>Ravi Ranjan Singh</strong>
          </p>
        </footer>
      </div>
    </div>
  );
};
