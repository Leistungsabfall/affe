import subprocess


class PBClipboard:
    @staticmethod
    def write(text):
        subprocess.run(
            args=['pbcopy'],
            input=text.encode('utf-8'),
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    @staticmethod
    def read():
        p = subprocess.run(
            args=['pbpaste'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        text = p.stdout.decode('utf-8')
        return text
