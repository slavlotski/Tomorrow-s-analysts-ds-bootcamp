import requests
import requests_mock
import pytest
from config.tokens import TELEGRAM_BOT_TOKEN, OPENAI_API_KEY

# Define constants for the API endpoints and tokens
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
OPENAI_API_URL = "https://api.openai.com/v1/engines/davinci-codex/completions"

# Mock data for testing
TELEGRAM_MESSAGE = {
    "chat_id": "123456789",
    "text": "Hello, this is a test message."
}

OPENAI_PROMPT = {
    "prompt": "Translate the following English text to French: 'Hello, how are you?'",
    "max_tokens": 60
}

def send_telegram_message(message):
    headers = {"Content-Type": "application/json"}
    response = requests.post(TELEGRAM_API_URL, json=message, headers=headers)
    return response

def get_openai_completion(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    response = requests.post(OPENAI_API_URL, json=prompt, headers=headers)
    return response

# Test for Telegram API
def test_telegram_api():
    with requests_mock.Mocker() as m:
        m.post(TELEGRAM_API_URL, status_code=200)
        response = send_telegram_message(TELEGRAM_MESSAGE)
        assert response.status_code == 200

# Test for OpenAI API
def test_openai_api():
    with requests_mock.Mocker() as m:
        m.post(OPENAI_API_URL, status_code=200)
        response = get_openai_completion(OPENAI_PROMPT)
        assert response.status_code == 200

if __name__ == "__main__":
    pytest.main()
