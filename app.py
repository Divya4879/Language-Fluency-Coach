from flask import Flask, render_template, request, jsonify, session
import os
import json
import sys
import ssl
from datetime import datetime
import requests
import tempfile
import re
from typing import Dict, List, Optional

try:
    import assemblyai as aai
    ASSEMBLYAI_AVAILABLE = True
except ImportError:
    ASSEMBLYAI_AVAILABLE = False

from utils.api_keys import get_api_keys
from utils.english_analyzer import EnglishAnalyzer
from utils.voice_manager import VoiceManager
from utils.fluency_coach import FluencyCoach

app = Flask(__name__)
app.secret_key = 'english_fluency_coach_secret_2024'

print("🔄 Initializing English Fluency Mastery Coach...")
api_keys = get_api_keys()
english_analyzer = EnglishAnalyzer(api_keys)
voice_manager = VoiceManager(api_keys)
fluency_coach = FluencyCoach(api_keys)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze_speech', methods=['POST'])
def analyze_speech():
    try:
        audio_file = request.files.get('audio')
        assessment_type = request.form.get('type', 'general')
        
        if not audio_file:
            return jsonify({'error': 'No audio file provided'}), 400
        
        # Save audio file temporarily
        session_id = session.get('session_id', datetime.now().strftime("%Y%m%d_%H%M%S"))
        session['session_id'] = session_id
        
        temp_path = f"temp/audio_{session_id}_{assessment_type}.wav"
        os.makedirs('temp', exist_ok=True)
        audio_file.save(temp_path)
        
        print(f"🔄 Starting speech analysis of {temp_path}")
        
        # Transcribe audio
        transcription = voice_manager.transcribe_audio(temp_path)
        
        if transcription.startswith("❌"):
            return jsonify({'error': transcription}), 500
        
        # Analyze English proficiency
        analysis = english_analyzer.analyze_speech_proficiency(
            transcription=transcription,
            audio_file_path=temp_path,
            assessment_type=assessment_type
        )
        
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        # Store analysis in session
        session['last_analysis'] = analysis
        session['last_transcription'] = transcription
        
        print(f"✅ Speech analysis completed: Grade {analysis.get('overall_grade', 'N/A')}")
        
        return jsonify({
            'success': True,
            'transcription': transcription,
            'analysis': analysis
        })
    
    except Exception as e:
        print(f"❌ Speech analysis error: {e}")
        return jsonify({'error': f'Speech analysis failed: {str(e)}'}), 500

@app.route('/practice_session', methods=['POST'])
def practice_session():
    try:
        data = request.json
        practice_type = data.get('type', 'conversation')
        topic = data.get('topic', 'general')
        user_input = data.get('input', '').strip()
        
        if not user_input:
            return jsonify({'error': 'No input provided'}), 400
        
        # Get coaching response
        coaching_response = fluency_coach.provide_coaching(
            user_input=user_input,
            practice_type=practice_type,
            topic=topic,
            user_level=session.get('user_level', 'intermediate')
        )
        
        # Store in session
        session['last_practice'] = {
            'type': practice_type,
            'topic': topic,
            'user_input': user_input,
            'coaching_response': coaching_response
        }
        
        return jsonify({
            'success': True,
            'coaching': coaching_response
        })
        
    except Exception as e:
        print(f"❌ Practice session error: {e}")
        return jsonify({'error': f'Practice session failed: {str(e)}'}), 500

@app.route('/transcribe_audio', methods=['POST'])
def transcribe_audio():
    try:
        audio_file = request.files.get('audio')
        if not audio_file:
            return jsonify({'error': 'No audio file provided'}), 400
        
        session_id = session.get('session_id', datetime.now().strftime("%Y%m%d_%H%M%S"))
        temp_path = f"temp/audio_{session_id}_transcribe.wav"
        os.makedirs('temp', exist_ok=True)
        audio_file.save(temp_path)
        
        print(f"🔄 Starting transcription of {temp_path}")
        
        transcription = voice_manager.transcribe_audio(temp_path)
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        print(f"✅ Transcription result: {transcription[:100]}...")
        
        return jsonify({
            'success': True,
            'transcription': transcription
        })
    
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return jsonify({'error': f'Transcription failed: {str(e)}'}), 500

@app.route('/get_practice_prompt', methods=['POST'])
def get_practice_prompt():
    try:
        data = request.json
        practice_type = data.get('type', 'conversation')
        topic = data.get('topic', 'general')
        level = data.get('level', 'intermediate')
        
        prompt = fluency_coach.generate_practice_prompt(
            practice_type=practice_type,
            topic=topic,
            level=level
        )
        
        return jsonify({
            'success': True,
            'prompt': prompt
        })
        
    except Exception as e:
        print(f"❌ Practice prompt error: {e}")
        return jsonify({'error': f'Failed to generate prompt: {str(e)}'}), 500

@app.route('/get_session_data')
def get_session_data():
    return jsonify({
        'session_id': session.get('session_id'),
        'user_level': session.get('user_level'),
        'last_analysis': session.get('last_analysis'),
        'last_transcription': session.get('last_transcription'),
        'last_practice': session.get('last_practice')
    })

@app.route('/reset_session', methods=['POST'])
def reset_session():
    session.clear()
    return jsonify({'success': True})

@app.route('/voice_status')
def voice_status():
    return jsonify(voice_manager.get_voice_status())

def create_self_signed_cert():
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        import datetime
        import ipaddress
        
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Local"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Local"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "English Fluency Coach"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.DNSName("127.0.0.1"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        with open("cert.pem", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        with open("key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print("✅ Self-signed certificate created")
        return True
        
    except ImportError:
        print("❌ cryptography package not available for HTTPS")
        return False
    except Exception as e:
        print(f"❌ Failed to create certificate: {e}")
        return False

if __name__ == '__main__':
    os.makedirs('temp', exist_ok=True)
    os.makedirs('static/audio', exist_ok=True)
    
    print("\n🎤 ENGLISH FLUENCY MASTERY COACH")
    print(f"🐍 Python {sys.version_info.major}.{sys.version_info.minor}")
    
    use_https = False
    if not os.path.exists("cert.pem") or not os.path.exists("key.pem"):
        print("🔒 Creating self-signed certificate for HTTPS...")
        use_https = create_self_signed_cert()
    else:
        use_https = True
    
    if use_https:
        print("🔒 Starting with HTTPS for microphone access")
        print("🌐 Open https://localhost:5000 in your browser")
        print("⚠️  You'll see a security warning - click 'Advanced' then 'Proceed to localhost'")
        print("=" * 70)
        
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('cert.pem', 'key.pem')
        
        app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=context)
    else:
        print("🌐 Starting with HTTP - microphone may not work on network IPs")
        print("🌐 For microphone access, use: http://localhost:5000")
        print("⚠️  Do NOT use IP addresses - use localhost only")
        print("=" * 70)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
