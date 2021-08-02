from enum import Enum

class CardColors(Enum):
    RED = 0
    BLUE = 1
    YELLOW = 2
    GREEN = 3
    BLACK = 4

class Card:
    def __init__(self, color, value) -> None:
        self.color = color
        self.value = value

    def __str__(self) -> str:
        return str((self.color, self.value))

    def __repr__(self) -> str:
        return str((self.color, self.value))