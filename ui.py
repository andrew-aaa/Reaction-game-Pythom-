import sys
import configparser
from pathlib import Path

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QMessageBox)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Reaction")
        self.setFixedSize(600, 400)

        button1 = QPushButton("Play")
        button1.setFixedSize(240, 60)
        button1.clicked.connect(self.start_game)

        button2 = QPushButton("Records")
        button2.setFixedSize(240, 60)
        button2.clicked.connect(self.open_window_records)

        button3 = QPushButton("Settings")
        button3.setFixedSize(240, 60)
        button3.clicked.connect(self.open_window_settings)

        button4 = QPushButton("Exit")
        button4.setFixedSize(240, 60)
        button4.clicked.connect(self.close)
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button4)
        layout.setSpacing(20)

        central_widget.setLayout(layout)

        with open('styles/styles_main.qss') as f:
            style_sheet = f.read()
        self.setStyleSheet(style_sheet)

    def start_game(self):    
        from game import run_game
        run_game()

    def open_window_records(self):
        pass

    def open_window_settings(self):
        self.hide()
        self.settings_window = SettingsWindow()
        self.settings_window.show()
        self.settings_window.closed.connect(self.show)


class RecordsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Reaction")
        self.setFixedSize(600, 400)

        self.button_back = QPushButton()
        self.button_back.clicked.connect(self.return_to_main)

        container = QWidget()
        container.setLayout(self.button_back)

        self.setCentralWidget(container)

    def return_to_main(self):
        pass


class SettingsWindow(QMainWindow):
    closed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setFixedSize(600, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.slider_1_label = QLabel("Target size:")
        self.slider_1_value = QLabel("10")
        self.slider_1 = QSlider(Qt.Orientation.Horizontal)
        self.slider_1.setRange(10, 100)
        self.slider_1.valueChanged.connect(lambda value: self.slider_1_value.setText(str(value)))

        self.slider_2_label = QLabel("Number of targets:")
        self.slider_2_value = QLabel("10")
        self.slider_2 = QSlider(Qt.Orientation.Horizontal)
        self.slider_2.setRange(10, 100)
        self.slider_2.valueChanged.connect(lambda value: self.slider_2_value.setText(str(value)))

        self.slider_3_label = QLabel("Delay time:")
        self.slider_3_value = QLabel("0")
        self.slider_3 = QSlider(Qt.Orientation.Horizontal)
        self.slider_3.setRange(0, 5)
        self.slider_3.valueChanged.connect(lambda value: self.slider_3_value.setText(str(value)))

        hbox_slider_1 = QHBoxLayout()
        hbox_slider_1.addWidget(self.slider_1_label)
        hbox_slider_1.addStretch()
        hbox_slider_1.addWidget(self.slider_1_value)
        hbox_slider_1.addWidget(self.slider_1)

        hbox_slider_2 = QHBoxLayout()
        hbox_slider_2.addWidget(self.slider_2_label)
        hbox_slider_2.addStretch()
        hbox_slider_2.addWidget(self.slider_2_value)
        hbox_slider_2.addWidget(self.slider_2)

        hbox_slider_3 = QHBoxLayout()
        hbox_slider_3.addWidget(self.slider_3_label)
        hbox_slider_3.addStretch()
        hbox_slider_3.addWidget(self.slider_3_value)
        hbox_slider_3.addWidget(self.slider_3)

        main_layout.addLayout(hbox_slider_1)
        main_layout.addStretch()
        main_layout.addLayout(hbox_slider_2)
        main_layout.addStretch()
        main_layout.addLayout(hbox_slider_3)

        button_1 = QPushButton("Save")
        button_1.setFixedSize(240, 60)
        button_1.clicked.connect(self.save_settings)

        button_2 = QPushButton("Back")
        button_2.setFixedSize(240, 60)
        button_2.clicked.connect(self.close)

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addStretch()
        hbox_buttons.addWidget(button_1)
        hbox_buttons.addWidget(button_2)
        hbox_buttons.addStretch()

        main_layout.addStretch()
        main_layout.addLayout(hbox_buttons)

        central_widget.setLayout(main_layout)

        with open('styles/styles_settings.qss') as f:
            style_sheet = f.read()
        self.setStyleSheet(style_sheet)

    def save_settings(self):
        values = {
            'size': int(self.slider_1.value()),
            'number': int(self.slider_2.value()),
            'time': int(self.slider_3.value())
        }

        current_dir = Path(__file__).parent.resolve()
        settings_file_path = current_dir / 'settings_for_game.ini'

        config = configparser.ConfigParser()
        config['DEFAULT'] = values

        with open(settings_file_path, 'w') as configfile:
            config.write(configfile)

        QMessageBox.information(
            self,
            "Success",
            "Settings saved successfully!"
        )

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()
