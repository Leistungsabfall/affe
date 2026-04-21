import subprocess


class WaylandClipboard:
    @staticmethod
    def write(text):
        for cmd in (['wl-copy'], ['wl-copy', '--primary']):
            subprocess.run(
                args=cmd,
                input=text.encode('utf-8'),
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

    @staticmethod
    def read():
        p = subprocess.run(
            args=['wl-paste'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        text = p.stdout.decode('utf-8')
        return text
