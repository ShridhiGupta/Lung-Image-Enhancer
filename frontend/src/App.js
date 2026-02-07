import React, { useState } from 'react';
import axios from 'axios';
import './index.css';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [enhancedImages, setEnhancedImages] = useState({ v1: null, v2: null });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleImageSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedImage(reader.result);
        setEnhancedImages({ v1: null, v2: null });
        setError('');
      };
      reader.readAsDataURL(file);
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-7xl mx-auto">
        <header className="text-center mb-8 pt-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            X-Ray Lung Enhancer
          </h1>
          <p className="text-gray-600 text-lg">
            AI-powered enhancement using transformer technology
          </p>
        </header>

        <div className="bg-white rounded-2xl shadow-xl p-8">
          {!selectedImage ? (
            <div className="text-center">
              <div className="border-4 border-dashed border-gray-300 rounded-xl p-12 hover:border-indigo-500 transition-colors">
                <svg className="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <label htmlFor="image-upload" className="cursor-pointer">
                  <span className="text-xl text-gray-600 mb-2 block">
                    Click to upload X-ray image
                  </span>
                  <span className="text-sm text-gray-500">
                    PNG, JPG up to 10MB
                  </span>
                  <input
                    id="image-upload"
                    type="file"
                    className="hidden"
                    accept="image/*"
                    onChange={handleImageSelect}
                  />
                </label>
              </div>
            </div>
          ) : (
            <div>
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-semibold text-gray-800">
                  Original X-Ray
                </h2>
                <button
                  onClick={resetImages}
                  className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
                >
                  Upload New Image
                </button>
              </div>

              <div className="grid md:grid-cols-3 gap-6 mb-8">
                <div className="text-center">
                  <div className="bg-gray-100 rounded-lg p-4 mb-3">
                    <img
                      src={selectedImage}
                      alt="Original X-ray"
                      className="w-full h-64 object-contain rounded"
                    />
                  </div>
                  <h3 className="font-medium text-gray-700">Original</h3>
                </div>

                <div className="text-center">
                  <div className="bg-gray-100 rounded-lg p-4 mb-3">
                    {enhancedImages.v1 ? (
                      <img
                        src={enhancedImages.v1}
                        alt="Enhanced Version 1"
                        className="w-full h-64 object-contain rounded"
                      />
                    ) : (
                      <div className="w-full h-64 flex items-center justify-center text-gray-500">
                        <div className="text-center">
                          <svg className="mx-auto h-12 w-12 text-gray-400 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                          </svg>
                          <p>Enhanced V1</p>
                        </div>
                      </div>
                    )}
                  </div>
                  <h3 className="font-medium text-gray-700">Enhanced V1 (Transformer)</h3>
                </div>

                <div className="text-center">
                  <div className="bg-gray-100 rounded-lg p-4 mb-3">
                    {enhancedImages.v2 ? (
                      <img
                        src={enhancedImages.v2}
                        alt="Enhanced Version 2"
                        className="w-full h-64 object-contain rounded"
                      />
                    ) : (
                      <div className="w-full h-64 flex items-center justify-center text-gray-500">
                        <div className="text-center">
                          <svg className="mx-auto h-12 w-12 text-gray-400 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                          </svg>
                          <p>Enhanced V2</p>
                        </div>
                      </div>
                    )}
                  </div>
                  <h3 className="font-medium text-gray-700">Enhanced V2 (Traditional)</h3>
                </div>
              </div>

              <div className="text-center">
                <button
                  onClick={enhanceImage}
                  disabled={loading}
                  className={`px-8 py-3 rounded-lg font-semibold transition-all transform hover:scale-105 ${
                    loading
                      ? 'bg-gray-400 cursor-not-allowed'
                      : 'bg-indigo-600 text-white hover:bg-indigo-700 shadow-lg'
                  }`}
                >
                  {loading ? (
                    <span className="flex items-center">
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Processing...
                    </span>
                  ) : (
                    'Enhance X-Ray'
                  )}
                </button>
              </div>

              {error && (
                <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
                  {error}
                </div>
              )}
            </div>
          )}
        </div>

        <footer className="text-center mt-8 pb-8 text-gray-600">
          <p>Powered by Vision Transformer & Advanced Image Processing</p>
          <p className="text-sm mt-2">Model: 40+ epochs, Loss &lt; 0.9</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
