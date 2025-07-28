#!/usr/bin/env python3
"""
English Fluency Coach - Quick Start Script
"""

import os
import sys

def main():
    print("🎤 English Fluency Mastery Coach")
    print("=" * 50)
    
    # Check if API keys are configured
    api_config_path = "utils/api_keys_config.py"
    if not os.path.exists(api_config_path):
        print("⚠️  API keys not configured!")
        print(f"📝 Please create {api_config_path} with your API keys:")
        print()
        print("GROQ_API_KEY = 'your_groq_api_key_here'")
        print("ASSEMBLYAI_API_KEY = 'your_assemblyai_api_key_here'")
        print()
        print("Get your keys from:")
        print("- Groq: https://console.groq.com/keys")
        print("- AssemblyAI: https://www.assemblyai.com/dashboard/")
        print()
        
        # Create template file
        with open(api_config_path, 'w') as f:
            f.write('# Add your API keys here\n')
            f.write('GROQ_API_KEY = "your_groq_api_key_here"\n')
            f.write('ASSEMBLYAI_API_KEY = "your_assemblyai_api_key_here"\n')
        
        print(f"✅ Template created at {api_config_path}")
        print("📝 Edit this file with your actual API keys, then run again.")
        return
    
    # Import and run the app
    try:
        from app import app
        print("✅ Starting English Fluency Coach...")
        print("🌐 Open https://localhost:5000 in your browser")
        print("⚠️  Accept the security warning for the self-signed certificate")
        print("🎤 Allow microphone access when prompted")
        print("=" * 50)
        
        # Run the app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("📦 Install with: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main()
