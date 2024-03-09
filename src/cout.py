
# Print utility wrapper
def print_banner():
    import colorama

    colorama.init(autoreset=True)

    # Write name of the utility
    print("\n\033[33m\033[1m"+"\
     /$$$$$$$  /$$   /$$ /$$$$$$  /$$$$$$  /$$   /$$ /$$$$$$$$ /$$$$$$$ \n\
    | $$__  $$| $$  | $$|_  $$_/ /$$__  $$| $$  | $$| $$_____/| $$__  $$\n\
    | $$  \\ $$| $$  | $$  | $$  | $$  \\__/| $$  | $$| $$      | $$  \\ $$\n\
    | $$$$$$$/| $$$$$$$$  | $$  |  $$$$$$ | $$$$$$$$| $$$$$   | $$$$$$$/\n\
    | $$____/ | $$__  $$  | $$   \\____  $$| $$__  $$| $$__/   | $$__  $$\n\
    | $$      | $$  | $$  | $$   /$$  \\ $$| $$  | $$| $$      | $$  \\ $$\n\
    | $$      | $$  | $$ /$$$$$$|  $$$$$$/| $$  | $$| $$$$$$$$| $$  | $$\n\
    |__/      |__/  |__/|______/ \\______/ |__/  |__/|________/|__/  |__/")

    # Positioning the cursor to display the utility version
    version = "1.0.1#dev"
    print("\033[7A\033[80C\033[1m"+"{"+"\033[32m"+version+"\033[39m"+"}")
    # Positioning the cursor to display the team name
    print("\033[4B\033[80C\033[1m"+"King Arthur's team")
    # Reset the cursor position
    print("\033[8B\033[80D")

    # Print referece
    print(
        "\033[1m"+"    Usage: python phisher.py [options] [input_file] [api_key]\n")


# Counts down the percentage and outputs it to the console
def print_percents(cnt):
    intcnt = int(cnt)
    percents = "####################################################################################################"
    dots = "...................................................................................................."
    if intcnt != 100:
        print("["+percents[:intcnt]+dots[intcnt:]+"] " +
              "\033[33m" + str(intcnt) + "%", end="\r")
    else:
        print("["+percents[:intcnt]+dots[intcnt:] +
              "] " + "\033[33m" + str(intcnt) + "%")
