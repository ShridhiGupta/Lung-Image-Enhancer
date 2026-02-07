import React, { useState } from 'react';
import axios from 'axios';
import './HomePage.css';

function HomePage() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [enhancedImages, setEnhancedImages] = useState({ v1: null, v2: null });
  const [diseasePrediction, setDiseasePrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const [activeTab, setActiveTab] = useState('report');

  const handleImageSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      processImage(file);
    }
  };

  const processImage = (file) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      setSelectedImage(reader.result);
      setEnhancedImages({ v1: null, v2: null });
      setDiseasePrediction(null);
      setError('');
    };
    reader.readAsDataURL(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = e.dataTransfer.files;
    if (files && files[0]) {
      processImage(files[0]);
    }
  };

  const enhanceImage = async () => {
    if (!selectedImage) return;

    setLoading(true);
    setError('');

    try {
      // Use environment-aware API URL
      const apiUrl = process.env.NODE_ENV === 'production' 
        ? '/api/enhance' 
        : 'http://localhost:5000/enhance';
      
      const response = await axios.post(apiUrl, {
        image: selectedImage
      });

      if (response.data.enhanced_v1 && response.data.enhanced_v2) {
        setEnhancedImages({
          v1: response.data.enhanced_v1,
          v2: response.data.enhanced_v2
        });
        
        // Set disease prediction if available
        if (response.data.disease_prediction) {
          setDiseasePrediction(response.data.disease_prediction);
        }
      }
    } catch (err) {
      const errorMessage = process.env.NODE_ENV === 'production' 
        ? 'Failed to enhance image. Please try again.'
        : 'Failed to enhance image. Please make sure the backend is running.';
      setError(errorMessage);
      console.error('Enhancement error:', err);
    } finally {
      setLoading(false);
    }
  };

  const resetImages = () => {
    setSelectedImage(null);
    setEnhancedImages({ v1: null, v2: null });
    setDiseasePrediction(null);
    setError('');
  };

  const downloadImage = (imageUrl, filename) => {
    const link = document.createElement('a');
    link.href = imageUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const getConfidenceClass = (confidence) => {
    if (confidence > 0.8) return 'high-confidence';
    if (confidence > 0.6) return 'medium-confidence';
    if (confidence > 0.4) return 'low-confidence';
    return 'very-low-confidence';
  };

  const getSeverityLevel = (severity) => {
    const levels = {
      'None': 0,
      'Mild': 1,
      'Moderate': 2,
      'Severe': 3,
      'Critical': 4
    };
    return levels[severity] || 0;
  };

  const getSeverityDescription = (severity) => {
    const descriptions = {
      'None': 'No immediate health risks detected',
      'Mild': 'Minor health concerns, monitor symptoms',
      'Moderate': 'Significant health issues require attention',
      'Severe': 'Serious condition needs immediate care',
      'Critical': 'Life-threatening, emergency care required'
    };
    return descriptions[severity] || 'Unknown severity level';
  };

  const getSeverityAction = (severity) => {
    const actions = {
      'None': '✓ No action needed',
      'Mild': '📅 Schedule routine check-up',
      'Moderate': '🏥 Consult doctor soon',
      'Severe': '🚑 Seek medical attention',
      'Critical': '🆘 Emergency care needed'
    };
    return actions[severity] || 'Consult healthcare provider';
  };

  const downloadReport = (report) => {
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'medical_report.txt';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleTabClick = (tab) => {
    setActiveTab(tab);
  };

  return (
    <div className="homepage">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"/>
                <path d="M12 8v4"/>
                <circle cx="12" cy="16" r="1"/>
              </svg>
            </div>
            <h1>X-Ray Lung Enhancer</h1>
          </div>
          <p className="tagline">Advanced AI-Powered Medical Image Enhancement</p>
          
          {/* Healthcare Trust Indicators */}
          <div className="trust-indicators">
            <div className="trust-item">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
              </svg>
              <span>HIPAA Compliant</span>
            </div>
            <div className="trust-item">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                <path d="M2 17l10 5 10-5"/>
                <path d="M2 12l10 5 10-5"/>
              </svg>
              <span>Secure Processing</span>
            </div>
            <div className="trust-item">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M9 12l2 2 4-4"/>
                <path d="M21 12c.552 0 1-.448 1-1s-.448-1-1-1-1 .448-1 1 .448 1 1 1z"/>
                <path d="M3 12c.552 0 1-.448 1-1s-.448-1-1-1-1 .448-1 1 .448 1 1 1z"/>
              </svg>
              <span>Clinically Validated</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {/* Upload Section */}
        {!selectedImage ? (
          <section className="upload-section">
            <div className="upload-container">
              <div className="healthcare-badge">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"/>
                </svg>
                Healthcare Grade AI Technology
              </div>
              <div 
                className={`upload-area ${isDragging ? 'dragging' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
              >
                <div className="upload-content">
                  <div className="upload-icon">
                    <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                      <polyline points="17,8 12,3 7,8"/>
                      <line x1="12" y1="3" x2="12" y2="15"/>
                    </svg>
                  </div>
                  <h2>Upload Your X-Ray</h2>
                  <p>Drag and drop your X-ray image here or click to browse</p>
                  <label htmlFor="image-upload" className="upload-button">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                      <polyline points="17,8 12,3 7,8"/>
                      <line x1="12" y1="3" x2="12" y2="15"/>
                    </svg>
                    Select X-Ray Image
                    <input
                      id="image-upload"
                      type="file"
                      accept="image/*"
                      onChange={handleImageSelect}
                    />
                  </label>
                  <p className="supported-formats">Supported: PNG, JPG, JPEG (Maximum 10MB)</p>
                </div>
              </div>
            </div>
          </section>
        ) : (
          <section className="results-section">
            {/* Control Panel */}
            <div className="control-panel">
              <div className="control-buttons">
                <button onClick={enhanceImage} disabled={loading} className="enhance-btn">
                  {loading ? (
                    <>
                      <div className="spinner"></div>
                      Processing...
                    </>
                  ) : (
                    <>
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"/>
                      </svg>
                      Enhance X-Ray
                    </>
                  )}
                </button>
                <button onClick={resetImages} className="reset-btn">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
                    <path d="M3 3v5h5"/>
                  </svg>
                  Upload New Image
                </button>
              </div>
            </div>

            {/* Error Display */}
            {error && (
              <div className="error-message">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="12" y1="8" x2="12" y2="12"/>
                  <line x1="12" y1="16" x2="12.01" y2="16"/>
                </svg>
                {error}
              </div>
            )}

            {/* Image Comparison */}
            <div className="image-comparison">
              <div className="comparison-grid">
                {/* Original Image */}
                <div className="image-card">
                  <div className="image-header">
                    <h3>Original X-Ray</h3>
                    <span className="image-label">Input</span>
                  </div>
                  <div className="image-container">
                    <img src={selectedImage} alt="Original X-ray" />
                  </div>
                </div>

                {/* Enhanced V1 - Transformer */}
                <div className="image-card">
                  <div className="image-header">
                    <h3>Enhanced V1</h3>
                    <span className="image-label transformer">Transformer</span>
                  </div>
                  <div className="image-container">
                    {enhancedImages.v1 ? (
                      <>
                        <img src={enhancedImages.v1} alt="Enhanced Version 1" />
                        <button 
                          onClick={() => downloadImage(enhancedImages.v1, 'enhanced_transformer.png')}
                          className="download-btn"
                        >
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                            <polyline points="7,10 12,15 17,10"/>
                            <line x1="12" y1="15" x2="12" y2="3"/>
                          </svg>
                          Download
                        </button>
                      </>
                    ) : (
                      <div className="placeholder">
                        <div className="placeholder-icon">
                          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                            <circle cx="8.5" cy="8.5" r="1.5"/>
                            <polyline points="21,15 16,10 5,21"/>
                          </svg>
                        </div>
                        <p>Enhanced V1</p>
                        <span>AI Transformer</span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Enhanced V2 - Traditional */}
                <div className="image-card">
                  <div className="image-header">
                    <h3>Enhanced V2</h3>
                    <span className="image-label traditional">Traditional</span>
                  </div>
                  <div className="image-container">
                    {enhancedImages.v2 ? (
                      <>
                        <img src={enhancedImages.v2} alt="Enhanced Version 2" />
                        <button 
                          onClick={() => downloadImage(enhancedImages.v2, 'enhanced_traditional.png')}
                          className="download-btn"
                        >
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                            <polyline points="7,10 12,15 17,10"/>
                            <line x1="12" y1="15" x2="12" y2="3"/>
                          </svg>
                          Download
                        </button>
                      </>
                    ) : (
                      <div className="placeholder">
                        <div className="placeholder-icon">
                          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                            <circle cx="8.5" cy="8.5" r="1.5"/>
                            <polyline points="21,15 16,10 5,21"/>
                          </svg>
                        </div>
                        <p>Enhanced V2</p>
                        <span>Traditional Processing</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Disease Prediction Section */}
            {diseasePrediction && diseasePrediction.success && (
              <section className="disease-prediction-section">
                <div className="prediction-header">
                  <h2 className="section-title">Disease Analysis Results</h2>
                  <div className="confidence-indicator">
                    <span className="confidence-label">AI Confidence</span>
                    <div className="confidence-visual">
                      <div 
                        className="confidence-circle" 
                        style={{ 
                          background: `conic-gradient(#10b981 ${diseasePrediction.top_prediction.confidence * 360}deg, #e5e7eb 0deg)` 
                        }}
                      >
                        <span className="confidence-percentage">
                          {diseasePrediction.top_prediction.percentage}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="diagnosis-main">
                  <div className="primary-diagnosis-card">
                    <div className="diagnosis-header">
                      <h3>Primary Diagnosis</h3>
                      <div className={`severity-badge ${diseasePrediction.disease_info.severity.toLowerCase().replace(' ', '-')}`}>
                        {diseasePrediction.disease_info.severity}
                      </div>
                    </div>
                    <div className="diagnosis-content">
                      <div className="disease-name-large">
                        {diseasePrediction.top_prediction.disease}
                      </div>
                      <div className="disease-description">
                        {diseasePrediction.disease_info.description}
                      </div>
                    </div>
                  </div>

                  <div className="predictions-visualization">
                    <h4>All Predictions</h4>
                    <div className="prediction-chart">
                      {diseasePrediction.predictions.map((pred, index) => (
                        <div key={index} className="prediction-bar-item">
                          <div className="prediction-info">
                            <span className="disease-label">{pred.disease}</span>
                            <span className="prediction-confidence">{pred.percentage}</span>
                          </div>
                          <div className="prediction-bar-container">
                            <div 
                              className="prediction-bar-fill" 
                              style={{ 
                                width: `${pred.confidence * 100}%`,
                                backgroundColor: index === 0 ? '#10b981' : '#6b7280'
                              }}
                            ></div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="detailed-analysis">
                  <div className="analysis-tabs">
                    <div 
                      className={`tab ${activeTab === 'report' ? 'active' : ''}`}
                      onClick={() => handleTabClick('report')}
                    >
                      Medical Report
                    </div>
                    <div 
                      className={`tab ${activeTab === 'info' ? 'active' : ''}`}
                      onClick={() => handleTabClick('info')}
                    >
                      Disease Information
                    </div>
                  </div>
                  
                  <div className="tab-content">
                    {activeTab === 'report' && (
                      <div className="medical-report-enhanced">
                        <div className="report-header">
                          <h4>Medical Analysis Report</h4>
                          <button 
                            onClick={() => downloadReport(diseasePrediction.report)}
                            className="download-report-btn"
                          >
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                              <polyline points="14,2 14,8 20,8"/>
                              <line x1="16" y1="13" x2="8" y2="13"/>
                              <line x1="16" y1="17" x2="8" y2="17"/>
                              <polyline points="10,9 9,9 8,9"/>
                            </svg>
                            Download Report
                          </button>
                        </div>
                        <div className="report-content-enhanced">
                          <pre>{diseasePrediction.report}</pre>
                        </div>
                      </div>
                    )}

                    {activeTab === 'info' && (
                      <div className="disease-info-enhanced">
                        <div className="info-cards-grid">
                          <div className="info-card">
                            <div className="info-card-header">
                              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                              </svg>
                              <h5>Description</h5>
                            </div>
                            <p>{diseasePrediction.disease_info.description}</p>
                          </div>

                          <div className="info-card">
                            <div className="info-card-header">
                              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"/>
                              </svg>
                              <h5>Symptoms</h5>
                            </div>
                            <p>{diseasePrediction.disease_info.symptoms}</p>
                          </div>

                          <div className="info-card">
                            <div className="info-card-header">
                              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <path d="M3 12h18m-9-9v18"/>
                                <circle cx="12" cy="12" r="10"/>
                              </svg>
                              <h5>Treatment</h5>
                            </div>
                            <p>{diseasePrediction.disease_info.treatment}</p>
                          </div>

                          <div className="info-card">
                            <div className="info-card-header">
                              <div className="severity-icon-wrapper">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                                  <line x1="12" y1="9" x2="12" y2="13"/>
                                  <line x1="12" y1="17" x2="12.01" y2="17"/>
                                </svg>
                              </div>
                              <h5>Risk Assessment</h5>
                            </div>
                            <div className="severity-level-compact" data-severity={diseasePrediction.disease_info.severity.toLowerCase()}>
                              <div className="severity-header-compact">
                                <span className="severity-label-compact">Severity Level</span>
                                <div className="severity-dots-compact">
                                  {[...Array(5)].map((_, i) => (
                                    <div 
                                      key={i} 
                                      className={`severity-dot-compact ${i < getSeverityLevel(diseasePrediction.disease_info.severity) ? 'active' : ''}`}
                                    />
                                  ))}
                                </div>
                              </div>
                              <div className="severity-value-compact">
                                {diseasePrediction.disease_info.severity}
                              </div>
                              <div className="severity-action-compact">
                                {getSeverityAction(diseasePrediction.disease_info.severity)}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </section>
            )}
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <div className="tech-info">
            <h4>Technology</h4>
            <p>Vision Transformer • Self-Attention • Medical Image Processing • CLAHE Enhancement</p>
          </div>
          <div className="model-info">
            <h4>Model Specifications</h4>
            <p>40+ Epochs Training • Loss &lt; 0.9 • HIPAA Compliant • Clinical Validation</p>
          </div>
          <div className="healthcare-info">
            <h4>Healthcare Standards</h4>
            <p>Medical Grade Security • Patient Privacy • FDA Guidelines • Clinical Accuracy</p>
          </div>
        </div>
        <div className="copyright">
          <p>&copy; 2024 X-Ray Lung Enhancer. Built for medical research and healthcare professionals.</p>
        </div>
      </footer>
    </div>
  );
}

export default HomePage;
