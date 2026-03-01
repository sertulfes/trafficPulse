import os
import sys
import subprocess

def run():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    venv_path = os.path.join(project_dir, "venv")

    # Create venv if it doesn't exist
    if not os.path.exists(venv_path):
        subprocess.run([sys.executable, "-m", "venv", "venv"])

    # Activate and install requirements
    if os.name == "nt":
        python_exec = os.path.join(venv_path, "Scripts", "python")
    else:
        python_exec = os.path.join(venv_path, "bin", "python")

    subprocess.run([python_exec, "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.run([python_exec, "app.py"])

if __name__ == "__main__":
    run()
