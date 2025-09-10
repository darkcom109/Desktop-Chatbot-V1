import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Text-to-speech
import pyttsx3

# Imports the system functions to properly start/stop app
import sys

# Imports the time module
import time

# Imports threading to ensure that text-to-speech disabled runs in their own background
import threading

# Imports core GUI widgets
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QLineEdit, QPushButton, QToolButton, QMenu, QAction
from PyQt5.QtCore import QTimer, Qt

# Imports for loading screen
from PyQt5.QtWidgets import QSplashScreen, QLabel
from PyQt5.QtGui import QPixmap, QFont

# Loading screen
from splash import show_loading_screen, show_title_screen

# Speech to text
import speech_recognition as sr

# Load env
load_dotenv()

# OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatbotApp(QWidget):
    def __init__(self):
        super().__init__() # Call QWidget constructor

        # Main window

        self.setWindowTitle("Advanced Linear Ethical Hacking Algorithm")
        self.setFixedSize(500, 600)

        # Initialise text-to-speech

        self.tts_engine = pyttsx3.init() # Initialise text-to-speech
        self.tts_engine.setProperty('rate', 250) # Change speed

        # Large chat display box

        self.chat_display = QTextEdit(self) # text box
        self.chat_display.setGeometry(10, 10, 480, 400)
        self.chat_display.setReadOnly(True)

        # Input field for user

        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(10, 420, 480, 30)
        self.input_field.setPlaceholderText(f"Type here...")
        self.input_field.returnPressed.connect(self.send_message)

        # Clear button to wipe chat display box

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.setGeometry(10, 460, 80, 30)
        self.clear_button.clicked.connect(self.clear_chat)

        # Send button to send data from input field

        self.send_button = QPushButton("Send", self)
        self.send_button.setGeometry(110, 460, 80, 30)
        self.send_button.clicked.connect(self.send_message)

        # Reset memory from scratch

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setGeometry(210, 460, 80, 30)
        self.reset_button.clicked.connect(self.reset_memory)

        # Speech Menu

        self.speech_toggle = QToolButton(self)
        self.speech_toggle.setGeometry(310, 460, 80, 30)
        self.speech_toggle.setText("Speech")
        self.speech_toggle.setPopupMode(QToolButton.InstantPopup)

        speech_menu = QMenu(self)

        enable_action = QAction("Enable", self)
        enable_action.triggered.connect(self.enable_speech)
        speech_menu.addAction(enable_action)

        disable_action = QAction("Disable", self)
        disable_action.triggered.connect(self.disable_speech)
        speech_menu.addAction(disable_action)

        self.speech_toggle.setMenu(speech_menu)

        # Light/dark-mode menu

        self.theme_toggle = QToolButton(self)
        self.theme_toggle.setGeometry(410, 460, 80, 30)
        self.theme_toggle.setText("Theme")
        self.theme_toggle.setPopupMode(QToolButton.InstantPopup)

        theme_menu = QMenu(self)
        light_action = QAction("Light", self)
        dark_action = QAction("Dark", self)

        light_action.triggered.connect(lambda: self.set_theme("C:/Users/garci/Downloads/Websites/Software Engineering/desktop-chatbot/app/styles/light.qss"))
        dark_action.triggered.connect(lambda: self.set_theme("C:/Users/garci/Downloads/Websites/Software Engineering/desktop-chatbot/app/styles/dark.qss"))

        theme_menu.addAction(light_action)
        theme_menu.addAction(dark_action)

        self.theme_toggle.setMenu(theme_menu)

        # Speech recognition

        self.mic_button = QPushButton("Speak", self)
        self.mic_button.setGeometry(10, 500, 480, 30)
        self.mic_button.clicked.connect(self.listen_to_speech)

        # Custom Personalities

        self.personality_toggle = QToolButton(self)
        self.personality_toggle.setGeometry(10, 540, 140, 30)
        self.personality_toggle.setText("Personality")
        self.personality_toggle.setPopupMode(QToolButton.InstantPopup)

        personality_menu = QMenu(self)
        default = QAction("Default", self)
        sarcastic = QAction("Sarcastic", self)

        default.triggered.connect(self.default_personality)
        sarcastic.triggered.connect(self.sarcastic_personality)

        personality_menu.addAction(default)
        personality_menu.addAction(sarcastic)

        self.personality_toggle.setMenu(personality_menu)

        self.chat_history = None
        self.default_personality()

        # Custom modes

        self.mode_toggle = QToolButton(self)
        self.mode_toggle.setGeometry(180, 540, 140, 30)
        self.mode_toggle.setText("Mode")
        self.mode_toggle.setPopupMode(QToolButton.InstantPopup)

        mode_menu = QMenu(self)
        summarise = QAction("Summarise", self)
        email = QAction("Email", self)
        check_link = QAction("Check Link", self)

        summarise.triggered.connect(self.summarise_mode)
        email.triggered.connect(self.email_mode)
        check_link.triggered.connect(self.check_link_mode)

        mode_menu.addAction(summarise)
        mode_menu.addAction(email)
        mode_menu.addAction(check_link)

        self.mode_toggle.setMenu(mode_menu)

        # Dashboard

        self.dashboard_button = QPushButton("Dashboard", self)
        self.dashboard_button.setGeometry(350, 540, 140, 30)
        self.dashboard_button.clicked.connect(self.display_dashboard)

        self.active_mode = None
        self.speech_enabled = False
        self.personality = "Default"

        with open("C:/Users/garci/Downloads/Custom Tkinter/app/assets/styles/dark.qss", "r") as f:
            self.setStyleSheet(f.read())

    # Receives message from input field and process it
    def send_message(self):
        user_text = self.input_field.text().strip()

        if not user_text:
            return
        
        self.chat_display.append(f"You: {user_text}")

        if self.active_mode == "Link Verification" and user_text.lower().startswith(":"):
            url = user_text[1:].strip()
            self.chat_display.append(f"Scanning link: {url}\n")
            result = self.scan_link(url)
            self.chat_display.append(result)
            self.input_field.clear()
            return

        if "speech on" in user_text:
            self.enable_speech()
            self.input_field.clear()
            return
        elif "speech off" in user_text:
            self.disable_speech()
            self.input_field.clear()
            return

        bot_response = self.get_bot_response(user_text)
        self.add_to_display(bot_response)
        self.input_field.clear()
        self.disable_features()
        self.speak_text(bot_response)
        self.enable_features()

    # Create response from AI
    def get_bot_response(self, user_input):
        
        self.chat_history.append({"role":"user", "content":user_input})
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.chat_history
        )

        bot_response = response.choices[0].message.content
        self.chat_history.append({"role":"assistant", "content": bot_response})
        return bot_response
    
    # Clear chat display box + input field
    def clear_chat(self):
        self.chat_display.clear()
        self.input_field.clear()

    # Reset AI memory
    def reset_memory(self):
        self.chat_history = [{"role": "system", "content": "You are a very informative chatbot"}]
        self.clear_chat()
        self.speech_enabled = False

    # Disable all features
    def disable_features(self):
        self.input_field.setEnabled(False)
        self.send_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.mic_button.setEnabled(False)

    # Enable all features
    def enable_features(self):
        self.input_field.setEnabled(True)
        self.send_button.setEnabled(True)
        self.reset_button.setEnabled(True)
        self.clear_button.setEnabled(True)
        self.mic_button.setEnabled(True)

    # Text-to-speech response
    def speak_text(self, bot_response):
        if self.speech_enabled:
            def run():
                self.tts_engine.say(bot_response)
                self.tts_engine.runAndWait()
                self.enable_features()

            threading.Thread(target=run, daemon=True).start()

    # Enable text-to-speech
    def enable_speech(self):
        def run():
            self.speech_enabled = True
            self.tts_engine.say("Speech Enabled")
            self.tts_engine.runAndWait()

        threading.Thread(target=run, daemon=True).start()

    # Disable text-to-speech
    def disable_speech(self):
        def run():
            self.speech_enabled = False
            self.tts_engine.say("Speech Disabled")
            self.tts_engine.runAndWait()

        threading.Thread(target=run, daemon=True).start()

    # Letter by letter animation
    def add_to_display(self, bot_response):
        self.chat_display.append("Bot: ")
        self.response_index = 0
        self.typed_text = ""

        def update_letter():
            self.disable_features()
            if self.response_index < len(bot_response):
                self.typed_text += bot_response[self.response_index]
                self.response_index += 1
                self.chat_display.moveCursor(self.chat_display.textCursor().End)
                self.chat_display.insertPlainText(bot_response[self.response_index - 1])
            else:
                self.enable_features()
                self.chat_display.moveCursor(self.chat_display.textCursor().End)
                self.chat_display.insertPlainText("\n")                
                self.typing_timer.stop()

        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(update_letter)
        self.typing_timer.start(30)

    # Light/dark mode
    def set_theme(self, file_name):
        with open(file_name, "r") as f:
            self.setStyleSheet(f.read())

    # Speech-to-text
    def listen_to_speech(self):
        self.clear_chat()
        self.chat_display.insertHtml("<p align='center'>Listening to Voice Command</p>")
        QApplication.processEvents()
        recogniser = sr.Recognizer()
        with sr.Microphone() as source:
            self.disable_features()
            try:
                recogniser.adjust_for_ambient_noise(source, duration=1)
                audio = recogniser.listen(source, timeout=5, phrase_time_limit=10)
                text = recogniser.recognize_google(audio)
                self.input_field.setText(text)
                self.send_message()
            except sr.WaitTimeoutError:
                self.chat_display.append("Listening timed out")
            except sr.UnknownValueError:
                self.chat_display.append("Sorry I didn't catch that")
            finally:
                self.enable_features()

    # Default personality
    def default_personality(self):
        self.clear_chat()
        self.personality = "Default"
        self.active_mode = None
        self.chat_display.insertHtml("<p align='center'>Your Personal Chatbot, Customise and Interact</p>")
        self.chat_history = [{"role": "system", "content": "You are a very informative chatbot"}]

    # Sarcastic personality
    def sarcastic_personality(self):
        self.clear_chat()
        self.personality = "Sarcastic"
        self.active_mode = None
        self.chat_display.insertHtml("<p align='center'>The Sarcastic Personality, Great for Those who want a Ruthless Chatbot</p>")
        self.chat_history = [{"role": "system", "content": "You are a very sarcastic chatbot"}]

    # Summarise mode
    def summarise_mode(self):
        self.clear_chat()
        self.active_mode = "Summarise"
        self.personality = None
        self.chat_display.insertHtml("<p align='center'>Summarise a piece of information in one sentence</p>")
        self.chat_history = [{"role": "system", "content":"You are a summariser chatbot, you are mostly used for summarising sentences in one sentence, specifically information"}]

    # Email drafting mode
    def email_mode(self):
        self.clear_chat()
        self.active_mode = "Email"
        self.personality = None
        self.chat_display.insertHtml("<p align='center'>Summarise, create or verify an email</p>")
        self.chat_history = [{"role": "system", "content":"Users will either send you an email, in which you need to summarise what the email is saying "
                                                          "or the user will ask you to draft them an email, in which you have to design them an email "
                                                          "according to the information they provide. Lastly, you can also be used to check if the email"
                                                          "might be a phishing scam if you believe it might be"}]

    # Check link mode
    def check_link_mode(self):
        self.clear_chat()
        self.personality = None
        self.active_mode = "Link Verification"
        self.chat_display.insertHtml("<p align='center'>Verify any link, format - ':https://website.com' or : before the website URL</p>")

    # Scan links
    def scan_link(self, url):
        api_key = os.getenv("VT_API_KEY")
        headers = {"x-apikey": api_key}
        scan_response = requests.post("https://www.virustotal.com/api/v3/urls",headers=headers, data={"url": url})
        if scan_response.status_code != 200:
            return f"Failed to scan URL: {scan_response.text}"
        
        scan_id = scan_response.json()["data"]["id"]

        report_url = f"https://www.virustotal.com/api/v3/analyses/{scan_id}"
        report_response = requests.get(report_url, headers=headers)

        if report_response.status_code != 200:
            return f"Failed to fetch report: {report_response.text}"
        
        data = report_response.json()["data"]["attributes"]
        stats = data["stats"]
        total = stats["malicious"] + stats["suspicious"] + stats["harmless"] + stats["undetected"]
        return f"""Link Report:
        1) Malicious: {stats['malicious']}
        2) Suspicious: {stats['suspicious']}
        3) Harmless: {stats['harmless']}
        4) Undetected: {stats['undetected']}
        5) Total Vendors: {total}
        """
    
    # Display dashboard
    def display_dashboard(self):
        self.clear_chat()
        mode = self.active_mode
        speech = self.speech_enabled
        personality = self.personality
        self.chat_display.insertHtml("<p align='center'>DASHBOARD</p>")
        self.chat_display.append(f"Mode: {mode}")
        self.chat_display.append(f"Speech Enabled: {speech}")
        self.chat_display.append(f"Personality: {personality}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loading_screen = show_loading_screen(app)
    title_screen = show_title_screen(app)

    window = ChatbotApp()
    window.show()
    loading_screen.finish(title_screen)
    title_screen.finish(window)
    sys.exit(app.exec_())

    