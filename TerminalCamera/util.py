import ctypes

# Windows types
class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

class SMALL_RECT(ctypes.Structure):
    _fields_ = [("Left", ctypes.c_short),
                ("Top", ctypes.c_short),
                ("Right", ctypes.c_short),
                ("Bottom", ctypes.c_short)]

class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [
        ("dwSize", COORD),
        ("dwCursorPosition", COORD),
        ("wAttributes", ctypes.c_ushort),
        ("srWindow", SMALL_RECT),
        ("dwMaximumWindowSize", COORD)
    ]

def get_console_size():
    csbi = CONSOLE_SCREEN_BUFFER_INFO()
    h = ctypes.windll.kernel32.GetStdHandle(-11)

    # Get console size in row, col
    if ctypes.windll.kernel32.GetConsoleScreenBufferInfo(h, ctypes.byref(csbi)):
        rows = csbi.srWindow.Bottom - csbi.srWindow.Top + 1
        cols = csbi.srWindow.Right - csbi.srWindow.Left + 1
        return rows, cols
    else:
        return None