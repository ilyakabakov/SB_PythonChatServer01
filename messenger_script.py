from datetime import datetime as dt
from flask import Flask, request, render_template, escape, abort
from typing import Tuple
import json

app = Flask(__name__)  # create new app(__name__ is constant)

DB_FILE = "db.json"


def load_messages() -> list:
    with open(DB_FILE, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data["messages"]


all_messages = load_messages()  # список всех сообщений в мессенджере


@app.route("/message_count")
def messages_count() -> str:
    return f"Messages in chat: {str(len(all_messages))}"


def save_messages() -> None:
    data = {
        "messages": all_messages
    }
    with open(DB_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


@app.route("/")  # main page
def index_page() -> str:
    return "From <b>SKILLBOX</b>!"


# all messages list:
@app.route("/get_messages")  # all messages page
def get_message() -> dict:
    return {"messages": all_messages}


# messages output func
# def print_message(message):
#     print(f"[{message['sender']}]: {message['text']} / {message['time']}")


@app.route("/chat")
def display_chat():
    return render_template("form.html")


def length_check(name_key: str, text_value: str, min_val: int, max_val: int) -> None:
    if not text_value:
        raise ValueError(f"Not valid  {name_key}. Name can can contain from 3 to 100 characters!")
    else:
        current_len = len(text_value)
        if max_val < current_len or current_len < min_val:
            raise ValueError(
                f"ERROR in {name_key} pole."
                f"{name_key} can can contain from {min_val} to {max_val} characters! "
                f"The current length = {current_len}."
            )


def checker(request_data: dict) -> Tuple[str, str]:
    sender = escape(request_data.get('name'))
    length_check('name', sender, 3, 100)

    text = escape(request_data['text'])
    length_check('text', text, 1, 3000)

    return sender, text


# send message получает из запроса имя отправителя и текст
@app.route("/send_message")
def send_message() -> str:
    try:
        sender, text = checker(request.args)
    except ValueError:
        abort(400)
    add_message(sender, text)
    save_messages()
    return "OK"


# incoming messages func
def add_message(sender: str, text: str) -> None:
    new_message = {
        'sender': sender,
        'text': text,
        'time': dt.now().time().isoformat(timespec='seconds')
    }
    all_messages.append(new_message)  # .append - add in dict


# Для каждого сообщения в списке all_messages
# for message in all_messages:
#     print_message(message)

app.run()
