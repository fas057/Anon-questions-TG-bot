import requests

TOKEN = '' # Token
ADMIN_CHAT_ID = '' #UserID

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    params = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=params)
    return response.json()

def handle_command(update):
    chat_id = update['message']['chat']['id']
    command = update.get('message', {}).get('text', '').lower()

    if command == '/start':
        send_message(chat_id, "") # Указываем приветственное сообщение при выполнении команды start
    else:
        send_message(chat_id, "")

def handle_message(update):
    chat_id = update['message']['chat']['id']
    text = update.get('message', {}).get('text', '')
    
    if chat_id != ADMIN_CHAT_ID and not text.startswith('/'):
        send_message(ADMIN_CHAT_ID, f" {text}") # Форма сообщения
        send_message(chat_id, "")
    elif text.startswith('/start'):
        handle_command(update)
    else:
        send_message(chat_id, "")

def main():
    update_id = None
    while True:
        response = requests.get(f'https://api.telegram.org/bot{TOKEN}/getUpdates?offset={update_id}')
        updates = response.json()['result']
        for update in updates:
            update_id = update['update_id'] + 1
            if 'message' in update:
                if 'text' in update['message']:
                    handle_message(update)
                elif 'entities' in update['message']:
                    if update['message']['entities'][0]['type'] == 'bot_command':
                        handle_command(update)

if __name__ == '__main__':
    main()