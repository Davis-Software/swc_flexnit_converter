import subprocess


def main():
    subprocess.run(["pip", "install", "-r", "requirements.txt"], shell=True)
    subprocess.run(
        ["npm", "install"],
        shell=True,
        cwd="static/js/front"
    )
    subprocess.run(
        ["npm", "run", "prod"],
        shell=True,
        cwd="static/js/front"
    )
    subprocess.run(["pyinstaller", "swc_flexnit_converter.spec"], shell=True)


if __name__ == "__main__":
    main()
