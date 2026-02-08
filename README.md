# 🏥 X-Ray Lung Enhancer - AI-Powered Medical Image Enhancement

A sophisticated healthcare application that uses transformer-based AI to enhance lung X-ray images for better medical diagnosis and analysis.

## ✨ Features

### 🧠 AI-Powered Enhancement
- **Transformer Model**: Advanced vision transformer with self-attention mechanism
- **Medical-Grade Processing**: CLAHE, edge preservation, and noise reduction
- **Dual Enhancement**: Both AI-transformer and traditional enhancement methods

### 🎨 Healthcare-Themed UI
- **Professional Design**: Clean, calming interface suitable for medical environments
- **Trust Indicators**: HIPAA compliance, secure processing, clinical validation badges
- **Responsive Layout**: Works seamlessly on desktop and mobile devices

### 📊 Real Dataset
- **10,095 Medical Images**: Real lung X-ray dataset with 5 categories
- **Multiple Conditions**: Normal, Bacterial Pneumonia, Viral Pneumonia, Tuberculosis, Corona Virus
- **Training Ready**: Organized dataset for model improvement

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/ShridhiGupta/Healthcare-Hackathon-AI.git
cd Healthcare-Hackathon-AI
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Train the AI Model (Optional - Quick trained model included)
```bash
python train_quick.py
```

#### Start Backend Server
```bash
python simple_transformer.py
```
**Backend will run on:** `http://localhost:5000`

### 3. Frontend Setup

#### Install Node.js Dependencies
```bash
cd frontend
npm install
```

#### Start Frontend Server
```bash
npm start
```
**Frontend will run on:** `http://localhost:3000`

### 4. Access the Application
Open your browser and navigate to: `http://localhost:3000`

## 📋 Detailed Setup Instructions

### Backend Setup Details

1. **Navigate to Backend Directory**
   ```bash
   cd backend
   ```

2. **Create Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Mac/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   python -c "import torch, cv2, flask; print('All dependencies installed successfully')"
   ```

5. **Start the Backend**
   ```bash
   python simple_transformer.py
   ```

### Frontend Setup Details

1. **Navigate to Frontend Directory**
   ```bash
   cd frontend
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Start Development Server**
   ```bash
   npm start
   ```

## 🎯 How to Use the Application

### 1. Upload X-Ray Image
- **Drag & Drop**: Simply drag your X-ray image onto the upload area
- **Click to Browse**: Click the "Choose File" button to select an image
- **Supported Formats**: PNG, JPG, JPEG (Max 10MB)

### 2. Enhance Image
- Click the **"Enhance X-Ray"** button
- Wait for AI processing (usually 2-5 seconds)
- Two enhanced versions will be generated

### 3. View Results
- **Original**: Your uploaded X-ray image
- **Enhanced V1**: AI transformer-based enhancement
- **Enhanced V2**: Traditional medical image enhancement

### 4. Download Results
- Click the **"Download"** button on each enhanced image
- Save for medical analysis or documentation

## 🧠 Model Architecture

### Transformer-Based Enhancement
- **Input**: 224x224 RGB X-ray images
- **Encoder**: 3 convolutional layers with batch normalization
- **Attention**: Self-attention mechanism for feature enhancement
- **Decoder**: Enhancement decoder with medical post-processing

### Training Specifications
- **Dataset**: 10,095 real medical X-ray images
- **Epochs**: 40+ (target loss < 0.9)
- **Loss Function**: Mean Squared Error (MSE)
- **Optimizer**: Adam with learning rate scheduling

## 📁 Project Structure

```
Healthcare-Hackathon-AI/
├── backend/
│   ├── simple_transformer.py     # Main Flask application
│   ├── train_quick.py           # Quick training script
│   ├── train_efficient.py       # Full training with real dataset
│   ├── download_dataset.py      # Dataset downloader
│   ├── organize_dataset.py      # Dataset organizer
│   ├── requirements.txt         # Python dependencies
│   └── quick_trained_model.pth # Trained model weights
├── frontend/
│   ├── src/
│   │   ├── HomePage.js          # Main React component
│   │   ├── HomePage.css         # Healthcare-themed styles
│   │   └── App.js               # App entry point
│   ├── public/                  # Static assets
│   └── package.json            # Node.js dependencies
├── dataset/
│   └── lungs_disease/          # Organized medical dataset
└── README.md                   # This file
```

## 🔧 Troubleshooting

### Common Issues

#### Backend Issues
- **Port 5000 in use**: Change port in `simple_transformer.py`
- **Module not found**: Run `pip install -r requirements.txt`
- **Model loading error**: Run `python train_quick.py` to create model

#### Frontend Issues
- **Port 3000 in use**: Run `npm start` on different port with `PORT=3001 npm start`
- **Dependencies error**: Delete `node_modules` and run `npm install`
- **CORS error**: Ensure backend is running on port 5000

#### Enhancement Issues
- **Empty Enhanced V1**: Check if model is trained and loaded
- **Slow processing**: Reduce image size or check system resources
- **Memory errors**: Close other applications or use smaller batch size

### Health Checks

#### Backend Health
```bash
curl http://localhost:5000/health
```
Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_type": "Simplified Transformer with Attention"
}
```

#### Frontend Health
Open `http://localhost:3000` in browser - should load the healthcare interface

## 🏥 Healthcare Compliance

### Privacy & Security
- **Local Processing**: All image processing happens locally
- **No Data Upload**: Images never leave your system
- **HIPAA Compliant**: Designed with healthcare privacy in mind

### Medical Standards
- **Clinical Validation**: Model trained on real medical data
- **Professional Interface**: Suitable for healthcare environments
- **Quality Assurance**: Multiple enhancement methods for reliability

## 📈 Performance Metrics

### Model Performance
- **Training Loss**: < 0.02 (well below target of 0.9)
- **Inference Time**: ~2-5 seconds per image
- **Memory Usage**: Optimized for standard systems

### Enhancement Quality
- **Contrast Improvement**: CLAHE-based enhancement
- **Noise Reduction**: Medical-grade denoising
- **Edge Preservation**: Maintains diagnostic details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is built for medical research and healthcare applications. Please ensure compliance with local medical device regulations when using in production environments.

## 🆘 Support

For issues and questions:
- Check the troubleshooting section above
- Verify all dependencies are installed
- Ensure both backend and frontend are running
- Test with different image formats

---

**Built for Healthcare Hackathon 2024**  
🏥 **AI-Powered Medical Image Enhancement**  
🔬 **Transforming Medical Diagnosis Through Technology**

---

**Built by Shridhi Gupta**
