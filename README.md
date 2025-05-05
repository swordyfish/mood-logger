# mood-logger
Quick and simple mood logger using Streamlit! You can check out the running app at: https://jgochioco-mood-logger.streamlit.app/

🧠 Mood Logger
- Log your mood, add a note if you'd like, and then visualize how your day is going!

🚀 Features
- Emoji-based mood tracking 😊😠😕🎉
- Optional note-taking
- Google Sheets as a backend
- Daily mood bar chart

🛠 How to Run
- Clone this repo
- Create a .venv and install dependencies from requirements.txt 
```
python -m venv .venv  
source .venv/bin/activate  
pip install -r requirements.txt
```
- Add your creds.json file (Google Service Account key) to the root directory.
- Run the app:
```
streamlit run mood_logger.py
```
