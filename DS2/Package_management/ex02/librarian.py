import subprocess
import os

class Installing:
    def test_venv(self):
        if not os.environ.get("VIRTUAL_ENV"):
            raise Exception("Venv deactivated")

    #def install_libraries(self):
    #subprocess.run(["pip", "install", "beautifulsoup4", "pytest"], check=True)

    def install_libraries(self):
        subprocess.run(["pip", "install",  "-r", "requirement.txt"], check=True)

    def show_libraries(self):
        subprocess.run(["pip", "freeze"])
        with open("requirements.txt", "w") as f:
            subprocess.run(["pip", "freeze"], stdout=f)

if __name__ == "__main__":
    try:
        install=Installing()
        install.test_venv()
        install.install_libraries()
        install.show_libraries()
    except subprocess.CalledProcessError as error:
        print(f"Error with installing libraries: {error}")
    except Exception as error:
        print(error)
