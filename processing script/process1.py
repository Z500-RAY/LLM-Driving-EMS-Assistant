import subprocess

# Function to open a new terminal and execute commands
def run_scripts():
    # Command to open a new terminal, navigate to the directory, activate conda environment, and run 0831.py
    command1 = (
        'start cmd /k "cd /d C:/Users/888/Desktop/0824 && conda activate aviation && python 0831.py"'
    )
    # Command to open a new terminal, navigate to the directory, activate conda environment, and run 0903.py
    command2 = (
        'start cmd /k "cd /d C:/Users/888/Desktop/0824 && conda activate aviation && python 0903.py"'
    )

    # Run each command in a separate terminal
    subprocess.Popen(command1, shell=True)
    subprocess.Popen(command2, shell=True)

if __name__ == "__main__":
    run_scripts()
