def clean_text(text: str) -> str:
    """문자열의 양쪽 공백과 쉼표(,)를 제거합니다."""
    return text.strip().replace(',', '')
