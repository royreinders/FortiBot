import json
import requests
import time
import sys

# Fixes reading of special characters
reload(sys)
sys.setdefaultencoding('utf8')

TOKEN = "<API TOKEN>"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
trigger_users = ["John", "Mary", "Bob"]
trigger_words = ["Forti"]
enable_trigger_words = True


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    #print url
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def get_message_info(updates):
    text = "FortiSticker"
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    message_id = updates["result"][last_update]["message"]["message_id"]
    if "sticker" not in updates["result"][last_update]["message"]:
        text = updates["result"][last_update]["message"]["text"]
    if "photo" not in updates["result"][last_update]["message"]:
        text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    user_first_name = updates["result"][last_update]["message"]["from"]["first_name"]
    return chat_id, user_first_name, text, message_id


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def filter_user(username):
    if username in trigger_users:
        return True
    else:
        return False


def filter_message(message):
    found_match = False
    for word in trigger_words:
         if word.lower() in message.lower():
             found_match = True
    return found_match

def generate_and_send_message(original_message, chat_id):
    new_message = "FortiFact: " + random.choice(list(open('FortiFacts.txt')))
    #print new_message

    send_message(new_message, chat_id)


def reply_all_filters():
    last_message_id = 0
    while True:
        chat_id, first_name, message, message_id = get_message_info(get_updates())
        if filter_user(first_name) & filter_message(message) & (message_id != last_message_id):
            last_message_id = message_id
            generate_and_send_message(message, chat_id)
        time.sleep(0.5)


def reply_user_filter():
    last_message_id = 0
    while True:
        chat_id, first_name, message, message_id = get_message_info(get_updates())
        if filter_user(first_name) & (message_id != last_message_id):
            last_message_id = message_id
            generate_and_send_message(message, chat_id)
        time.sleep(0.5)


def listen():
    if(enable_trigger_words):
        reply_all_filters()
    else:
        reply_user_filter()

listen()
