import os
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from assets.logo import yazdir_logo

yazdir_logo()
class AESCipher:
    def __init__(self, key: bytes):
        self.key = key
        self.backend = default_backend()
        self.block_size = algorithms.AES.block_size

    def encrypt(self, plaintext: str) -> bytes:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(self.block_size).padder()
        padded_plaintext = padder.update(plaintext.encode()) + padder.finalize()
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

        return iv + ciphertext

    def decrypt(self, ciphertext: bytes) -> str:
        iv = ciphertext[:16]
        actual_ciphertext = ciphertext[16:]

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(self.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return plaintext.decode()

console = Console()
key = os.urandom(32)
cipher = AESCipher(key)

# Dil seçimi
language = Prompt.ask("[bold cyan]Choose a language / Bir dil seçin (en/tr):[/bold cyan]", choices=["en", "tr"])

# Mesajlar
messages = {
    "en": {
        "welcome": "[bold magenta]Welcome to Rasperon Cipher Factory[/bold magenta]",
        "action_prompt": "[bold cyan]Choose an action (encrypt/decrypt/exit):[/bold cyan]",
        "exit": "[bold red]Exiting...[/bold red]",
        "enter_text_encrypt": "[bold yellow]Enter text to encrypt:[/bold yellow]",
        "enter_text_decrypt": "[bold yellow]Enter text to decrypt (in hex format):[/bold yellow]",
        "encryption_result": "Encryption Result",
        "original_text": "Original Text",
        "encrypted_text": "Encrypted Text",
        "decryption_result": "Decryption Result",
        "decrypted_text": "Decrypted Text",
        "error": "[bold red]Error:[/bold red]",
        "program_end": "[bold green]Program terminated.[/bold green]",
        "save_to_file": "Do you want to save the result to a file? (yes/no):",
        "file_saved": "Result saved to file: {}"
    },
    "tr": {
        "welcome": "[bold magenta]Rasperon Şifreleme Fabrikasına Hoşgeldiniz[/bold magenta]",
        "action_prompt": "[bold cyan]Bir işlem seçin (şifrele/deşifrele/çıkış):[/bold cyan]",
        "exit": "[bold red]Çıkış yapılıyor...[/bold red]",
        "enter_text_encrypt": "[bold yellow]Şifrelenecek metni girin:[/bold yellow]",
        "enter_text_decrypt": "[bold yellow]Şifresi çözülecek metni girin (hex formatında):[/bold yellow]",
        "encryption_result": "Şifreleme Sonucu",
        "original_text": "Orijinal Metin",
        "encrypted_text": "Şifrelenmiş Metin",
        "decryption_result": "Deşifreleme Sonucu",
        "decrypted_text": "Çözümlenmiş Metin",
        "error": "[bold red]Hata:[/bold red]",
        "program_end": "[bold green]Program sonlandırıldı.[/bold green]",
        "save_to_file": "Sonucu bir dosyaya kaydetmek ister misiniz? (evet/hayır):",
        "file_saved": "Sonuç dosyaya kaydedildi: {}"
    }
}

msg = messages[language]
console.print(msg["welcome"])

def save_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    console.print(msg["file_saved"].format(filename))

while True:
    action = Prompt.ask(msg["action_prompt"], choices=["encrypt", "decrypt", "exit"] if language == "en" else ["şifrele", "deşifrele", "çıkış"])

    if action == "exit" or action == "çıkış":
        console.print(msg["exit"])
        break
    elif action == "encrypt" or action == "şifrele":
        plaintext = Prompt.ask(msg["enter_text_encrypt"])
        ciphertext = cipher.encrypt(plaintext)
        ciphertext_hex = ciphertext.hex()

        table = Table(title=msg["encryption_result"])
        table.add_column(msg["original_text"], justify="center", style="cyan")
        table.add_column(msg["encrypted_text"], justify="center", style="magenta")
        table.add_row(plaintext, "\n".join([ciphertext_hex[i:i+64] for i in range(0, len(ciphertext_hex), 64)]))
        console.print(table)

        console.print(f"\n{msg['encrypted_text']}: {ciphertext_hex}\n")
        save = Prompt.ask(msg["save_to_file"], choices=["yes", "no"] if language == "en" else ["evet", "hayır"])
        if save == "yes" or save == "evet":
            save_to_file(ciphertext_hex, "encrypted.txt")

    elif action == "decrypt" or action == "deşifrele":
        ciphertext_hex = Prompt.ask(msg["enter_text_decrypt"])
        try:
            ciphertext = bytes.fromhex(ciphertext_hex)
            decrypted_plaintext = cipher.decrypt(ciphertext)

            table = Table(title=msg["decryption_result"])
            table.add_column(msg["encrypted_text"], justify="center", style="magenta")
            table.add_column(msg["decrypted_text"], justify="center", style="cyan")
            table.add_row("\n".join([ciphertext_hex[i:i+64] for i in range(0, len(ciphertext_hex), 64)]), decrypted_plaintext)
            console.print(table)

            console.print(f"\n{msg['decrypted_text']}: {decrypted_plaintext}\n")
            save = Prompt.ask(msg["save_to_file"], choices=["yes", "no"] if language == "en" else ["evet", "hayır"])
            if save == "yes" or save == "evet":
                save_to_file(decrypted_plaintext, "decrypted.txt")
        except Exception as e:
            console.print(f"{msg['error']} {str(e)}")

console.print(msg["program_end"])
