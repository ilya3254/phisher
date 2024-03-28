# Print utility wrapper
def print_banner():
    import colorama

    colorama.init(autoreset=True)

    # Write name of the utility
    print("\n\033[33m\033[1m" + "\
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
    print("\033[7A\033[80C\033[1m" + "{" + "\033[32m" + version + "\033[39m" + "}")
    # Positioning the cursor to display the team name
    print("\033[4B\033[80C\033[1m" + "Knights of the Round Table")
    # Reset the cursor position
    print("\033[8B\033[80D")

    # Print referece
    print(
        "\033[1m" + "    Usage: python phisher [options] [input_file] [api_key]\n")


# Counts down the percentage and outputs it to the console
def print_percents(cnt: int):
    percents = "#" * 100
    dots = "." * 100
    if cnt != 100:
        print("[" + percents[:cnt] + dots[cnt:] + "] " +
              "\033[33m" + str(cnt) + "%", end="\r")
    else:
        print("[" + percents[:cnt] + dots[cnt:] +
              "] " + "\033[33m" + str(cnt) + "%")
