from flask import Flask, request, render_template
import os
from dotenv import load_dotenv
import anthropic
import json
import datetime


load_dotenv()

api_key=os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(
    api_key=api_key,
    timeout = 15.0
)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=['POST'])
def add():
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        with open('reminders.json', 'r') as file:
            data = json.load(file)
            print(f"File Data=", data)

    except FileNotFoundError as e:
        print("Error:", e)

    except json.JSONDecodeError as e:
        print("Error:", e)
    
    new_reminder = request.get_json(force=True)["response"]
    with open('reminders.json', 'w') as file:
        data.append({"REMINDER": new_reminder, "DATE": timestamp_str})
        json.dump(data, file)
    return json.dumps(data)
        
    
@app.route("/read_reminders", methods=["GET"])
def read_reminders():
    with open('reminders.json', 'r') as file:
        data = json.load(file)
        prompt = f"When given: {data} Act like Jarvis in Iron-Man in the Marvels, my name's AUDRAN. Only give your answer when it's finished and polished, do not give any of your reasonning, punctuation or thoughts. Only finished answer. Keep it tight no more than 3 sentences. Your task is STEP 1: Read my reminders while the page is loading. STEP 2: Give personalized greeting, make sure everything is clean. STEP 3: Acknowledge with the user what to focus on. STEP 4: Acknowledge what's coming up. Last but not least STEP 5: Encourage the user to do what he has to do."
    return json.dumps(data)

@app.route("/delete", methods=["POST"])
def delete():
    with open('reminders.json', 'r') as file:
        data = json.load(file)
        reminder_index = request.get_json(force=True)["index"]
        print(request.get_json(force=True))
        data.pop(int(reminder_index))

        
    with open('reminders.json', 'w') as file:
        json.dump(data, file)
    return data