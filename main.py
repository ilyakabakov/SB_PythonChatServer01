from datetime import datetime as dt
from flask import Flask, request, render_template
import json

app = Flask(__name__)  # create new app(__name__ is constant)

DB_FILE = "db.json"


def load_messages():
    with open(DB_FILE, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data["messages"]


all_messages = load_messages()  # список всех сообщений в мессенджере
count = 1


# def messages_count():
#     return count += 1

def save_messages():
    data = {
        "messages": all_messages
    }
    with open(DB_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


@app.route("/")  # main page
def index_page():
    return 'From <b>SKILLBOX</b>'


# all messages list:
# flask сам кодирует в json если функцию возвращает словарь
@app.route("/get_messages")  # all messages page
def get_message():
    return {"messages": all_messages}


# messages output func
def print_message(message):
    print(f"[{message['sender']}]: {message['text']} / {message['time']}")


@app.route("/chat")
def display_chat():
    return render_template("form.html")


# send message получает из запроса имя отправителя и текст
@app.route("/send_message")
def send_message():
    sender = request.args["name"]
    text = request.args["text"]
    add_message(sender, text)
    checker(sender, text)
    save_messages()

    return "OK"


def checker(sender, text):
    checked_d = {
        'sender': sender,
        'text': text,
        'time': dt.now().strftime("%H:%M:%S")
    }
    if len(str(sender)) < 3 or len(str(sender)) > 100:
        checked_d['sender'] = 'ERROR'
        checked_d['text'] = 'Write the valid Name: The name should be at least 3 characters and not more than 100'
    if len(str(text)) < 1 or len(str(text)) > 3000:
        checked_d['text'] = 'ERROR: Your text so much loOoong or short. And will deleted when i finish the code!'
    all_messages.append(checked_d)


# incoming messages func
def add_message(sender, text):
    new_message = {
        'sender': sender,
        'text': text,
        'time': dt.now().strftime("%H:%M:%S")
    }
    all_messages.append(new_message)  # .append - add in dict


app.run()
