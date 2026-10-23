import os
import shutil
from colorama import init, Fore, Style

# Initialize colorama for Windows/Linux/Chromebook ANSI translation
init(autoreset=True)

# Custom color palette matching the uploaded UI
HOT_PINK = "\033[38;2;255;0;160m"
BRIGHT_MAGENTA = "\033[38;2;255;30;200m"
MAGENTA = "\033[38;2;255;0;255m"
CYAN = "\033[38;2;0;220;255m"
GREEN = "\033[38;2;40;220;120m"
YELLOW = "\033[38;2;255;200;50m"
RED = "\033[38;2;255;50;50m"
WHITE = "\033[38;2;245;245;245m"
GRAY = "\033[38;2;120;120;120m"
RESET = Style.RESET_ALL

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_banner(author="aqxior"):
    clear_screen()
    ascii_art = f"""
{HOT_PINK} /__  \\|  \\  \\ \\ / /  _   | |   _   \\
/ /\\  \\| | \\  \\ V /  | | | | | |_)  /
|  _   | |  \\   /   | | | | |  _  < 
| | |  | \\  / / \\ \\ | |_| | | | \\  \\
\\_| |_/\\__// /   \\_\\ \\___/|_|_|  \\_\\{RESET}
"""
    print(ascii_art)
    
    term_width = shutil.get_terminal_size((80, 24)).columns
    max_w = min(term_width, 78)
    line = "─" * max_w
    print(f"{HOT_PINK}{line}{RESET}")
    
    subtext = f"MADE BY - {author}"
    pad = max(0, (max_w - len(subtext)) // 2)
    print(" " * pad + f"{Style.BRIGHT}{WHITE}{subtext}{RESET}\n")

def render_menu(items, prompt_tag="aqxior"):
    mid = (len(items) + 1) // 2
    left_col = items[:mid]
    right_col = items[mid:]

    col_width = 36
    total_inner_width = col_width * 2 + 3

    print(f"{HOT_PINK}╭{'─' * total_inner_width}╮{RESET}")

    max_rows = max(len(left_col), len(right_col))
    for i in range(max_rows):
        left_item = left_col[i] if i < len(left_col) else None
        right_item = right_col[i] if i < len(right_col) else None

        if left_item:
            num_str = f"{HOT_PINK}[{BRIGHT_MAGENTA}{str(left_item['num']).rjust(2)}{HOT_PINK}]{RESET}"
            title_str = f"{WHITE}{left_item['title'][:col_width - 8].ljust(col_width - 8)}{RESET}"
            left_str = f"  {num_str} {title_str}"
        else:
            left_str = " " * col_width

        if right_item:
            num_str = f"{HOT_PINK}[{BRIGHT_MAGENTA}{str(right_item['num']).rjust(2)}{HOT_PINK}]{RESET}"
            title_str = f"{WHITE}{right_item['title'][:col_width - 8].ljust(col_width - 8)}{RESET}"
            right_str = f"  {num_str} {title_str}"
        else:
            right_str = " " * col_width

        print(f"{HOT_PINK}│{RESET}{left_str} {HOT_PINK}│{RESET}{right_str} {HOT_PINK}│{RESET}")

    print(f"{HOT_PINK}╰{'─' * total_inner_width}╯{RESET}\n")
    return f"{RED}({prompt_tag}){RESET} {WHITE}Option:{RESET} "
