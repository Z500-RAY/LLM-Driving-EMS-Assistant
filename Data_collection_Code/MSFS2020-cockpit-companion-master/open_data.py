import requests
import os
import time

def open_file():

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop_path, "data.txt")

    open(file_path, 'r')

if __name__ == "__main__":
    open_file()