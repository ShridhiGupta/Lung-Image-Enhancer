import React, { useState } from 'react';
import axios from 'axios';
import './HomePage.css';

function HomePage() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [enhancedImages, setEnhancedImages] = useState({ v1: null, v2: null });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isDragging, setIsDragging] = useState(false);

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
      const response = await axios.post('http://localhost:5000/enhance', {
        image: selectedImage
      });

      if (response.data.enhanced_v1 && response.data.enhanced_v2) {
        setEnhancedImages({
          v1: response.data.enhanced_v1,
          v2: response.data.enhanced_v2
        });
      }
    } catch (err) {
      setError('Failed to enhance image. Please make sure the backend is running.');
      console.error('Enhancement error:', err);
    } finally {
      setLoading(false);
    }
  };

  const resetImages = () => {
    setSelectedImage(null);
    setEnhancedImages({ v1: null, v2: null });
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
                  <h2>Upload X-Ray Image</h2>
                  <p>Drag and drop your X-ray image here or click to browse</p>
                  <label htmlFor="image-upload" className="upload-button">
                    Choose File
                    <input
                      id="image-upload"
                      type="file"
                      accept="image/*"
                      onChange={handleImageSelect}
                    />
                  </label>
                  <p className="supported-formats">Supported formats: PNG, JPG, JPEG (Max 10MB)</p>
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
