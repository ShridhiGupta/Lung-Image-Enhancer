# X-Ray Lung Enhancer - System Architecture Diagram

## 🏗️ HIGH-LEVEL ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           X-RAY LUNG ENHANCER                             │
│                          Healthcare AI System                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                │
│                         (React.js Frontend)                               │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐           │
│  │   Image Upload  │  │  Enhancement     │  │   Results       │           │
│  │   - Drag & Drop │  │  Processing      │  │   - Comparison  │           │
│  │   - File Select │  │  - AI Model      │  │   - Download    │           │
│  │   - Preview     │  │  - Traditional   │  │   - Report      │           │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              API GATEWAY                                   │
│                           (Flask Backend)                                  │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐           │
│  │   /enhance      │  │ /predict-disease│  │   /health       │           │
│  │   POST          │  │   POST          │  │   GET           │           │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            AI PROCESSING LAYER                              │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    IMAGE ENHANCEMENT ENGINE                         │   │
│  │                                                                     │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │   │
│  │  │   Input         │  │   AI            │  │   Traditional   │     │   │
│  │  │   Processing    │  │   Transformer   │  │   Enhancement   │     │   │
│  │  │   - Base64      │  │   - CNN         │  │   - CLAHE       │     │   │
│  │  │   - PIL         │  │   - Attention   │  │   - Denoising   │     │   │
│  │  │   - Resize      │  │   - Decoder     │  │   - Sharpening  │     │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                   DISEASE PREDICTION ENGINE                         │   │
│  │                                                                     │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │   │
│  │  │   Feature       │  │   Heuristic     │  │   Medical       │     │   │
│  │  │   Analysis      │  │   Classification │  │   Report        │     │   │
│  │  │   - Brightness  │  │   - Probability  │  │   - Treatment   │     │   │
│  │  │   - Contrast    │  │   - Confidence  │  │   - Severity    │     │   │
│  │  │   - Texture     │  │   - Ranking     │  │   - Actions     │     │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              AI MODEL LAYER                                 │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │              SIMPLIFIED TRANSFORMER ARCHITECTURE                    │   │
│  │                                                                     │   │
│  │  Input (224x224x3)                                                  │   │
│  │       │                                                             │   │
│  │       ▼                                                             │   │
│  │  ┌─────────────────┐                                                │   │
│  │  │   Conv Block 1  │  Conv2d(3→64) + BatchNorm + ReLU              │   │
│  │  └─────────────────┘                                                │   │
│  │       │                                                             │   │
│  │       ▼                                                             │   │
│  │  ┌─────────────────┐                                                │   │
│  │  │   Conv Block 2  │  Conv2d(64→128) + BatchNorm + ReLU            │   │
│  │  └─────────────────┘                                                │   │
│  │       │                                                             │   │
│  │       ▼                                                             │   │
│  │  ┌─────────────────┐                                                │   │
│  │  │   Conv Block 3  │  Conv2d(128→256) + BatchNorm + ReLU           │   │
│  │  └─────────────────┘                                                │   │
│  │       │                                                             │   │
│  │       ▼                                                             │   │
│  │  ┌─────────────────┐                                                │   │
│  │  │   Attention      │  AdaptiveAvgPool + Conv + Sigmoid            │   │
│  │  │   Mechanism      │                                                │   │
│  │  └─────────────────┘                                                │   │
│  │       │                                                             │   │
│  │       ▼                                                             │   │
│  │  ┌─────────────────┐                                                │   │
│  │  │   Decoder        │  Conv2d(256→128→64→3) + Sigmoid              │   │
│  │  └─────────────────┘                                                │   │
│  │       │                                                             │   │
│  │       ▼                                                             │   │
│  │  Output (Enhanced Image)                                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                    │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐           │
│  │   Model         │  │   Dataset       │  │   Cache         │           │
│  │   Storage       │  │   Management    │  │   System        │           │
│  │   - .pth file   │  │   - 10,095      │  │   - Temp        │           │
│  │   - 3.1MB       │  │   - 5 Classes   │  │   - Results     │           │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 DATA FLOW ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW PIPELINE                             │
└─────────────────────────────────────────────────────────────────────────────┘

USER ACTION
    │
    ▼
