import sys
import wave
import simpleaudio as sa
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

import cv2
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication, QLineEdit, QPushButton, QFileDialog

# from ImageProcessor import ImageProcessor
from ImageReader import ImageReader


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setStyleSheet("background-color: rgb(255, 255, 204)")
        self.width = 640
        self.height = 900
        self.audio = []
        self.time_for_command = 10
        self.setFixedSize(self.width, self.height)
        # create the label that holds the image
        self.image_label = QLabel(self)
        # create a text label

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        font1 = QtGui.QFont("Roboto", 10)
        font2 = QtGui.QFont("Roboto", 16)
        self.edit1 = QLineEdit()
        self.edit2 = QLineEdit()
        self.edit3 = QLineEdit()
        self.edit4 = QLineEdit()
        self.edit_for_time = QLineEdit()
        self.output_filename = None
        self.edit1.setFixedWidth(250)
        self.edit2.setFixedWidth(250)
        self.edit3.setFixedWidth(250)
        self.edit4.setFixedWidth(250)
        self.edit_for_time.setFixedWidth(250)
        self.start_btn = QPushButton('Старт', self)
        self.start_btn.setFont(font2)
        self.start_btn.clicked.connect(self.start_clicked)
        self.load_button1 = QPushButton('Загрузить аудио-файлы', self)
        self.output_file_btn = QPushButton('Укажите файл для \n результатов', self)
        self.end_btn = QPushButton('Закончить работу и \n показать результаты', self)
        self.change_camera = QPushButton('Поменять камеру', self)
        self.end_btn.setGeometry(290, 580, 325, 80)
        self.load_button1.setGeometry(290, 660, 325, 80)
        self.output_file_btn.setGeometry(290, 740, 325, 80)
        self.change_camera.setGeometry(290, 820, 325, 80)
        self.start_btn.setStyleSheet('background-color: rgb(0,200,0);')
        self.end_btn.setStyleSheet('background: rgb(252,123,30);')
        self.load_button1.setStyleSheet('background: rgb(30,130,252);')
        self.output_file_btn.setStyleSheet('background: rgb(252,230,30);')
        self.change_camera.setStyleSheet('background: rgb(247, 77, 77);')
        self.end_btn.setFont(font2)
        self.load_button1.setFont(font2)
        self.output_file_btn.setFont(font2)
        self.change_camera.setFont(font2)
        self.end_btn.clicked.connect(self.finish_clicked)
        self.load_button1.clicked.connect(self.load_file1)
        self.output_file_btn.clicked.connect(self.output_file)
        self.change_camera.clicked.connect(self.change_camera_param)
        label1 = QLabel('Название первого предмета:')
        label2 = QLabel('Название второго предмета:')
        label3 = QLabel('Название третьего предмета:')
        label4 = QLabel('Название четвертого предмета:')
        label_for_time = QLabel('Время на выполнение команды:')
        label1.setFont(font1)
        label2.setFont(font1)
        label3.setFont(font1)
        label4.setFont(font1)
        label_for_time.setFont(font1)
        label1.setFixedWidth(250)
        label2.setFixedWidth(250)
        label3.setFixedWidth(250)
        label4.setFixedWidth(250)
        label_for_time.setFixedWidth(250)
        self.edit1.setFont(font1)
        self.edit2.setFont(font1)
        self.edit3.setFont(font1)
        self.edit4.setFont(font1)
        self.edit_for_time.setFont(font1)
        vbox.addWidget(self.start_btn)
        vbox.addWidget(self.image_label)
        vbox.addWidget(label1)
        vbox.addWidget(self.edit1)
        vbox.addWidget(label2)
        vbox.addWidget(self.edit2)
        vbox.addWidget(label3)
        vbox.addWidget(self.edit3)
        vbox.addWidget(label4)
        vbox.addWidget(self.edit4)
        vbox.addWidget(label_for_time)
        vbox.addWidget(self.edit_for_time)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)
        # create a grey pixmap
        grey = QPixmap(640, 520)
        grey.fill(QColor('darkGray'))
        # set the image image to the grey pixmap
        self.image_label.setPixmap(grey)
        self.reader = None
        self.camera_param = 1

        # self.processor = ImageProcessor()
        # self.reader = ImageReader(self, self.process_img, 0)

    def load_file1(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        self.filenames, _ = file_dialog.getOpenFileNames(self, 'Выберите файлы', '', '(*.wav)')

        if self.filenames:
            for filename in self.filenames:
                wave_obj = sa.WaveObject.from_wave_file(filename)
                self.audio.append(wave_obj)
        file_dialog.close()

    def change_camera_param(self):
        if self.camera_param == 1:
            self.camera_param = 0
        else:
            self.camera_param = 1

    def output_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        self.filename, _ = file_dialog.getOpenFileName(self, 'Выберите файл', '', '(*.txt)')

        if self.filename:
            self.output_filename = self.filename
        file_dialog.close()

    def start_clicked(self):
        if self.edit_for_time.text() != "":
            self.time_for_command = int(self.edit_for_time.text())
        self.reader = ImageReader(self, self.process_img, self.camera_param)
        self.reader.start()

    def finish_clicked(self):
        self.reader.stop()
        file = open(self.output_filename, 'a')
        date = self.get_date()
        file.write(str(int(self.reader.points * 100 / self.reader.total_attempts)) + " " + str(date) + "\n")
        file.flush()
        self.graphic()
        file.close()

    @staticmethod
    def get_date():
        current_datetime = str(datetime.now()).split(" ")[0].split("-")
        curr = current_datetime[2] + "." + current_datetime[1] + "." + current_datetime[0][2::]
        return curr

    def graphic(self):
        file = open(self.output_filename, 'r')
        x = list()
        y = list()
        for line in file:
            s = line.split(" ")
            x.append(s[1])
            y.append(int(s[0]))
        file.close()
        plt.figure(figsize=(8, 6))
        plt.text(2, 90, "Текущий результат: " + str(y[-1]) + "%" + "\n" + "График прогресса:")
        plt.plot(x, y)
        plt.axis([x[0], x[-1], 0, 100])
        plt.xlabel('Дата измерения')
        plt.ylabel('Процент удачно выполненных заданий')
        plt.scatter(x, y, s=50, color='red')
        plt.show()

    def process_img(self, img):
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # self.processor.process(rgb_image)
        pix_map = self.convert_cv_qt(rgb_image)
        self.image_label.setPixmap(pix_map)

    def convert_cv_qt(self, cv_img):
        pass
        h, w, ch = cv_img.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(cv_img.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.width, self.height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.reader.stop()
        super().closeEvent(a0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
