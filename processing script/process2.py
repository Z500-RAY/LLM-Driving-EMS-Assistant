import subprocess
import webbrowser

# Function to open a new terminal and execute commands
def run_glass_server():
    # Command to open a new terminal, navigate to the directory, activate conda environment, and run glass_server.py
    command = (
        'start cmd /k "cd /d C:/Users/888/Desktop/MFS2020-CC/MSFS2020-cockpit-companion-master && conda activate mfs2020 && python glass_server.py"'
    )
    subprocess.Popen(command, shell=True)

if __name__ == "__main__":
    run_glass_server()
    
    # Open localhost:5000 in the default web browser
    webbrowser.open("http://localhost:5000")