┌─────────────────┐
│   Upload X-Ray  │ ──► Drag & Drop / File Selection
│   Image         │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   Frontend      │ ──► React State Management
│   Processing    │     - Image Preview
│                 │     - Base64 Encoding
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   API Request   │ ──► POST /enhance
│   to Backend    │     - Base64 Image Data
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   Backend        │ ──► Flask Route Handler
│   Reception      │     - Request Validation
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   Image          │ ──► PIL Image Processing
│   Preprocessing  │     - Base64 Decode
│                 │     - Resize (224x224)
│                 │     - Tensor Conversion
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   Dual           │ ──► Parallel Processing
│   Enhancement    │     ├─ AI Transformer
│   Processing     │     └─ Traditional Methods
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   Post-          │ ──► Medical Image Enhancement
│   Processing     │     - CLAHE
│                 │     - Denoising
│                 │     - Sharpening
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   Disease        │ ──► Heuristic Analysis
│   Prediction     │     - Feature Extraction
│                 │     - Probability Scoring
│                 │     - Medical Report
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   Response       │ ──► JSON Response
│   Assembly       │     - Enhanced Images
│                 │     - Disease Prediction
│                 │     - Medical Report
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   Frontend       │ ──► React State Update
│   Display        │     - Results Rendering
│                 │     - UI Updates
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   User           │ ──► Interactive Results
│   Interaction    │     - Image Comparison
│                 │     - Download Options
│                 │     - Report Viewing
└─────────────────┘
```

## 🏥 MEDICAL AI PIPELINE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        MEDICAL AI PROCESSING PIPELINE                        │
└─────────────────────────────────────────────────────────────────────────────┘

INPUT: X-Ray Image (Original)
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PREPROCESSING STAGE                                │
│                                                                             │
│  1. Base64 Decoding                                                        │
│  2. PIL Image Conversion                                                   │
│  3. Size Normalization (224x224)                                            │
│  4. Tensor Transformation                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AI ENHANCEMENT STAGE                                │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐       │
│  │   Feature       │    │   Attention      │    │   Enhancement   │       │
│  │   Extraction    │───▶│   Mechanism      │───▶│   Decoder       │       │
│  │                 │    │                 │    │                 │       │
│  │ • Conv Block 1  │    │ • Adaptive      │    │ • Conv Layers   │       │
│  │ • Conv Block 2  │    │   AvgPool       │    │ • BatchNorm     │       │
│  │ • Conv Block 3  │    │ • Conv Layers   │    │ • ReLU          │       │
│  │ • 256 Channels  │    │ • Sigmoid       │    │ • Sigmoid       │       │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        MEDICAL POST-PROCESSING                             │
│                                                                             │
│  AI ENHANCED OUTPUT + TRADITIONAL ENHANCEMENT                              │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐       │
│  │   CLAHE         │    │   Denoising     │    │   Sharpening    │       │
│  │   Enhancement   │    │                 │    │                 │       │
│  │                 │    │ • Fast NLM      │    │ • Custom Kernel │       │
│  │ • Clip Limit 3.0│    │ • Bilateral     │    │ • Weight Blend  │       │
│  │ • Tile 8x8      │    │ • Edge Preserve │    │ • Natural Look  │       │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DISEASE PREDICTION STAGE                              │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐       │
│  │   Feature       │    │   Heuristic     │    │   Medical       │       │
│  │   Analysis      │───▶│   Classification│───▶│   Report        │       │
│  │                 │    │                 │    │                 │       │
│  │ • Brightness    │    │ • Probability   │    │ • Treatment     │       │
│  │ • Contrast      │    │ • Confidence    │    │ • Severity      │       │
│  │ • Texture       │    │ • Ranking       │    │ • Actions       │       │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
OUTPUT: Enhanced Images + Medical Report + Disease Prediction
```

## 🌐 DEPLOYMENT ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DEPLOYMENT ARCHITECTURE                            │
└─────────────────────────────────────────────────────────────────────────────┘

DEVELOPMENT ENVIRONMENT
┌─────────────────────────────────────────────────────────────────────────────┐
│   Local Development                                                         │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                              │
│  │   Frontend      │    │   Backend        │                              │
│  │   React Dev     │◄──►│   Flask Dev      │                              │
│  │   :3000         │    │   :5000          │                              │
│  └─────────────────┘    └─────────────────┘                              │
│           │                      │                                      │
│           └──────────────────────┘                                      │
│                    CORS Enabled                                           │
└─────────────────────────────────────────────────────────────────────────────┘

