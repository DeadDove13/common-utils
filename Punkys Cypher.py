# ╔════════════════════════════════════════════════════════════════════════════════╗
# ║                                 Punkys Cypher                                  ║
# ╟────────────────────────────────────────────────────────────────────────────────╢
# ║  Author     :  Ratbag (Dove)                                                   ║
# ║                                                                                ║
# ║  Github     :  https://github.com/DeadDove13                                   ║
# ║                                                                                ║
# ║  Description:  Simple monoalphabetic substitution cipher with custom symbols.  ║
# ║                 Encrypts or decrypts character-by-character in the console.    ║
# ║                                                                                ║
# ║  Notes      :  Uses the colorama library                                       ║
# ║                                                                                ║
# ╚════════════════════════════════════════════════════════════════════════════════╝
from colorama import init, Fore, Style

#------------- INIT COLORAMA -------------
init(autoreset=True)

#------------- CIPHER MAPPINGS -------------
# letter -> symbol mapping
cipher = {
    'a': "8", 'b': "3", 'c': "1", 'd': "4", 'e': "7",
    'f': "5", 'g': "$", 'h': "#", 'i': "^", 'j': "*",
    'k': "!", 'l': "?", 'm': "=", 'n': "&", 'o': "%",
    'p': "<", 'q': ">", 'r': "(", 's': ")", 't': "+",
    'u': "/", 'v': ",", 'w': "6", 'x': "h", 'y': "n",
    'z': "p"
}

# symbol -> letter mapping (for decryption)
reverse_cipher = {v: k for k, v in cipher.items()}


#------------- BANNER DISPLAY -------------
def print_banner():
    print(Fore.GREEN + r"""
                    _                                 _               
                   | |                               | |              
  _ __  _   _ _ __ | | ___   _ ___    ___ _   _ _ __ | |__   ___ _ __ 
 | '_ \| | | | '_ \| |/ / | | / __|  / __| | | | '_ \| '_ \ / _ \ '__|
 | |_) | |_| | | | |   <| |_| \__ \ | (__| |_| | |_) | | | |  __/ |   
 | .__/ \__,_|_| |_|_|\_\\__, |___/  \___|\__, | .__/|_| |_|\___|_|   
 | |                      __/ |            __/ | |                    
 |_|                     |___/            |___/|_|                    
""" + Style.RESET_ALL)

    print(Fore.YELLOW + "GitHub: DeadDove13" + Style.RESET_ALL + "\n")


#------------- ENCRYPT STRING -------------
def encrypt_string(text):
    # Convert to lowercase and map each char
    return ''.join(cipher.get(c, c) for c in text.lower())


#------------- DECRYPT STRING -------------
def decrypt_string(text):
    # Reverse map each symbol back to a letter
    return ''.join(reverse_cipher.get(c, c) for c in text)


#------------- MAIN LOOP -------------
def main():
    print_banner()

    while True:
        print("Select an option:")
        print("1: Encrypt")
        print("2: Decrypt")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            text = input("Enter text to encrypt: ")
            print("Encrypted text:", encrypt_string(text), "\n")
        elif choice == "2":
            text = input("Enter text to decrypt: ")
            print("Decrypted text:", decrypt_string(text), "\n")
        else:
            # fallback for invalid option
            print("Do you have rocks in your head mate? Please select 1 or 2.\n")

#------------- ENTRY POINT -------------
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # exit cleanly on Ctrl+C
        print("\nExiting...")

    # pause on exit so double-clicking doesn’t insta-close
    input("Press Enter to exit...")
