# common-utils
A personal collection of general-purpose PowerShell and Python scripts used for automation, system utilities, and small tooling tasks. Centralizes standalone scripts that don’t warrant their own repositories.

---

## Tools

### `blue_insomnia.py`
**Tray and CLI sleep toggle for Windows.**  
Toggle system sleep mode via CLI or a tray icon. Useful for keeping a machine awake during long tasks (Running an archive bot for example). 
Allows you to lock your computer when afk without it going to sleep.

**Dependencies:**  
- `pywin32`  
- `Pillow`  
- `rich` 

---

### `boxgen.py`
**Create multi-line comment banners with GUI.**  
Generate boxed comment headers for multiple programming languages. Supports inline and newline content modes.

**Dependencies:**  
- `tkinter` (builtin)  
- `ttk`, `ScrolledText`

---

### `punkys_cypher.py`
**Punkys substitution cipher.**  
Simple monoalphabetic substitution cipher with support for custom symbols. Encrypt/decrypt via terminal interaction.
Basicly useless, but I needed somewhere to put this, as people keep asking me for it

**Dependencies:**  
- `colorama`

---

### `run.bat`
**Used to launch Python scripts on click.**  
A minimal batch launcher for Python scripts with terminal pause. Useful for when you cbf navigating to the file in cmd. Allows for double-click to run `.py` scripts.

---

## Author

**Ratbag (Dove)**  
[github.com/DeadDove13](https://github.com/DeadDove13)
