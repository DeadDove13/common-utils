:: ╔════════════════════════════════════════════════════════════════════════════════╗
:: ║                                  Run Script                                    ║
:: ╟────────────────────────────────────────────────────────────────────────────────╢
:: ║  Author     :  Ratbag (Dove)                                                   ║
:: ║                                                                                ║
:: ║  Github     :  https://github.com/DeadDove13                                   ║
:: ║                                                                                ║
:: ║  Description:  Launches a Python script from a .bat file.                      ║
:: ║                 Useful for double-click running scripts with terminal pause.   ║
:: ║                                                                                ║
:: ║  Notes      :  Place this within the same folder as your script and            ║
:: ║                 change "script_name.py" to the name of your script.            ║
:: ║                 Remove 'setlocal' if modifying environment variables globally  ║
:: ╚════════════════════════════════════════════════════════════════════════════════╝
@echo off
setlocal

::Change the File path to your script
python "script_name.py"
pause