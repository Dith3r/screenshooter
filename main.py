import subprocess
import argparse

from datetime import datetime
from pathlib import Path

class Shot:
    @property
    def command(self):
        raise NotImplementedError
    
    def __init__(self):
        time = int(datetime.utcnow().timestamp() * 100)
        home = Path.home()

        command_line = ["maim", Path.home() / "screenshots" / f"{time}.png"]
        command_line = command_line[0:1] + self.command + command_line[-1:]

        result = subprocess.run(command_line, capture_output=True)
        
        if result.returncode:
            print(result.stderr)


class Range(Shot):
    command = ["-s"]


class Screen(Shot):
    command = []


class Window(Shot):
    command = ["-st", '999999']


class Shooter:
    __slots__ = ('_parser')
    _types = {
        "range": Range,
        "screen": Screen,
        "window": Window
    }

    def __init__(self):
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument('type', choices=self._types.keys(), type=str)

    def shoot(self):
        args = self._parser.parse_args()

        if args:
            cmd = self._types[args.type]
            cmd()
        else:
            self._parser.print_help()

    
if __name__ == "__main__":
    shooter = Shooter().shoot()