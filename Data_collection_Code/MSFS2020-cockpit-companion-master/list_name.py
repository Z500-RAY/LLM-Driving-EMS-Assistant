import pygetwindow as gw

def list_all_windows():
    windows = gw.getAllTitles()
    for i, title in enumerate(windows):
        print(f"{i + 1}: {title}")

list_all_windows()