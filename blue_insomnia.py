# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                                 Blue Incomnia                                 ║
# ╟───────────────────────────────────────────────────────────────────────────────╢
# ║  Author     :  Ratbag (Dove)                                                  ║
# ║                                                                               ║
# ║  Github     :  https://github.com/DeadDove13                                  ║
# ║                                                                               ║
# ║  Description:  Prevents Windows from sleeping. Tray icon + rich terminal UI.  ║
# ║                 Left-click toggles, right-click exits.                        ║
# ║                                                                               ║
# ║  Notes      :  Tray icons not cleaned up. No state persistence.               ║
# ║                 Requires Windows + pywin32 + Pillow.                          ║
# ║                                                                               ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝
import ctypes
import subprocess
import re
import sys
import threading
import os
import uuid
import random
import win32api
import win32con
import win32gui
from PIL import Image, ImageDraw
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Constants for sleep prevention flags
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001

# Global state variables
sleep_prevention_enabled = False
state_lock = threading.Lock()
console = Console()
tray = None

#------------- SLEEP STATE MANAGEMENT -------------
# Checks current Windows power settings to determine if sleep is disabled
def get_current_sleep_state() -> bool:
    try:
        output = subprocess.check_output(
            "powercfg -query SCHEME_CURRENT SUB_SLEEP STANDBYIDLE",
            shell=True, text=True
        )
        match = re.search(r"AC Power Setting Index:\s*0x([0-9A-Fa-f]+)", output)
        return bool(match and int(match.group(1), 16) == 0)
    except subprocess.CalledProcessError:
        return False

# Enables or disables system sleep prevention
def set_sleep_prevention(enable: bool):
    global sleep_prevention_enabled
    flags = ES_CONTINUOUS | (ES_SYSTEM_REQUIRED if enable else 0)
    ctypes.windll.kernel32.SetThreadExecutionState(flags)
    with state_lock:
        sleep_prevention_enabled = enable

#------------- RICH TERMINAL UI -------------
# Generates the layout for the terminal interface
def generate_layout() -> Panel:
    with state_lock:
        enabled = sleep_prevention_enabled
    status = Text("Sleep Prevention: ", style="bold white")
    status.append("ON" if enabled else "OFF", style="blue" if enabled else "red")

    table = Table(show_header=False, show_lines=False, expand=False, padding=(0,1))
    table.add_column("Key", style="yellow", justify="right", no_wrap=True)
    table.add_column("Action", style="white")
    table.add_row("1", "Toggle Sleep Prevention")
    table.add_row("0", "Exit")

    art = Text(
"""
  _______ __                 ___                                  __       
 |   _   |  .--.--.-----.   |   .-----.-----.-----.--------.-----|__.---.-.
 |.  1   |  |  |  |  -__|   |.  |     |__ --|  _  |        |     |  |  _  |
 |.  _   |__|_____|_____|   |.  |__|__|_____|_____|__|__|__|__|__|__|___._|
 |:  1    \                 |:  |                                          
 |::.. .  /                 |::.|                                          
 `-------'                  `---'                                         
""", style="bold blue")

    return Panel.fit(Group(art, status, Text("\n"), table), title="[cyan]Menu[/cyan]", border_style="blue")

#------------- TRAY ICON GENERATOR -------------
# Draws a coloured circle icon (blue/red) and saves as .ico for tray

def make_icon(color: tuple) -> str:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((2, 2, 14, 14), fill=color)
    filename = f"tray_icon_{uuid.uuid4().hex}.ico"
    path = os.path.join(os.getenv("TEMP"), filename)
    img.save(path, format="ICO")
    return path

#------------- TRAY ICON HANDLER CLASS -------------
class SysTrayIcon:
    def __init__(self, on_toggle, on_exit):
        self.on_toggle = on_toggle
        self.on_exit = on_exit
        self.hinst = win32api.GetModuleHandle(None)
        self.class_name = "SleepTrayIcon"
        self.hwnd = None
        self.callback_message = win32con.WM_USER + 20

        self._register_class()
        self._create_window()
        self.update_icon(sleep_prevention_enabled)

    # Main event loop
    def run(self):
        win32gui.PumpMessages()

    # Registers window class with callback function
    def _register_class(self):
        wndclass = win32gui.WNDCLASS()
        wndclass.lpfnWndProc = self._wnd_proc
        wndclass.lpszClassName = self.class_name
        self.class_atom = win32gui.RegisterClass(wndclass)

    # Creates invisible window required for tray icon
    def _create_window(self):
        self.hwnd = win32gui.CreateWindow(
            self.class_atom,
            self.class_name,
            0, 0, 0, 0, 0, 0, 0,
            self.hinst,
            None
        )

    # Updates the icon in system tray (blue for enabled, red for disabled)
    def update_icon(self, enabled):
        color = (0, 0, 200, 255) if enabled else (200, 0, 0, 255)
        ico_path = make_icon(color)

        hicon = win32gui.LoadImage(
            self.hinst,
            ico_path,
            win32con.IMAGE_ICON,
            0, 0,
            win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        )
        tip = f"Sleep Prevention: {'ON' if enabled else 'OFF'} | {random.randint(1000,9999)}"
        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, self.callback_message, hicon, tip)

        try:
            win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)
        except Exception:
            win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)

    # Handles tray events (left click to toggle, right click to show menu)
    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == self.callback_message and lparam == win32con.WM_LBUTTONUP:
            self.on_toggle()
        elif msg == self.callback_message and lparam == win32con.WM_RBUTTONUP:
            self._show_menu()
        elif msg == win32con.WM_DESTROY:
            win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, (self.hwnd, 0))
            win32gui.PostQuitMessage(0)
        elif msg == win32con.WM_COMMAND:
            if wparam == 1023:
                self.on_exit()
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    # Creates and shows context menu on right click
    def _show_menu(self):
        menu = win32gui.CreatePopupMenu()
        win32gui.AppendMenu(menu, win32con.MF_STRING, 1023, "Exit")
        pos = win32gui.GetCursorPos()
        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None)
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

#------------- ACTION HANDLER -------------
# Toggles the sleep prevention state and updates UI + tray icon
def toggle_state(icon=None, item=None):
    set_sleep_prevention(not sleep_prevention_enabled)
    if tray:
        tray.update_icon(sleep_prevention_enabled)
    console.clear()
    console.print(generate_layout())
    console.print("[bold white]Enter choice:[/bold white] ", end="")
    sys.stdout.flush()

# Creates the tray icon in a background thread
def create_tray():
    def _exit():
        win32gui.PostMessage(tray.hwnd, win32con.WM_DESTROY, 0, 0)
        os._exit(0)
    global tray
    tray = SysTrayIcon(on_toggle=toggle_state, on_exit=_exit)
    tray.run()

#------------- MAIN LOOP -------------
if __name__ == "__main__":
    sleep_prevention_enabled = get_current_sleep_state()
    threading.Thread(target=create_tray, daemon=True).start()

    console.clear()
    console.print(generate_layout())
    console.print("[bold white]Enter choice:[/bold white] ", end="")
    sys.stdout.flush()

    while True:
        try:
            choice = input().strip()
        except (KeyboardInterrupt, EOFError):
            break
        if choice == "1":
            toggle_state()
        elif choice == "0":
            if tray:
                win32gui.PostMessage(tray.hwnd, win32con.WM_DESTROY, 0, 0)
            break
        else:
            console.clear()
            console.print(generate_layout())
            console.print("[bold white]Enter choice:[/bold white] ", end="")
            sys.stdout.flush()
    sys.exit(0)
#------------- END MAIN -------------
