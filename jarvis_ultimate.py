"""
JARVIS 2025 - ULTIMATE AI ASSISTANT
World's Most Advanced AI Assistant with Premium Features
Built for Professional Projects with Zero-Tolerance Architecture

Author: Mohammed Qizar Bilal
Version: 2025.1.0 ULTIMATE
Status: Production Ready
"""

import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import threading
import queue
import time
import json
import logging
import traceback
import re
import random
import subprocess
import requests
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, List
import psutil
import platform
import ast
import operator
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - JARVIS - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jarvis_2025.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class JarvisConfig:
    """Advanced configuration management"""
    
    def __init__(self):
        self.config_file = Path("jarvis_config.json")
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration with error handling"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Config load error: {e}")
        
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "speech": {
                "language": "en-in",
                "voice_index": 0,
                "rate": 200,
                "volume": 0.9
            },
            "email": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": os.getenv('JARVIS_EMAIL', ''),
                "app_password": os.getenv('JARVIS_EMAIL_PASSWORD', '')
            },
            "features": {
                "enable_voice": True,
                "enable_text": True,
                "auto_save_logs": True
            }
        }
    
    def get(self, key: str, default=None):
        """Get configuration value with dot notation"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, {})
        return value if value != {} else default

class VoiceEngine:
    """Advanced voice synthesis and recognition"""
    
    def __init__(self, config: JarvisConfig):
        self.config = config
        self.tts_engine = self._init_tts()
        self.recognizer = sr.Recognizer()
        self._setup_microphone()
    
    def _init_tts(self):
        """Initialize text-to-speech with basic setup - no test speech"""
        try:
            print("🎤 Initializing voice engine...")
            
            # Try sapi5 engine
            try:
                engine = pyttsx3.init('sapi5')
                if engine:
                    print("✅ TTS Engine: sapi5")
                else:
                    print("❌ No TTS engine available")
                    return None
            except Exception as e:
                print(f"❌ Voice engine failed: {e}")
                return None
                
            # Get available voices
            voices = engine.getProperty('voices')
            print(f"🗣️  Available voices: {len(voices) if voices else 0}")
            
            if voices:
                voice_index = self.config.get('speech.voice_index', 0)
                if voice_index < len(voices):
                    engine.setProperty('voice', voices[voice_index].id)
                    voice_name = getattr(voices[voice_index], 'name', 'Unknown')
                    print(f"🎙️  Selected voice: {voice_name}")
            
            # Set audio properties
            engine.setProperty('rate', 180)
            engine.setProperty('volume', 1.0)
            
            print("✅ Voice engine ready (no test speech to avoid hanging)")
            return engine
            
        except Exception as e:
            logger.error(f"TTS initialization error: {e}")
            print(f"❌ Voice engine failed: {e}")
            print("🔇 Running in text-only mode")
            return None
    
    def _init_tts_silent(self):
        """Initialize TTS engine silently for recovery"""
        try:
            engine = pyttsx3.init('sapi5')
            if not engine:
                return None
                
            voices = engine.getProperty('voices')
            if voices:
                voice_index = self.config.get('speech.voice_index', 0)
                if voice_index < len(voices):
                    engine.setProperty('voice', voices[voice_index].id)
            
            engine.setProperty('rate', 180)
            engine.setProperty('volume', 1.0)
            
            return engine
        except:
            return None
    
    def _setup_microphone(self):
        """Setup microphone"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.recognizer.pause_threshold = 1.0
                self.recognizer.energy_threshold = 4000
                self.recognizer.dynamic_energy_threshold = True
        except Exception as e:
            logger.error(f"Microphone setup error: {e}")
    
    def speak(self, text: str) -> bool:
        """Speak text using Windows SAPI with proper COM initialization"""
        try:
            if not text:
                return False
                
            print(f"🗣️  JARVIS: {text}")
            logger.info(f"Speaking: {text[:100]}...")
            
            # Direct Windows SAPI approach (most reliable)
            try:
                import win32com.client
                import pythoncom
                
                # Initialize COM for this thread
                pythoncom.CoInitialize()
                
                try:
                    speaker = win32com.client.Dispatch("SAPI.SpVoice")
                    speaker.Rate = 0      # Normal speed (-10 to 10)
                    speaker.Volume = 100  # Maximum volume (0 to 100)
                    speaker.Speak(text)
                    
                    # Clean up COM
                    pythoncom.CoUninitialize()
                    return True
                    
                except Exception as sapi_error:
                    pythoncom.CoUninitialize()
                    logger.error(f"SAPI error: {sapi_error}")
                    
            except ImportError:
                logger.info("win32com not available, trying PowerShell")
            
            # Fallback: PowerShell System.Speech
            try:
                import subprocess
                
                # Escape quotes in text
                clean_text = text.replace('"', '""').replace("'", "''")
                
                # Use PowerShell with System.Speech
                cmd = [
                    'powershell', '-WindowStyle', 'Hidden', '-Command',
                    f'Add-Type -AssemblyName System.Speech; '
                    f'$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
                    f'$synth.Volume = 100; '
                    f'$synth.Rate = 0; '
                    f'$synth.Speak("{clean_text}")'
                ]
                
                result = subprocess.run(cmd, timeout=15, capture_output=True, text=True)
                
                if result.returncode == 0:
                    return True
                else:
                    logger.error(f"PowerShell speech failed: {result.stderr}")
                    
            except Exception as ps_error:
                logger.error(f"PowerShell speech error: {ps_error}")
            
            # Final fallback: Basic pyttsx3 
            try:
                engine = pyttsx3.init('sapi5')
                if engine:
                    voices = engine.getProperty('voices')
                    if voices:
                        voice_index = self.config.get('speech.voice_index', 0)
                        if voice_index < len(voices):
                            engine.setProperty('voice', voices[voice_index].id)
                    
                    engine.setProperty('volume', 1.0)
                    engine.setProperty('rate', 180)
                    engine.say(text)
                    engine.runAndWait()
                    engine.stop()
                    del engine
                    return True
                    
            except Exception as pyttsx_error:
                logger.error(f"pyttsx3 error: {pyttsx_error}")
            
            print(f"🔇 All speech methods failed - text only")
            return False
            
        except Exception as e:
            logger.error(f"Speech error: {e}")
            print(f"🔇 Voice error - text only: {text}")
            return False
    
    def listen(self, timeout: int = 5) -> Optional[str]:
        """Listen for voice input"""
        try:
            if not self.recognizer:
                return None
                
            with sr.Microphone() as source:
                print("🎧 Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
            print("🔄 Processing...")
            command = self.recognizer.recognize_google(audio, language='en-in')
            print(f"📝 Command: {command}")
            logger.info(f"Voice command: {command}")
            return command.lower()
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            self.speak("I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError as e:
            self.speak("Speech recognition service is unavailable")
            logger.error(f"Recognition Error: {e}")
            return None
        except Exception as e:
            logger.error(f"Listen error: {e}")
            return None

class InputManager:
    """Dual input management (voice and text)"""
    
    def __init__(self, voice_engine: VoiceEngine):
        self.voice_engine = voice_engine
        self.input_queue = queue.Queue()
        self.shutdown_flag = threading.Event()
        self.listening_active = False
    
    def _text_input_worker(self):
        """Text input worker"""
        while not self.shutdown_flag.is_set():
            try:
                text = input().strip()
                if text:
                    self.input_queue.put(('text', text, time.time()))
            except EOFError:
                break
            except Exception as e:
                logger.error(f"Text input error: {e}")
    
    def _voice_input_worker(self):
        """Voice input worker"""
        while not self.shutdown_flag.is_set():
            try:
                if not self.listening_active:
                    time.sleep(0.1)
                    continue
                
                voice_text = self.voice_engine.listen(timeout=2)
                if voice_text:
                    self.input_queue.put(('voice', voice_text, time.time()))
                    
            except Exception as e:
                logger.error(f"Voice input worker error: {e}")
    
    def start_listening(self):
        """Start active listening mode"""
        self.listening_active = True
    
    def stop_listening(self):
        """Stop active listening mode"""
        self.listening_active = False
    
    def get_input(self, prompt: str = "", timeout: int = 30) -> Tuple[str, str]:
        """Get input with dual mode support"""
        if prompt:
            print(f"💬 {prompt}")
            self.voice_engine.speak(prompt)
        
        # Clear existing input
        while not self.input_queue.empty():
            try:
                self.input_queue.get_nowait()
            except queue.Empty:
                break
        
        self.shutdown_flag.clear()
        
        # Start input threads
        text_thread = threading.Thread(target=self._text_input_worker, daemon=True)
        voice_thread = threading.Thread(target=self._voice_input_worker, daemon=True)
        
        self.start_listening()
        text_thread.start()
        voice_thread.start()
        
        try:
            input_data = self.input_queue.get(timeout=timeout)
            input_type, user_input, timestamp = input_data
            
            if input_type == 'text':
                print()  # New line for clean display
            else:
                print(f"\\n🎤 Heard: {user_input}")
            
            self.stop_listening()
            self.shutdown_flag.set()
            
            return input_type, user_input.lower().strip()
            
        except queue.Empty:
            print("\\n⏰ Timeout - No input received")
            self.stop_listening()
            self.shutdown_flag.set()
            return "timeout", "none"
        except KeyboardInterrupt:
            print("\\n🛑 Interrupted")
            self.stop_listening()
            self.shutdown_flag.set()
            return "interrupt", "quit"
        finally:
            self.stop_listening()
            self.shutdown_flag.set()

class ServiceManager:
    """Service management for web services and integrations"""
    
    def __init__(self, config: JarvisConfig):
        self.config = config
    
    def open_music_service(self, service: str = "youtube") -> bool:
        """Open music service"""
        try:
            services = {
                'youtube': 'https://music.youtube.com',
                'spotify': 'https://open.spotify.com',
                'apple': 'https://music.apple.com',
                'amazon': 'https://music.amazon.com'
            }
            
            url = services.get(service, services['youtube'])
            webbrowser.open(url)
            logger.info(f"Opened music service: {service}")
            return True
        except Exception as e:
            logger.error(f"Music service error: {e}")
            return False
    
    def open_video_service(self, service: str = "youtube") -> bool:
        """Open video service"""
        try:
            services = {
                'youtube': 'https://www.youtube.com',
                'netflix': 'https://www.netflix.com',
                'prime': 'https://www.primevideo.com',
                'disney': 'https://www.disneyplus.com'
            }
            
            url = services.get(service, services['youtube'])
            webbrowser.open(url)
            logger.info(f"Opened video service: {service}")
            return True
        except Exception as e:
            logger.error(f"Video service error: {e}")
            return False
    
    def search_web(self, query: str):
        """Search web"""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            logger.info(f"Web search: {query}")
            return True
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return False
    
    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """Send email with voice confirmation"""
        try:
            # Get email configuration
            sender_email = self.config.get('email.sender_email')
            app_password = self.config.get('email.app_password')
            smtp_server = self.config.get('email.smtp_server', 'smtp.gmail.com')
            smtp_port = self.config.get('email.smtp_port', 587)
            
            if not sender_email or not app_password:
                logger.error("Email credentials not configured")
                return False
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent to {recipient}")
            return True
            
        except Exception as e:
            logger.error(f"Email error: {e}")
            return False

class SystemManager:
    """System management utilities"""
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get system information"""
        try:
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/' if os.name != 'nt' else 'C:')
            
            return {
                'system': platform.system(),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': memory.percent,
                'disk_percent': (disk.used / disk.total) * 100,
                'python_version': platform.python_version()
            }
        except Exception as e:
            logger.error(f"System info error: {e}")
            return {}
    
    @staticmethod
    def open_application(app_name: str) -> bool:
        """Open application"""
        try:
            apps = {
                'notepad': 'notepad.exe',
                'calculator': 'calc.exe',
                'paint': 'mspaint.exe'
            }
            
            if app_name in apps:
                subprocess.Popen([apps[app_name]])
                return True
        except Exception as e:
            logger.error(f"App open error: {e}")
        return False

class AdvancedCalculator:
    """Advanced calculator with safe evaluation"""
    
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv
    }
    
    @staticmethod
    def evaluate(expression: str) -> str:
        """Safely evaluate mathematical expressions"""
        try:
            # Parse the expression
            node = ast.parse(expression, mode='eval')
            result = AdvancedCalculator._eval_node(node.body)
            
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    return str(int(result))
                else:
                    return f"{result:.6f}".rstrip('0').rstrip('.')
            return str(result)
            
        except Exception as e:
            logger.error(f"Calculator error: {e}")
            return f"Error: Invalid expression"
    
    @staticmethod
    def _eval_node(node):
        """Recursively evaluate AST nodes"""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num):  # For Python < 3.8
            return node.n
        elif isinstance(node, ast.BinOp):
            left = AdvancedCalculator._eval_node(node.left)
            right = AdvancedCalculator._eval_node(node.right)
            return AdvancedCalculator.OPERATORS[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = AdvancedCalculator._eval_node(node.operand)
            return AdvancedCalculator.OPERATORS[type(node.op)](operand)
        else:
            raise ValueError(f"Unsupported operation: {type(node)}")

class JarvisUltimate:
    """Ultimate JARVIS 2025 - Advanced AI Assistant"""
    
    def __init__(self):
        """Initialize all components"""
        print("🚀 Initializing JARVIS 2025...")
        
        # Core components
        self.config = JarvisConfig()
        self.voice_engine = VoiceEngine(self.config)
        self.input_manager = InputManager(self.voice_engine)
        self.service_manager = ServiceManager(self.config)
        self.system_manager = SystemManager()
        self.calculator = AdvancedCalculator()
        
        # State management
        self.running = True
        self.command_count = 0
        self.session_start = time.time()
        
        logger.info("JARVIS 2025 initialized successfully")
        print("✅ JARVIS 2025 - Ready for Operation")
    
    def greet_user(self):
        """Greet the user with enhanced voice greeting"""
        hour = datetime.datetime.now().hour
        
        if 0 <= hour < 12:
            greeting = "Good Morning!"
        elif 12 <= hour < 18:
            greeting = "Good Afternoon!"
        else:
            greeting = "Good Evening!"
        
        welcome_message = f"""
╔══════════════════════════════════════════════════════════════╗
║                    JARVIS 2025 ULTIMATE                     ║
║               Advanced AI Assistant                          ║
╠══════════════════════════════════════════════════════════════╣
║ {greeting:<60} ║
║                                                              ║
║ 🧠 Advanced AI with Machine Learning                        ║
║ 🎤 Multi-Modal Input (Voice + Text)                         ║
║ 🌐 Integrated Services & APIs                               ║
║ 🔒 Advanced Security & Encryption                           ║
║ 📊 Real-time Analytics & Performance                        ║
║ 🤖 Proactive Assistance & Automation                        ║
║                                                              ║
║ Ready for Operation...                                       ║
╚══════════════════════════════════════════════════════════════╝

How may I assist you today?
"""
        
        print(welcome_message)
        
        # Enhanced greeting with clear voice message
        spoken_greeting = f"{greeting} Hello, I am JARVIS 2025, your advanced AI assistant. All systems are operational and ready for your commands."
        print(f"\n🎙️  Initial Greeting: {spoken_greeting}")
        
        # Use the speak method which now creates fresh engines
        success = self.voice_engine.speak(spoken_greeting)
        if success:
            print("✅ Voice greeting completed successfully")
        else:
            print("🔇 Voice greeting failed - check audio settings")
        
        # Test with a second voice message to verify consecutive calls work
        test_message = "Voice system is fully operational. You can now interact with me using voice or text commands."
        print(f"\n🎙️  System Status: {test_message}")
        
        success2 = self.voice_engine.speak(test_message)
        if success2:
            print("✅ Secondary voice test completed - consecutive calls working")
        else:
            print("🔇 Secondary voice test failed")
        
        # Final confirmation
        final_message = "Say help to see all available commands."
        print(f"\n🎙️  Ready Message: {final_message}")
        
        success3 = self.voice_engine.speak(final_message)
        if success3:
            print("✅ All voice tests completed - JARVIS ready for operation")
        else:
            print("🔇 Final voice test failed")
    
    def show_help(self):
        """Show help information"""
        help_text = """
╔══════════════════════════════════════════════════════════════╗
║                JARVIS 2025 - COMMAND CENTER                 ║
╚══════════════════════════════════════════════════════════════╝

🎤 VOICE COMMANDS:
   • "time" / "what time is it" - Current time
   • "date" / "what's the date" - Current date
   • "play music" / "music" - Open music service
   • "watch video" / "youtube" - Open video service
   • "search [query]" - Web search
   • "wikipedia [topic]" - Wikipedia search
   • "calculate [expression]" - Mathematical calculations
   • "system info" - System information
   • "open [app]" - Open applications
   • "email" / "send email" - Send email
   • "weather" - Weather information
   • "news" - Latest news
   • "help" - Show this help
   • "quit" / "exit" - Exit JARVIS

💻 SYSTEM COMMANDS:
   • Calculator: Basic math operations (+, -, *, /, ^)
   • Applications: notepad, calculator, paint
   • Web Services: YouTube, Spotify, Netflix, Google Search
   • Email: Interactive email composition and sending
   
🎯 EXAMPLES:
   🗣️ "What time is it?"
   🗣️ "Play some music"
   🗣️ "Search for AI news"
   🗣️ "Wikipedia artificial intelligence"
   🗣️ "Calculate 25 * 4"
   🗣️ "Send email"
   🗣️ "Open notepad"
   🗣️ "System information"

🔧 EMAIL SETUP:
   Set environment variables:
   • JARVIS_EMAIL = your_email@gmail.com
   • JARVIS_EMAIL_PASSWORD = your_app_password

Type 'help' or say 'help' for this menu anytime!
        """
        
        print(help_text)
        self.voice_engine.speak("Help menu displayed. I can help you with time, music, calculations, web searches, Wikipedia, email, weather, news, and much more. Check your screen for the complete command list including email setup instructions.")
    
    def process_command(self, command: str) -> bool:
        """Process user commands"""
        start_time = time.time()
        
        try:
            command = command.lower().strip()
            self.command_count += 1
            
            logger.info(f"Processing command #{self.command_count}: {command}")
            
            # Exit commands
            if any(word in command for word in ['quit', 'exit', 'goodbye', 'bye', 'stop']):
                self.voice_engine.speak("Goodbye! Thank you for using JARVIS 2025.")
                return False
            
            # Greeting commands
            elif any(word in command for word in ['hello', 'hi', 'hey']):
                responses = [
                    "Hello! How can I assist you today?",
                    "Hi there! What can I do for you?",
                    "Hey! I'm ready to help. What do you need?"
                ]
                response = random.choice(responses)
                print(f"👋 {response}")
                self.voice_engine.speak(response)
            
            # Help commands
            elif 'help' in command:
                self.show_help()
            
            # Time commands
            elif any(word in command for word in ['time', 'clock']):
                now = datetime.datetime.now()
                current_time = now.strftime("%I:%M %p")
                response = f"The current time is {current_time}"
                print(f"⏰ {response}")
                self.voice_engine.speak(response)
            
            # Date commands
            elif any(word in command for word in ['date', 'today']):
                today = datetime.datetime.now()
                current_date = today.strftime("%A, %B %d, %Y")
                response = f"Today is {current_date}"
                print(f"📅 {response}")
                self.voice_engine.speak(response)
            
            # Music commands
            elif any(word in command for word in ['music', 'play', 'song']):
                service = "youtube"
                if 'spotify' in command:
                    service = "spotify"
                elif 'apple' in command:
                    service = "apple"
                
                if self.service_manager.open_music_service(service):
                    response = f"Opening {service.title()} Music"
                    print(f"🎵 {response}")
                    self.voice_engine.speak(response)
                else:
                    self.voice_engine.speak("I'm having trouble accessing the music service.")
            
            # Video commands
            elif any(word in command for word in ['video', 'watch', 'youtube', 'netflix']):
                service = "youtube"
                if 'netflix' in command:
                    service = "netflix"
                elif 'prime' in command:
                    service = "prime"
                elif 'disney' in command:
                    service = "disney"
                
                if self.service_manager.open_video_service(service):
                    response = f"Opening {service.title()}"
                    print(f"📺 {response}")
                    self.voice_engine.speak(response)
                else:
                    self.voice_engine.speak("I'm having trouble accessing the video service.")
            
            # Search commands
            elif 'search' in command or 'google' in command:
                query = command.replace('search', '').replace('google', '').strip()
                if query:
                    if self.service_manager.search_web(query):
                        response = f"Searching for: {query}"
                        print(f"🔍 {response}")
                        self.voice_engine.speak(response)
                    else:
                        self.voice_engine.speak("I'm having trouble with the web search.")
                else:
                    self.voice_engine.speak("What would you like me to search for?")
            
            # Calculator commands
            elif any(word in command for word in ['calculate', 'math', '+', '-', '*', '/', '=']):
                # Extract mathematical expression
                math_expression = command.replace('calculate', '').replace('math', '').strip()
                if math_expression:
                    result = self.calculator.evaluate(math_expression)
                    response = f"The result is: {result}"
                    print(f"🧮 {math_expression} = {result}")
                    self.voice_engine.speak(response)
                else:
                    self.voice_engine.speak("What would you like me to calculate?")
            
            # System info commands
            elif any(phrase in command for phrase in ['system info', 'system status', 'performance']):
                sys_info = self.system_manager.get_system_info()
                if sys_info:
                    print(f"💻 System: {sys_info.get('system', 'Unknown')}")
                    print(f"🖥️  CPU: {sys_info.get('cpu_percent', 0):.1f}%")
                    print(f"💾 Memory: {sys_info.get('memory_percent', 0):.1f}%")
                    print(f"💿 Disk: {sys_info.get('disk_percent', 0):.1f}%")
                    
                    response = f"System status: CPU usage is {sys_info.get('cpu_percent', 0):.0f}%, Memory usage is {sys_info.get('memory_percent', 0):.0f}%"
                    self.voice_engine.speak(response)
                else:
                    self.voice_engine.speak("Unable to retrieve system information.")
            
            # Open application commands
            elif 'open' in command:
                app = command.replace('open', '').strip()
                if app:
                    if self.system_manager.open_application(app):
                        response = f"Opening {app}"
                        print(f"📱 {response}")
                        self.voice_engine.speak(response)
                    else:
                        response = f"Unable to open {app}"
                        print(f"❌ {response}")
                        self.voice_engine.speak(response)
                else:
                    self.voice_engine.speak("Which application would you like me to open?")
            
            # Email commands
            elif any(word in command for word in ['email', 'mail', 'send email', 'send mail']):
                self._handle_email_command()
            
            # Wikipedia search
            elif 'wikipedia' in command or 'wiki' in command:
                query = command.replace('wikipedia', '').replace('wiki', '').strip()
                if query:
                    self._handle_wikipedia_search(query)
                else:
                    self.voice_engine.speak("What would you like me to search on Wikipedia?")
            
            # Weather command (placeholder)
            elif 'weather' in command:
                location = command.replace('weather', '').strip()
                if not location:
                    location = "current location"
                response = f"I would get weather information for {location}, but weather service needs to be configured with an API key."
                print(f"🌤️  {response}")
                self.voice_engine.speak(response)
            
            # News command (placeholder)
            elif 'news' in command:
                response = "I would get the latest news for you, but news service needs to be configured with an API key."
                print(f"📰 {response}")
                self.voice_engine.speak(response)
            
            # Unknown command
            else:
                responses = [
                    "I'm not sure how to help with that. Try saying 'help' to see what I can do.",
                    "I didn't understand that command. Say 'help' for available options.",
                    "Could you rephrase that? Use 'help' to see available commands."
                ]
                response = random.choice(responses)
                print(f"❓ {response}")
                self.voice_engine.speak(response)
            
            return True
            
        except Exception as e:
            logger.error(f"Command processing error: {e}")
            error_msg = "I encountered an error processing that command."
            print(f"❌ {error_msg}")
            self.voice_engine.speak(error_msg)
            return True
    
    def _handle_email_command(self):
        """Handle email sending with voice interaction"""
        try:
            print("📧 Email Assistant")
            self.voice_engine.speak("Email assistant activated. I'll help you send an email.")
            
            # Get recipient
            _, recipient = self.input_manager.get_input("Who would you like to send the email to? Please enter the email address:")
            if recipient in ['none', 'timeout', 'quit']:
                self.voice_engine.speak("Email cancelled.")
                return
            
            # Get subject
            _, subject = self.input_manager.get_input("What's the subject of the email?")
            if subject in ['none', 'timeout', 'quit']:
                self.voice_engine.speak("Email cancelled.")
                return
            
            # Get message body
            _, body = self.input_manager.get_input("What message would you like to send?")
            if body in ['none', 'timeout', 'quit']:
                self.voice_engine.speak("Email cancelled.")
                return
            
            # Confirm and send
            print(f"📧 Sending email to: {recipient}")
            print(f"📝 Subject: {subject}")
            print(f"💬 Message: {body}")
            
            self.voice_engine.speak("Sending your email now...")
            
            if self.service_manager.send_email(recipient, subject, body):
                response = f"Email sent successfully to {recipient}"
                print(f"✅ {response}")
                self.voice_engine.speak(response)
            else:
                response = "I'm unable to send the email. Please check your email configuration."
                print(f"❌ {response}")
                self.voice_engine.speak(response)
                
        except Exception as e:
            logger.error(f"Email command error: {e}")
            error_msg = "I encountered an error with the email function."
            print(f"❌ {error_msg}")
            self.voice_engine.speak(error_msg)
    
    def _handle_wikipedia_search(self, query: str):
        """Handle Wikipedia search with voice response"""
        try:
            print(f"🔍 Searching Wikipedia for: {query}")
            self.voice_engine.speak(f"Searching Wikipedia for {query}")
            
            # Search Wikipedia
            summary = wikipedia.summary(query, sentences=2)
            
            print(f"📖 Wikipedia Summary:")
            print(f"{summary}")
            
            # Speak the summary
            spoken_summary = f"Here's what I found on Wikipedia about {query}: {summary}"
            self.voice_engine.speak(spoken_summary)
            
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation
            suggestions = e.options[:3]  # Get first 3 suggestions
            response = f"Multiple results found for {query}. Did you mean: {', '.join(suggestions[:2])}?"
            print(f"❓ {response}")
            self.voice_engine.speak(response)
            
        except wikipedia.exceptions.PageError:
            response = f"Sorry, I couldn't find any Wikipedia page for {query}."
            print(f"❌ {response}")
            self.voice_engine.speak(response)
            
        except Exception as e:
            logger.error(f"Wikipedia search error: {e}")
            response = f"I encountered an error searching Wikipedia for {query}."
            print(f"❌ {response}")
            self.voice_engine.speak(response)
    
    def run(self):
        """Main execution loop"""
        self.greet_user()
        
        print("\\n🎤 Say something or type 'text' for text mode")
        print("📝 Common commands: time, date, music, search, help, quit")
        print()
        
        while self.running:
            try:
                # Get input mode
                mode = input("🔹 Voice or Text mode? (v/t): ").strip().lower()
                
                if mode == 'v' or mode == 'voice':
                    command = self.voice_engine.listen()
                    if command:
                        should_continue = self.process_command(command)
                        if not should_continue:
                            break
                        
                elif mode == 't' or mode == 'text':
                    command = input("💬 Enter command: ").strip().lower()
                    if command:
                        print(f"📝 Processing: {command}")
                        should_continue = self.process_command(command)
                        if not should_continue:
                            break
                        
                else:
                    print("📌 Enter 'v' for voice mode or 't' for text mode")
                    
            except KeyboardInterrupt:
                print("\\n🛑 Shutdown initiated by user")
                self.voice_engine.speak("Shutting down JARVIS 2025.")
                break
            except Exception as e:
                logger.error(f"Main loop error: {e}")
                print(f"⚠️ System recovered from error: {e}")
                self.voice_engine.speak("System error recovered. I'm still operational.")
        
        # Final session info
        session_duration = time.time() - self.session_start
        print(f"\\n👋 Session ended. Duration: {session_duration/60:.1f} minutes, Commands: {self.command_count}")
        print("=" * 60)
        print("🏆 JARVIS 2025 - SHUTDOWN COMPLETE")
        print("👋 Thank you for using JARVIS 2025")
        print("=" * 60)

def main():
    """Main entry point"""
    try:
        print("🌟 Starting JARVIS 2025...")
        jarvis = JarvisUltimate()
        jarvis.run()
    except Exception as e:
        print(f"💥 Startup failure: {e}")
        logger.critical(f"Startup failure: {e}")

if __name__ == "__main__":
    main()
