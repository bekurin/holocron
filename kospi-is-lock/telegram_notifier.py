import requests

class TelegramNotifier:
    """메시지 전송을 담당하는 서드파티 통합 클래스"""
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def send_message(self, text):
        if not self.token:
            print("텔레그램 토큰이 설정되지 않아 콘솔에만 출력합니다.")
            return
            
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': 'Markdown'
        }
        try:
            requests.post(url, data=payload)
        except Exception as e:
            print(f"Telegram 메시지 전송 실패: {e}")
