from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QComboBox,
    QLabel, QRadioButton, QHBoxLayout, QGroupBox, QTextEdit, QProgressBar,
    QMessageBox,
)
from PySide6.QtCore import Qt
import sys

from ffmpeg_thread import FFmpegThread

class FileSelectorApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the user interface
        self.initUI()

    def initUI(self):
        # Create a button for selecting the file
        self.selectButton = QPushButton("Select File", self)
        self.selectButton.clicked.connect(self.openFileDialog)

        # Create a dropdown menu for selecting output format
        self.formatLabel = QLabel("Select Output Format:", self)
        self.formatComboBox = QComboBox(self)
        self.video_formats = ["MP4", "AVI", "MOV", "MKV", "FLV", "WMV"]
        self.audio_formats = ["MP3", "OGG", "OPUS"]

        # Create a group box for media type selection
        self.mediaGroup = QGroupBox("Select Media Type", self)
        self.mediaLayout = QHBoxLayout()
        self.videoRadio = QRadioButton("Video", self)
        self.audioRadio = QRadioButton("Audio", self)
        self.videoRadio.setChecked(True)  # Default to video
        self.mediaLayout.addWidget(self.videoRadio)
        self.mediaLayout.addWidget(self.audioRadio)
        self.mediaGroup.setLayout(self.mediaLayout)
        self.videoRadio.toggled.connect(self.updateFormats)
        self.audioRadio.toggled.connect(self.updateFormats)

        # Create a convert button
        self.convertButton = QPushButton("Convert", self)
        self.convertButton.clicked.connect(self.convertFile)

        # Create a progress bar and status text area
        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.statusText = QTextEdit(self)
        self.statusText.setReadOnly(True)

        # Create a layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.selectButton)
        layout.addWidget(self.mediaGroup)
        layout.addWidget(self.formatLabel)
        layout.addWidget(self.formatComboBox)
        layout.addWidget(self.convertButton)
        layout.addWidget(self.progressBar)
        layout.addWidget(self.statusText)
        self.setLayout(layout)

        # Set up the main window
        self.setWindowTitle("File Converter")
        self.setGeometry(300, 300, 500, 300)  # x, y, width, height

        # Initialize selected file
        self.selected_file = None

        # Initialize formats
        self.updateFormats()

    def openFileDialog(self):
        # Open file dialog with all file types
        options = QFileDialog.Options()
        self.selected_file, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "All Files (*);;Video Files (*.mp4 *.avi *.mov *.mkv *.flv *.wmv);;Audio Files (*.mp3 *.ogg *.opus)",
            options=options
        )

        if self.selected_file:
            print(f"Selected file: {self.selected_file}")

    def updateFormats(self):
        if self.videoRadio.isChecked():
            self.formatComboBox.clear()
            self.formatComboBox.addItems(self.video_formats)
        elif self.audioRadio.isChecked():
            self.formatComboBox.clear()
            self.formatComboBox.addItems(self.audio_formats)

    def convertFile(self):
        if not self.selected_file:
            self.statusText.append("No file selected.")
            QMessageBox.warning(self, "No File", "No file was selected.")
            return

        # Determine whether video or audio is selected
        media_type = "video" if self.videoRadio.isChecked() else "audio"
        selected_format = self.formatComboBox.currentText().lower()
        output_file = f"{self.selected_file}.{selected_format}"

        # Build the FFmpeg command based on media type
        if media_type == "video":
            command = [
                "ffmpeg",
                "-i", self.selected_file,
                "-c:v", "libx264",
                "-preset", "slow",
                "-crf", "22",
                "-c:a", "aac",
                "-b:a", "192k",
                output_file
            ]
        else:  # audio
            if selected_format == "opus":
                codec = "libopus"
                command = [
                    "ffmpeg",
                    "-i", self.selected_file,
                    "-c:a", codec,
                    "-b:a", "64k",
                    output_file
                ]
            else:
                codec = "libmp3lame" if selected_format == "mp3" else "libvorbis"
                command = [
                    "ffmpeg",
                    "-i", self.selected_file,
                    "-c:a", codec,
                    "-b:a", "192k",
                    output_file
                ]

        # Print the command for debugging purposes
        print(f"Running command: {' '.join(command)}")

        # Update status text
        self.statusText.append(f"Starting conversion to {output_file}...")

        # Create and start the FFmpeg thread
        self.ffmpeg_thread = FFmpegThread(command)
        self.ffmpeg_thread.progress.connect(self.updateProgress)
        self.ffmpeg_thread.status_message.connect(self.updateStatus)
        self.ffmpeg_thread.finished.connect(self.onConversionFinished)
        self.ffmpeg_thread.start()

    def updateProgress(self, percentage):
        # Update progress bar with the percentage
        self.progressBar.setValue(percentage)

    def updateStatus(self, message):
        # Update status text
        self.statusText.append(message)

    def onConversionFinished(self, success):
        if success:
            self.statusText.append("Conversion completed successfully.")
        else:
            self.statusText.append("Conversion failed.")
        self.progressBar.setValue(100)

def main():
    app = QApplication(sys.argv)
    window = FileSelectorApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
