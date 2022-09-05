import time
import os
from colorama import init
from colorama import Fore, Back, Style


from termcolor import colored


init()

for item in 5, 4, 3, 2, 1:
    print(colored("[GOODBYE]", "magenta", attrs=["underline", "bold"]) + " Programma terminato in " +
          colored("  " + str(item) + "  ", "magenta", "on_white", attrs=["bold"],) + " secondi" + colored(" [GOODBYE]", "magenta", attrs=["underline", "bold"]) + "\r", end="")
    time.sleep(1)

os.system("cls")

print(colored("[EXIT] Bye Bye >:D\n\n\r", "magenta", attrs=["bold"]))

input(colored("[INPUT]", "yellow", attrs=["bold"]) + " Premi " + colored("[ ENTER ]", "white",
      "on_green", attrs=["bold"]) + " per chiudere il programma...")
