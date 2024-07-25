import os
from colorama import Fore, Back, Style
from website import ultimate
from term_image.image import from_url
import webbrowser
from PIL import Image
import fontstyle


def clear_screen():
    while True:
        try:
            clear_input = str(input("Clear screen for more room? (Press Y or N): ")).strip().lower()
            if clear_input == 'y':
                if os.name == 'nt': 
                    os.system('cls')
                else: os.system('clear')
                break
            elif clear_input == 'n': break
        except ValueError: print("Please enter a Valid Value")
    

   




def main():
    clear_screen()
    
    
    text = fontstyle.apply("Craiglist CLI!\n\n A questionably worse way of viewing craigslist posts!",
                    "bold/Italic/purple")
    
    print(text)

    ultimate.all_marketplaces()


if __name__ == "__main__":
    main()
