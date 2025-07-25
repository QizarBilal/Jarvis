# JARVIS 2025 - Setup Guide

## 🚀 Quick Start

1. **Run JARVIS:**
   ```
   python jarvis_ultimate.py
   ```

2. **Basic Commands:**
   - "hello" - Get a greeting
   - "help" - Show all commands
   - "time" - Current time
   - "date" - Current date
   - "wikipedia [topic]" - Search and hear about any topic
   - "email" - Send an email (requires setup)

## 📧 Email Setup

To enable email functionality:

1. **Set Environment Variables:**
   ```powershell
   # In PowerShell:
   $env:JARVIS_EMAIL = "your-email@gmail.com"
   $env:JARVIS_EMAIL_PASSWORD = "your-app-password"
   ```

2. **Gmail App Password:**
   - Go to Google Account settings
   - Enable 2-Factor Authentication
   - Generate an "App Password" for JARVIS
   - Use the app password (not your regular password)

3. **Test Email:**
   - Say "email" to JARVIS
   - Follow voice prompts for recipient, subject, and message

## 🎤 Voice Features

JARVIS now provides voice responses for:
- ✅ All command confirmations
- ✅ Wikipedia article summaries
- ✅ Email interaction prompts
- ✅ Error messages and help
- ✅ Time and date announcements

## 🎯 Enhanced Features

- **Wikipedia Integration:** Real-time search with voice summaries
- **Interactive Email:** Voice-guided email composition
- **Enhanced Help:** Comprehensive command listing
- **Error Handling:** Clear voice feedback for all issues

## 🛠️ Troubleshooting

- **Voice Issues:** Ensure speakers/headphones are working
- **Email Issues:** Check environment variables and app password
- **Import Errors:** Install requirements: `pip install -r requirements.txt`

---
**JARVIS 2025** - Your Enhanced AI Assistant
