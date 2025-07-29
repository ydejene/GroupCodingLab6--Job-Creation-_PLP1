import os


def clear_screen():
    """Clear the terminal screen"""
    if os.name == 'nt':  
        os.system('cls')
    else: 
        os.system('clear')

def pause():
    """Wait for user to press Enter"""
    input("\nPress Enter to return to main menu...")
