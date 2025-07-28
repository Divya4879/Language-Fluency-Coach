# 🎙️ Speak Reflect Improve

Speak naturally and let our AI analyze your English proficiency across all areas

Check out my project's snapshots here:-

<img width="1920" height="1386" alt="screencapture-127-0-0-1-5000-2025-07-28-05_40_34" src="https://github.com/user-attachments/assets/978e2d92-260b-41da-b3c8-a15650273258" />

<img width="1920" height="1677" alt="image" src="https://github.com/user-attachments/assets/5252ce6a-264c-4126-8b15-28f589fb63e7" />


Check it out here(live version) :- [Speak Reflect Improve](https://english-fluency-coach.onrender.com)

---

## Features

### 🎤 Speech Analysis
- **Pronunciation Assessment**: Detailed analysis of pronunciation clarity, accent, and intonation
- **Vocabulary Evaluation**: Assessment of vocabulary range, sophistication, and appropriateness
- **Grammar Analysis**: Grammar accuracy, sentence structure, and complexity evaluation
- **Fluency Assessment**: Speech flow, hesitation patterns, and filler word detection
- **Coherence & Organization**: Logical flow and idea connection analysis
- **Idioms & Phrases**: Natural expression and idiomatic usage evaluation

### 📊 Proficiency Grading
- **CEFR Level Assessment**: A1, A2, B1, B2, C1, C2 level determination
- **Overall Grade**: 1-10 scoring system with detailed explanations
- **Actionable Feedback**: Specific improvement recommendations

### 🤖 AI-Powered Coaching
- **Real-time Feedback**: Immediate corrections and suggestions
- **Personalized Tips**: Customized improvement strategies
- **Cultural Context**: Natural expressions and cultural nuances
- **Encouragement**: Motivational feedback to boost confidence

---

## Technology Stack

- **Backend**: Flask (Python)
- **AI Analysis**: Groq API with Llama3-8b-8192 model
- **Speech Recognition**: AssemblyAI
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Audio Processing**: Web Audio API, MediaRecorder API
- **Styling**: Custom CSS with dark green theme
- **Security**: HTTPS with self-signed certificates for microphone access

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- Modern web browser with microphone support
- Internet connection for AI API calls

### 1. Clone and Setup
```bash
cd /home/divya/Language-Fluency-Coach
pip install -r requirements.txt
```

### 2. Configure API Keys
Create `utils/api_keys_config.py` with your API keys:

```python
# Get your Groq API key from: https://console.groq.com/keys
GROQ_API_KEY = "gsk_your_groq_api_key_here"

# Get your AssemblyAI API key from: https://www.assemblyai.com/dashboard/
ASSEMBLYAI_API_KEY = "your_assemblyai_api_key_here"
```

### 3. Run the Application
```bash
python app.py
```

The application will:
- Create self-signed certificates for HTTPS
- Start on https://localhost:5000
- Display setup instructions in the terminal

### 4. Access the Application
1. Open https://localhost:5000 in your browser
2. Accept the security warning (click "Advanced" → "Proceed to localhost")
3. Allow microphone access when prompted

## API Configuration

### Groq API Setup
1. Visit https://console.groq.com/keys
2. Create an account and generate an API key
3. Add the key to your configuration file

### AssemblyAI Setup
1. Visit https://www.assemblyai.com/dashboard/
2. Sign up and get your API key
3. Add the key to your configuration file

---

## Usage Guide

### Taking an Assessment
1. Click "Start Assessment" on the home page
2. Choose assessment type:
   - **Quick Assessment**: 2-3 minute general proficiency test
   - **Comprehensive Assessment**: 5-7 minute detailed analysis
   - **Topic-Based Assessment**: Focused evaluation on specific topics
3. Click the microphone button and speak naturally
4. Review your detailed analysis and recommendations

### Understanding Your Results

#### Scoring System
- **1-3**: Beginner level, needs significant improvement
- **4-6**: Intermediate level, good foundation with areas to improve
- **7-8**: Advanced level, strong skills with minor refinements needed
- **9-10**: Proficient level, excellent command of English

#### CEFR Levels
- **A1-A2**: Basic user (Beginner to Elementary)
- **B1-B2**: Independent user (Intermediate to Upper-Intermediate)
- **C1-C2**: Proficient user (Advanced to Proficient)

---

## Features in Detail

### Speech Analysis Components
- **Pronunciation**: Clarity, accent, stress patterns, intonation
- **Vocabulary**: Range, sophistication, appropriateness, advanced word usage
- **Grammar**: Accuracy, sentence complexity, tense usage, error patterns
- **Fluency**: Speech flow, hesitation patterns, filler words, natural rhythm
- **Coherence**: Logical organization, idea connection, topic development
- **Idioms**: Natural expressions, phrasal verbs, colloquialisms

### Coaching Feedback
- **Immediate Feedback**: Positive reinforcement and acknowledgment
- **Corrections**: Specific errors with explanations and corrections
- **Pronunciation Notes**: Targeted pronunciation improvement tips
- **Vocabulary Enhancement**: Advanced word suggestions and usage examples
- **Grammar Improvements**: Specific grammar corrections and explanations
- **Fluency Tips**: Strategies to improve natural speech flow
- **Cultural Context**: Natural expressions and cultural nuances
- **Practice Suggestions**: Customized exercises for improvement
- **Encouragement**: Motivational messages and progress recognition

---

## Troubleshooting

### Microphone Issues
- Ensure microphone permissions are granted
- Use HTTPS (required for microphone access)
- Check browser compatibility (Chrome, Firefox, Safari recommended)
- Verify microphone is working in other applications

### API Issues
- Verify API keys are correctly configured
- Check internet connection
- Ensure API quotas are not exceeded
- Review console logs for specific error messages

### Audio Quality
- Use a quiet environment for recording
- Speak clearly and at normal volume
- Ensure stable internet connection for processing
- Use a good quality microphone if available

---

## Browser Compatibility
- **Chrome**: Full support (recommended)
- **Firefox**: Full support
- **Safari**: Full support
- **Edge**: Full support
- **Mobile browsers**: Limited support (microphone access varies)

---

## Security Notes
- The application uses HTTPS with self-signed certificates
- Audio data is processed securely and not stored permanently
- API keys should be kept confidential
- Temporary audio files are automatically cleaned up

---

## Development

### Project Structure
```
english-fluency-coach/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── utils/                # Utility modules
│   ├── api_keys.py       # API key management
│   ├── english_analyzer.py # Speech analysis engine
│   ├── voice_manager.py  # Audio processing
│   └── fluency_coach.py  # Coaching logic
├── templates/            # HTML templates
│   ├── index.html        # Main application
│   ├── assessment.html   # Assessment page
│   └── practice.html     # Practice page
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   └── js/
│       └── app.js        # Frontend JavaScript
└── temp/                 # Temporary audio files
```

---

## 🌐 Render Deployment - Complete Guide

### Step 1: Create Render Account

1. **Visit Render**: Go to [render.com](https://render.com)
2. **Sign Up**: Click "Get Started" → "Sign up with GitHub" (recommended)
3. **Authorize GitHub**: Allow Render to access your repositories
4. **Verify Email**: Check your email and verify your account

### Step 2: Prepare Your Repository

### Step 3: Connect GitHub Repository

1. **Login to Render Dashboard**: Go to [dashboard.render.com](https://dashboard.render.com)
2. **New Web Service**: Click "New +" → "Web Service"
3. **Connect Repository**: 
   - If first time: Click "Connect GitHub" → Authorize Render
   - Select your `Academic-Coach` repository
   - Click "Connect"

### Step 4: Configure Web Service

#### Basic Configuration:
- **Name**: `Academic-Coach` (or your preferred name)
- **Region**: Choose closest to your users (e.g., Oregon, Frankfurt, Singapore)
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave blank (uses repository root)

#### Build & Deploy Settings:
- **Runtime**: `Python 3`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  gunicorn app:app
  ```

#### Advanced Settings:
- **Instance Type**: `Free` (for testing) or `Starter` ($7/month for production)
- **Auto-Deploy**: `Yes` (deploys automatically on git push)

### Step 5: Environment Variables

In the **Environment** section, add these variables:

| Variable Name | Value | Notes |
|---------------|-------|-------|
| `GROQ_API_KEY` | `gsk_your-actual-groq-key` | Get from [console.groq.com](https://console.groq.com) |
| `ASSEMBLYAI_API_KEY` | `your-actual-assemblyai-key` | Get from [assemblyai.com](https://www.assemblyai.com) |

**To add environment variables:**
1. Scroll to "Environment Variables" section
2. Click "Add Environment Variable"
3. Enter key and value
4. Click "Save Changes"

### Step 6: Deploy

1. **Review Settings**: Double-check all configurations
2. **Create Web Service**: Click "Create Web Service"
3. **Monitor Build**: Watch the build logs in real-time
4. **Wait for Deployment**: First deployment takes 2-5 minutes
   
---

## License
This project is for educational and personal use. Please respect API terms of service for Groq and AssemblyAI.

---

**Happy Learning! 🎓**

Improve your English fluency with AI-powered personalized coaching.
