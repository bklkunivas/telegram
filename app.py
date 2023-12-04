import asyncio
import requests
from flask import Flask, render_template

from telethon import TelegramClient

app = Flask(__name__)

# Global variable to store sent message IDs
sent_messages = set()

async def read_telegram_messages(api_id, api_hash, phone_number, bot_token, chat_id):
    global sent_messages
    session_name = f"{phone_number}.session"

    async with TelegramClient(session_name, api_id, api_hash) as client:
        # Connect to Telegram
        if not await client.is_user_authorized():
            await client.send_code_request(phone_number)
            await client.sign_in(phone_number, input('Enter the code: '))

        # Read messages
        dialogs = await client.get_dialogs()
        dd = ['-1001735208775', '-1001237603036', '-1001212969072', '-1001285105872', '-1001949522847', '-1001351402590']

        for dialog in dialogs:
            messages = await client.get_messages(dialog.id, limit=10)
            for message in messages:
                if str(dialog.id) in dd and message.id not in sent_messages:
                    sent_messages.add(message.id)
                    if message.reply_to and str(message.text) != "":
                        original_message = await client.get_messages(dialog.id, ids=message.reply_to_msg_id)
                        response = f"{dialog.name}\n""==============================\n"f"{message.text}\n\n\n"f"{dialog.name}'s reply to:\n""----------------------------------------------------------\n"f"{original_message.text}".replace("&", "and")
                        print(response)
                        requests.post(f'https://api.telegram.org/bot6841210725:AAHvasAZbQuPIY9I-JoygPmkcneoJs46ThQ/sendMessage?chat_id=-4084391280&text={response}')

                else:
                    if str(dialog.id) in dd and str(message.text) != "" and message.id not in sent_messages:
                        response = f"{dialog.name}\n""===============================\n"f"{message.text}".replace("Technical & Fundamental", "Technical and Fundamental")
                        print(response)
                        requests.post(f'https://api.telegram.org/bot6841210725:AAHvasAZbQuPIY9I-JoygPmkcneoJs46ThQ/sendMessage?chat_id=-4084391280&text={response}')

def log_message(message):
    with open("log.txt", "a") as log_file:
        log_file.write(message)

@app.route('/refresh_messages')
def refresh_messages():
    # Replace these with your own values
    api_id = '23345565'
    api_hash = '8f56003dce30d58deb7857d14e2bf9ef'
    phone_number = '+91 63829 40859'
    bot_token = '6841210725:AAHvasAZbQuPIY9I-JoygPmkcneoJs46ThQ'
    chat_id = '4084391280'

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(read_telegram_messages(api_id, api_hash, phone_number, bot_token, chat_id))
    finally:
        loop.close()

    return render_template('refresh_messages.html')

if __name__ == "__main__":
    app.run(debug=True, port=8080)