import requests
import sys

# Конфигурация (в проде лучше использовать .env)
BOT_TOKEN = "ВАШ_ТОКЕН"
CHAT_ID = "ВАШ_ID"


def send_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        resp = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
        resp.raise_for_status()
        print("Текст успешно отправлен.")
    except Exception as e:
        print(f"Ошибка при отправке: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        send_file(sys.argv[1])
    else:
        print("Инструкция: python tg_sender.py input.txt")
