# Desktop-Chatbot-V1

## Features  

- 👤 **Artificial Intelligence**  
  - Interact with the OpenAI API using text
  - Sarcastic personality available (similar to MondayGPT)

- 📚 **Alternative Modes**  
  - Email mode, users can verify if an email is not trustworthy
  - Summarise mode, users can have long scripts of text be summarised in one sentence 
  - Link mode, users can have a website URL verified using the VirusTotal API
  - Text-to-speech mode, users can have their text read to them using the pytts library
  - Speech-to-text mode, users can talk to their microphone and have the chatbot listen to their response

- ⚡ **Dashboard**  
  - Users can view their dashboard to check what modes and personality the AI is set to

- 🌇 **Light/Dark Modes**  
  - Users can choose between light and dark mode (default due to retro-gui style)
 
- 🔑 **Splash Screen + Memory**  
  - An animated splash screen that simulates a hacking tool
  - AI can keep track of the user's messages unless they reset the chatbot's memory

## Tech Stack  

- **Interface** PyQt-5 QSS
- **API** OpenAI API, VirusTotal API

## Getting Started  

### Prerequisites  
You will need to create a .env containing your OpenAI (uses credits) and VirusTotal (free up to a limit) API keys

### Installation  

```bash
# Clone the repository
git clone https://github.com/darkcom109/Desktop-Chatbot-V1.git
cd Desktop-Chatbot-V1

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install requirements.txt
pip install -r requirements.txt
