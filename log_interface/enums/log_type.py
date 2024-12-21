from enum import Enum

class LogType(Enum):
    """
    Enumeration the holds the different log types that can be received
    """
    Event = 0
    Information = 1
    Bug = 2
    Warning = 3