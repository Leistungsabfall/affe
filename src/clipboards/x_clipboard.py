import subprocess


class XClipboard:
    @staticmethod
    def write(text):
        for clipboard in ('primary', 'clipboard',):
            subprocess.run(
                args=['xclip', '-selection', clipboard],
                input=text.encode('utf-8'),
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

    @staticmethod
    def read():
        p = subprocess.run(
            args=['xclip', '-selection', 'primary', '-o'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        text = p.stdout.decode('utf-8')
        return text