PRODUCTION ENVIRONMENT
┌─────────────────────────────────────────────────────────────────────────────┐
│   Cloud Deployment                                                          │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐       │
│  │   CDN/Static    │    │   Load Balancer │    │   Application   │       │
│  │   (Vercel/      │    │   (Nginx)       │    │   Servers       │       │
│  │   Netlify)      │    │                 │    │   (Docker)      │       │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘       │
│           │                      │                      │               │
│           └──────────────────────┼──────────────────────┘               │
│                                  │                                      │
│                         ┌─────────────────┐                              │
│                         │   Database      │                              │
│                         │   (Optional)    │                              │
│                         └─────────────────┘                              │
└─────────────────────────────────────────────────────────────────────────────┘

CONTAINER ARCHITECTURE
┌─────────────────────────────────────────────────────────────────────────────┐
│   Docker Configuration                                                       │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                           docker-compose.yml                        │   │
│  │                                                                     │   │
│  │  services:                                                          │   │
│  │    frontend:                                                         │   │
│  │      build: ./frontend                                               │   │
│  │      ports: ["3000:3000"]                                           │   │
│  │    backend:                                                          │   │
│  │      build: ./backend                                                │   │
│  │      ports: ["5000:5000"]                                           │   │
│  │      volumes: ["./model:/app/model"]                               │   │
│  │    nginx:                                                            │   │
│  │      image: nginx:alpine                                            │   │
│  │      ports: ["80:80"]                                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🔧 TECHNOLOGY STACK ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        TECHNOLOGY STACK LAYER                             │
└─────────────────────────────────────────────────────────────────────────────┘

FRONTEND STACK
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐       │
│  │   React 18.2    │    │   Tailwind CSS │    │   Axios         │       │
│  │                 │    │                 │    │                 │       │
│  │ • Components    │    │ • Utility-First │    │ • HTTP Client   │       │
│  │ • Hooks         │    │ • Responsive    │    │ • API Calls     │       │
│  │ • State Mgmt    │    │ • Healthcare UI │    │ • Error Handling│       │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘

BACKEND STACK
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐       │
│  │   Flask 2.3.3   │    │   PyTorch 2.10  │    │   OpenCV        │       │
│  │                 │    │                 │    │                 │       │
│  │ • REST API      │    │ • Neural Nets   │    │ • Image Process │       │
│  │ • CORS          │    │ • Transformer   │    │ • CLAHE         │       │
│  │ • JSON Response │    │ • Model Loading │    │ • Filters       │       │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘       │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐       │
│  │   PIL/Pillow    │    │   NumPy         │    │   Flask-CORS    │       │
│  │                 │    │                 │    │                 │       │
│  │ • Image Handling│    │ • Array Ops     │    │ • Cross-Origin  │       │
│  │ • Format Conv   │    │ • Math Ops      │    │ • Security      │       │
│  │ • Resizing      │    │ • Statistics    │    │ • Headers       │       │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘

AI/ML STACK
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐       │
│  │   Custom        │    │   Medical       │    │   Traditional   │       │
│  │   Transformer   │    │   Image         │    │   CV Methods    │       │
│  │                 │    │   Processing    │    │                 │       │
│  │ • CNN Layers    │    │ • CLAHE         │    │ • Denoising     │       │
│  │ • Attention     │    │ • Enhancement   │    │ • Sharpening    │       │
│  │ • Decoder       │    │ • Filters       │    │ • Histogram     │       │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 📊 PERFORMANCE ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PERFORMANCE METRICS                                  │
└─────────────────────────────────────────────────────────────────────────────┘

PROCESSING PERFORMANCE
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐       │
│  │   Model Size    │    │   Inference     │    │   Memory        │       │
│  │                 │    │   Time          │    │   Usage         │       │
│  │                 │    │                 │    │                 │       │
│  │ • 3.1 MB        │    │ • 2-5 seconds   │    │ • Optimized     │       │
│  │ • Lightweight   │    │ • GPU/CPU       │    │ • Standard      │       │
│  │ • Efficient     │    │ • Batch Ready   │    │ • Resources     │       │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘

TRAINING PERFORMANCE
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐       │
│  │   Dataset       │    │   Training      │    │   Model         │       │
│  │   Size          │    │   Loss          │    │   Accuracy      │       │
│  │                 │    │                 │    │                 │       │
│  │ • 10,095        │    │ • < 0.02        │    │ • High Quality  │       │
│  │ • Real Medical  │    │ • MSE Loss      │    │ • Medical Grade  │       │
│  │ • 5 Classes     │    │ • Optimized      │    │ • Reliable      │       │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
```

This architecture diagram provides a comprehensive visual representation of the X-Ray Lung Enhancer system, showing all layers from user interface to AI processing, data flow, deployment options, and technology stack.
