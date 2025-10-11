import time


class NewsInformation:
    def __init__(self) -> None:
        self.title = ""
        self.link = ""
        self.published: time.struct_time | None = None

    def __repr__(self) -> str:
        return f"NewsInformation(title='{self.title}', link='{self.link}', published='{self.published}')"
