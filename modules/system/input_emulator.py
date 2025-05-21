# modules/system/input_emulator.py
import ctypes
import os

dll_path = os.path.abspath("forge_input.dll")
forge = ctypes.WinDLL(dll_path)

# Bind functions
type_text = forge.type_text
type_text.argtypes = [ctypes.c_char_p]
type_text.restype = None

move_mouse = forge.move_mouse
move_mouse.argtypes = [ctypes.c_int, ctypes.c_int]
move_mouse.restype = None

click_mouse = forge.click_mouse
click_mouse.restype = None

# Optional wrappers
def send_keys(text: str):
    type_text(text.encode('utf-8'))

def move_cursor(x: int, y: int):
    move_mouse(x, y)

def click():
    click_mouse()
