from PySide6.QtCore import QThread, Signal
import subprocess
import re

class FFmpegThread(QThread):
    progress = Signal(int)
    status_message = Signal(str)
    finished = Signal(bool)

    def __init__(self, command, parent=None):
        super().__init__(parent)
        self.command = command

    def run(self):
        try:
            process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            total_duration = None
            for line in process.stderr:
                self.status_message.emit(line.strip())  # Emit the raw stderr line

                # Extract total duration from the first line containing "Duration"
                if "Duration" in line and total_duration is None:
                    match = re.search(r"Duration: (\d+):(\d+):(\d+)\.(\d+)", line)
                    if match:
                        h, m, s, ms = map(int, match.groups())
                        total_duration = h * 3600 + m * 60 + s + ms / 100
                # Extract elapsed time from lines containing "time="
                elif "time=" in line:
                    match = re.search(r"time=(\d+):(\d+):(\d+)\.(\d+)", line)
                    if match and total_duration:
                        h, m, s, ms = map(int, match.groups())
                        elapsed_time = h * 3600 + m * 60 + s + ms / 100
                        progress = int((elapsed_time / total_duration) * 100)
                        self.progress.emit(progress)

            process.wait()
            self.finished.emit(process.returncode == 0)
        except Exception as e:
            self.status_message.emit(f"Error: {e}")
            self.finished.emit(False)
