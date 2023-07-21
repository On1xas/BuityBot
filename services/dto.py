from dataclasses import dataclass


class DTO:
    id: int
    username: str
    first_name: str
    last_name: str
    language_code: str
    chat_id: int
    chat_type: str
    last_msg: str