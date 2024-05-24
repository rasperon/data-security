import os

def yazdir_logo():
    # CMD ekranını temizle
    os.system("cls" if os.name == "nt" else "clear")

    logo = """
______                                     
| ___ \                                    
| |_/ /__ _ ___ _ __   ___ _ __ ___  _ __  
|    // _` / __| '_ \ / _ \ '__/ _ \| '_ \ 
| |\ \ (_| \__ \ |_) |  __/ | | (_) | | | |
\_| \_\__,_|___/ .__/ \___|_|  \___/|_| |_|
               | |                         
               |_|                         
    """
    print(logo)

# filigran dosyası içindeki ASCII logosunu yazdırıyoruz
if __name__ == "__main__":
    yazdir_logo()