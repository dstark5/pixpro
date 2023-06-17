import os
import sys
import threading
import time

import cv2
import numpy
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QRubberBand, QPushButton, QStackedWidget,QSlider, QFileDialog, QComboBox, QProgressBar
from PyQt5 import QtCore, QtGui
import shutil,random,dlib,atexit,pymsgbox,multiprocessing
import scipy.spatial as spatial



class window(QWidget):
    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(200, 100, 1591, 891)
        self.setWindowTitle("   PixPro")
        self.setWindowIcon(QtGui.QIcon("icons/pixpro.ico"))
        self.currentImage = "icons/default.jpg"
        self.image_save=None
        self.usr_path = (os.path.expanduser("~"))
        self.res = 1
        self.setFixedWidth(1591)
        self.stackedwidgets = QStackedWidget(self)
        self.stackedwidgets.setGeometry(0, 0, 1591, 1151)


        self.__ui__()
        self.ui_crop()
        self.ui_brightness()
        self.ui_contrast()
        self.ui_autoadjust()
        self.ui_sketch()
        self.ui_cartoon()
        self.ui_flip()
        self.ui_rotate()
        self.ui_blur()
        self.ui_BW()
        self.ui_color_invert()
        self.ui_enhance()
        self.ui_resize()
        self.ui_ai()
        self.ui_file()

        self.stackedwidgets.setCurrentIndex(15)

    def __ui__(self):
        self.widget = QWidget()
        self.widget.setGeometry(0, 0, 2135, 1551)
        self.image = cv2.imread(self.currentImage)
        frame_width, frame_height, left_margin, top_margin = self.resolution(self.image)

        self.label = QLabel(self.widget)
        self.pix = QtGui.QPixmap(self.currentImage)
        self.label.setPixmap(self.pix)
        self.label.setScaledContents(True)
        self.label.setFixedSize(int(frame_width), int(frame_height))
        self.label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

        self.iconbutton(self.widget, "icons/crop.svg", 1281, 50, 54, 54, "Crop", self.change_ui)
        self.iconbutton(self.widget, "icons/brightness.png", 1281, 150, 54, 54, "Brightness", self.change_ui_brightness)
        self.iconbutton(self.widget, "icons/contrast.png", 1281, 250, 54, 54, "Contrast", self.change_ui_contrast)
        self.iconbutton(self.widget, "icons/adjust.svg", 1281, 350, 54, 54, "Auto adjust", self.change_ui_autoadjust)
        self.iconbutton(self.widget, "icons/sketch.png", 1281, 450, 54, 54, "Sketch Effect", self.change_ui_sketch)
        self.iconbutton(self.widget, "icons/cartoon.png", 1281, 550, 54, 54, "Cartoon Effect", self.change_ui_cartoon)
        self.iconbutton(self.widget, "icons/ai.png", 1281, 650, 54, 54, "AI", self.change_ui_ai)
        self.iconbutton(self.widget, "icons/enhance.png", 1391, 50, 54, 54, "Enhance", self.change_ui_enhance)
        self.iconbutton(self.widget, "icons/flip.png", 1391, 150, 54, 54, "Flip", self.change_ui_flip)
        self.iconbutton(self.widget, "icons/rotate.png", 1391, 250, 54, 54, "Rotate", self.change_ui_rotate)
        self.iconbutton(self.widget, "icons/blur.png", 1391, 350, 54, 54, "Blur", self.change_ui_blur)
        self.iconbutton(self.widget, "icons/black-and-white.png", 1391, 450, 54, 54, "Black & White", self.change_ui_bw)
        self.iconbutton(self.widget, "icons/invert.png", 1391, 550, 54, 54, "invert", self.change_ui_colorInvert)
        self.iconbutton(self.widget, "icons/resize.png", 1391, 650, 54, 54, "Compress", self.change_ui_resize)


        button=QPushButton(self.widget)
        button.setGeometry(1281,750,179,54)
        button.setStyleSheet("QPushButton{border-radius:25px;font-weight:bold;background-color:black;color:white;} QPushButton::hover{background-color:white;color:black;border:1px solid black;}")
        button.setText("save")
        button.clicked.connect(self.file_save)

        self.stackedwidgets.addWidget(self.widget)

    def change_ui(self):
        self.stackedwidgets.setCurrentIndex(1)

    def change_ui_brightness(self):
        self.stackedwidgets.setCurrentIndex(2)

    def change_ui_contrast(self):
        self.stackedwidgets.setCurrentIndex(3)

    def change_ui_autoadjust(self):
        self.stackedwidgets.setCurrentIndex(4)

    def change_ui_sketch(self):
        self.stackedwidgets.setCurrentIndex(5)

    def change_ui_cartoon(self):
        self.stackedwidgets.setCurrentIndex(6)

    def change_ui_flip(self):
        self.stackedwidgets.setCurrentIndex(7)

    def change_ui_rotate(self):
        self.stackedwidgets.setCurrentIndex(8)

    def change_ui_blur(self):
        self.stackedwidgets.setCurrentIndex(9)

    def change_ui_bw(self):
        self.stackedwidgets.setCurrentIndex(10)

    def change_ui_colorInvert(self):
        self.stackedwidgets.setCurrentIndex(11)

    def change_ui_enhance(self):
        self.stackedwidgets.setCurrentIndex(12)

    def change_ui_resize(self):
        self.stackedwidgets.setCurrentIndex(13)

    def change_ui_ai(self):
        self.stackedwidgets.setCurrentIndex(14)




    def ui_crop(self):
        self.crop = QWidget()
        self.crop.setGeometry(0, 0, 2135, 1551)
        self.image = cv2.imread(self.currentImage)
        frame_width, frame_height, left_margin, top_margin = self.resolution(self.image)

        self.crop_label = Qlabel(self.crop)

        self.crop_pix = QtGui.QPixmap(self.currentImage).scaled(int(frame_width), int(frame_height), QtCore.Qt.KeepAspectRatio)
        self.crop_label.setPixmap(self.crop_pix)
        self.crop_label.setScaledContents(True)
        self.crop_label.setFixedSize(int(frame_width), int(frame_height))
        self.crop_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))
        self.path=(self.usr_path+ "/.PixPro/")

        def checked():
            img = cv2.imread(self.currentImage)
            x = self.crop_label.getpos()
            if x:
                img = img[int(x[1] * self.res):int((x[3] + x[1]) * self.res),int(x[0] * self.res):int((x[2] + x[0]) * self.res)]
                cv2.imwrite(self.path+"crop.jpg", img)

                image = cv2.imread(self.path+"crop.jpg")
                frame_width, frame_height, left_margin, top_margin = self.resolution(image)
                self.crop_pix = QtGui.QPixmap(self.path+"crop.jpg").scaled(int(frame_width), int(frame_height),QtCore.Qt.KeepAspectRatio)
                self.crop_label.setPixmap(self.crop_pix)
                self.crop_label.setScaledContents(True)
                self.crop_label.setFixedSize(frame_width, frame_height)
                self.crop_label.setGeometry(left_margin, top_margin, frame_width, frame_height)
                self.crop_label.hiderubberband(True)
                self.currentImage = self.path+"crop.jpg"
                self.lable_update_thread()

        def cancel():
            self.crop_label.hiderubberband(True)

        def back():
            self.stackedwidgets.setCurrentIndex(0)

        def info():
            pymsgbox.alert("Click and drag on the image to crop")

        self.iconbutton(self.crop, "icons/back.svg", 1, 1, 53, 53, "Back", back)
        self.iconbutton(self.crop, "icons/checked.png", 1391, 715, 53, 53, "save", checked)
        self.iconbutton(self.crop, "icons/cancel.png", 1491, 715, 53, 53, "cancel", cancel)
        self.iconbutton(self.crop, "icons/info.png", 1521, 5, 53, 53, "info", info,25)

        self.stackedwidgets.addWidget(self.crop)

    def ui_brightness(self):
        self.ui = QWidget()
        self.ui.setGeometry(0, 0, 2135, 1551)

        self.image = cv2.imread(self.currentImage)
        frame_width, frame_height, left_margin, top_margin = self.resolution(self.image)

        self.ui_label = QLabel(self.ui)
        self.ui_pix = QtGui.QPixmap(self.currentImage)
        self.ui_label.setPixmap(self.ui_pix)
        self.ui_label.setScaledContents(True)
        self.ui_label.setFixedSize(int(frame_width), int(frame_height))
        self.ui_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

        def sliderx(x):
            time.sleep(0.1)
            Image_cv2.brightness(self.image, x)
            #img = QtGui.QImage(im.data, im.shape[1], im.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.ui_pix = QtGui.QPixmap(self.path+"Brightned_image.jpg")
            self.ui_label.setPixmap(self.ui_pix)


        self.slider = QSlider(self.ui)
        self.slider.setGeometry(50, 795, 550, 15)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(450)
        self.slider.setValue(255)
        self.slider.setStyleSheet("*::handle:horizontal{background-color:red;border:1px solid red;border-radius:7px;}") # "*::groove:horizontal{border-radius:5px;}"+"*::add-page:horizontal{background-color:black;}"+"*::sub-page:horizontal{background-color:red;}"
        self.slider.valueChanged.connect(sliderx)
        def back():
            self.stackedwidgets.setCurrentIndex(0)

        def checked():
            if os.path.isfile(self.path+"Brightned_image.jpg"):
                self.currentImage = self.path+"Brightned_image.jpg"
                self.lable_update_thread()

        def cancel():
            self.slider.setValue(255)


        self.iconbutton(self.ui, "icons/back.svg", 1, 1, 53, 53, "Back", back)
        self.iconbutton(self.ui, "icons/checked.png", 1291, 715, 53, 53, "save", checked)
        self.iconbutton(self.ui, "icons/cancel.png", 1391, 715, 53, 53, "cancel", cancel)

        self.stackedwidgets.addWidget(self.ui)

    def ui_contrast(self):
        self.contrast_ui = QWidget()
        self.contrast_ui.setGeometry(0, 0, 2135, 1551)

        self.image = cv2.imread(self.currentImage)
        frame_width, frame_height, left_margin, top_margin = self.resolution(self.image)

        self.contrast_label = QLabel(self.contrast_ui)
        self.contrast_pix = QtGui.QPixmap(self.currentImage)
        self.contrast_label.setPixmap(self.contrast_pix)
        self.contrast_label.setScaledContents(True)
        self.contrast_label.setFixedSize(int(frame_width), int(frame_height))
        self.contrast_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

        def sliderx(x):
            time.sleep(0.1)
            Image_cv2.contrast(self.image, x)
            self.contrast_pix = QtGui.QPixmap(self.path+"contrast_image.jpg")
            self.contrast_label.setPixmap(self.contrast_pix)

        self.contrast_slider = QSlider(self.contrast_ui)
        self.contrast_slider.setGeometry(50, 795, 550, 15)
        self.contrast_slider.setOrientation(QtCore.Qt.Horizontal)
        self.contrast_slider.setMinimum(1)
        self.contrast_slider.setMaximum(127)
        self.contrast_slider.setValue(5)
        self.contrast_slider.setStyleSheet(
            "*::handle:horizontal{background-color:red;border:1px solid red;border-radius:7px;}")  # "*::groove:horizontal{border-radius:5px;}"+"*::add-page:horizontal{background-color:black;}"+"*::sub-page:horizontal{background-color:red;}"
        self.contrast_slider.valueChanged.connect(sliderx)

        def back():
            self.stackedwidgets.setCurrentIndex(0)

        def checked():
            if os.path.isfile(self.path+"contrast_image.jpg"):
                self.currentImage = self.path+"contrast_image.jpg"
                self.lable_update_thread()

        def cancel():
            self.contrast_slider.setValue(1)


        self.iconbutton(self.contrast_ui,"icons/back.svg" , 1, 1, 53, 53, "Back", back)
        self.iconbutton(self.contrast_ui, "icons/checked.png", 1291, 715, 53, 53, "save", checked)
        self.iconbutton(self.contrast_ui, "icons/cancel.png", 1391, 715, 53, 53, "cancel", cancel)

        self.stackedwidgets.addWidget(self.contrast_ui)

    def ui_sketch(self):
        self.sketch = QWidget()
        self.sketch.setGeometry(0, 0, 2135, 1551)

        self.image = cv2.imread(self.currentImage)
        frame_width, frame_height, left_margin, top_margin = self.resolution(self.image)

        self.s_label = QLabel(self.sketch)
        self.s_pix = QtGui.QPixmap(self.currentImage)
        self.s_label.setPixmap(self.s_pix)
        self.s_label.setScaledContents(True)
        self.s_label.setFixedSize(int(frame_width), int(frame_height))
        self.s_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

        def sketch_():
            Image_cv2.sketch(self.image)
            self.s_pix = QtGui.QPixmap(self.path+"sketch_image.jpg")
            self.s_label.setPixmap(self.s_pix)

        def pencil_sketch():
            Image_cv2.pencil_sketch(self.image)
            self.s_pix = QtGui.QPixmap(self.path+"sketch_image.jpg")
            self.s_label.setPixmap(self.s_pix)

        def sketch_thread():
            thread=threading.Thread(target=pencil_sketch)
            thread.daemon=True
            thread.start()


        button_ = QPushButton(self.sketch)
        button_.setGeometry(1281,150,179,54)
        button_.setText("sketch")
        button_.setStyleSheet("QPushButton{border-radius:25px;font-weight:bold;background-color:black;color:white;} QPushButton::hover{background-color:white;color:black;border:1px solid black;}")
        button_.clicked.connect(sketch_)

        button = QPushButton(self.sketch)
        button.setGeometry(1281, 250, 179, 54)
        button.setText("Pencil sketch")
        button.setStyleSheet("QPushButton{border-radius:25px;font-weight:bold;background-color:black;color:white;} QPushButton::hover{background-color:white;color:black;border:1px solid black;}")
        button.clicked.connect(sketch_thread)

        def back():
            self.stackedwidgets.setCurrentIndex(0)

        def checked():
            if os.path.isfile(self.path+"sketch_image.jpg"):
                self.currentImage = self.path+"sketch_image.jpg"
                self.lable_update_thread()

        def cancel():
            self.s_pix = QtGui.QPixmap(self.currentImage)
            self.s_label.setPixmap(self.s_pix)

        self.iconbutton(self.sketch, "icons/back.svg", 1, 1, 53, 53, "Back", back)
        self.iconbutton(self.sketch, "icons/checked.png", 1291, 715, 53, 53, "save", checked)
        self.iconbutton(self.sketch, "icons/cancel.png", 1391, 715, 53, 53, "cancel", cancel)

        self.stackedwidgets.addWidget(self.sketch)

    def ui_cartoon(self):
        self.cartoon = QWidget()
        self.cartoon.setGeometry(0, 0, 2135, 1551)

        self.image = cv2.imread(self.currentImage)
        frame_width, frame_height, left_margin, top_margin = self.resolution(self.image)

        self.cartoon_label = QLabel(self.cartoon)
        self.cartoon_pix = QtGui.QPixmap(self.currentImage)
        self.cartoon_label.setPixmap(self.cartoon_pix)
        self.cartoon_label.setScaledContents(True)
        self.cartoon_label.setFixedSize(int(frame_width), int(frame_height))
        self.cartoon_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

        self.cartoon_probar=QProgressBar(self.cartoon)
        self.cartoon_probar.setGeometry(1191,350,350,19)
        self.cartoon_probar.setAlignment(QtCore.Qt.AlignCenter)
        self.cartoon_probar.setStyleSheet("QProgressBar{border:1px solid white;border-radius:9px;font-weight:bold;} QProgressBar::chunk{border-radius:7px;background-color:qlineargradient(x1:0 y1:0,x2:1 y2:1,stop:0 red,stop:1 #fc00ff);}")
        self.cartoon_probar.hide()

        self.cartoon_prolable=QLabel(self.cartoon)
        self.cartoon_prolable.setGeometry(1295,395,350,19)
        self.cartoon_prolable.setText("# Processing")
        self.cartoon_prolable.setStyleSheet("font-weight:bold;")
        self.cartoon_prolable.hide()

        def cartoon_():
            self.cartoon_probar.show()
            self.cartoon_prolable.show()
            self.button_.setEnabled(False)
            self.cartoon_probar.setValue(5)
            time.sleep(0.1)
            self.cartoon_probar.setValue(50)
            Image_cv2.cartoon_effect(self.image)
            self.cartoon_probar.setValue(75)
            time.sleep(0.1)
            self.cartoon_probar.setValue(95)
            time.sleep(0.1)
            self.cartoon_probar.hide()
            self.cartoon_prolable.hide()
            self.button_.setEnabled(True)
            self.cartoon_pix = QtGui.QPixmap(self.path+"cartoon_image.jpg")
            self.cartoon_label.setPixmap(self.cartoon_pix)

        def cartoon_thread():
            thread=threading.Thread(target=cartoon_)
            thread.daemon=True
            thread.start()


        self.button_ = QPushButton(self.cartoon)
        self.button_.setGeometry(1291,150,179,54)
        self.button_.setText("cartoon")
        self.button_.setStyleSheet("QPushButton{border-radius:25px;font-weight:bold;background-color:black;color:white;} QPushButton::hover{background-color:white;color:black;border:1px solid black;}")
        self.button_.clicked.connect(cartoon_thread)

        def back():
            self.stackedwidgets.setCurrentIndex(0)

        def checked():
            if os.path.isfile(self.path+"cartoon_image.jpg"):
                self.currentImage = self.path+"cartoon_image.jpg"
                self.lable_update_thread()

        def cancel():
            self.cartoon_pix = QtGui.QPixmap(self.currentImage)
            self.cartoon_label.setPixmap(self.cartoon_pix)

        self.iconbutton(self.cartoon, "icons/back.svg", 1, 1, 53, 53, "Back", back)
        self.iconbutton(self.cartoon, "icons/checked.png", 1291, 715, 53, 53, "save", checked)
        self.iconbutton(self.cartoon, "icons/cancel.png", 1391, 715, 53, 53, "cancel", cancel)

        self.stackedwidgets.addWidget(self.cartoon)

    def ui_autoadjust(self):
        self.ui_ = QWidget()
        self.ui_.setGeometry(0, 0, 2135, 1551)

        self.image = cv2.imread(self.currentImage)
        frame_width, frame_height, left_margin, top_margin = self.resolution(self.image)

        self.ad_label = QLabel(self.ui_)
        self.ad_pix = QtGui.QPixmap(self.currentImage)
        self.ad_label.setPixmap(self.ad_pix)
        self.ad_label.setScaledContents(True)
        self.ad_label.setFixedSize(int(frame_width), int(frame_height))
        self.ad_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

        self.ad_probar = QProgressBar(self.ui_)
        self.ad_probar.setGeometry(1191, 350, 350, 19)
        self.ad_probar.setAlignment(QtCore.Qt.AlignCenter)
        self.ad_probar.setStyleSheet(
            "QProgressBar{border:1px solid white;border-radius:9px;font-weight:bold;} QProgressBar::chunk{border-radius:7px;background-color:qlineargradient(x1:0 y1:0,x2:1 y2:1,stop:0 red,stop:1 #fc00ff);}")
        self.ad_probar.hide()

        self.ad_prolable = QLabel(self.ui_)
        self.ad_prolable.setGeometry(1295, 395, 350, 19)
        self.ad_prolable.setText("# Denoising")
        self.ad_prolable.setStyleSheet("font-weight:bold;")
        self.ad_prolable.hide()

        def autoadjust_():
            Image_cv2.auto_BrightContrast(self.image)
            self.ad_pix = QtGui.QPixmap(self.path+"adjusted_image.jpg")
            self.ad_label.setPixmap(self.ad_pix)

        def denoise_():
            self.ad_probar.show()
            self.ad_prolable.show()
            self.ad_probar.setValue(5)
            time.sleep(0.1)
            self.ad_probar.setValue(50)
            Image_cv2.denoiser(self.image)
            self.ad_probar.setValue(75)
            time.sleep(0.1)
            self.ad_probar.setValue(95)
            time.sleep(0.1)
            self.ad_probar.hide()
            self.ad_prolable.hide()
            self.ad_pix = QtGui.QPixmap(self.path+"adjusted_image.jpg")
            self.ad_label.setPixmap(self.ad_pix)

        button_ = QPushButton(self.ui_)
        button_.setGeometry(1295,150,255,54)
        button_.setText("auto Brightness & Contrast")
        button_.setStyleSheet("QPushButton{border-radius:25px;font-weight:bold;background-color:black;color:white;} QPushButton::hover{background-color:white;color:black;border:1px solid black;}")
        button_.clicked.connect(autoadjust_)

        button = QPushButton(self.ui_)
        button.setGeometry(1325,250,179,54)
        button.setText("Denoise")
        button.setStyleSheet("QPushButton{border-radius:25px;font-weight:bold;background-color:black;color:white;} QPushButton::hover{background-color:white;color:black;border:1px solid black;}")
        button.clicked.connect(denoise_)


        def back():
            self.stackedwidgets.setCurrentIndex(0)

        def checked():
            if os.path.isfile(self.path+"adjusted_image.jpg"):
                self.currentImage = self.path+"adjusted_image.jpg"
                self.lable_update_thread()

        def cancel():
            self.ad_pix = QtGui.QPixmap(self.currentImage)
            self.ad_label.setPixmap(self.ad_pix)

        self.iconbutton(self.ui_, "icons/back.svg", 1, 1, 53, 53, "Back", back)
        self.iconbutton(self.ui_, "icons/checked.png", 1291, 715, 53, 53, "save", checked)
        self.iconbutton(self.ui_, "icons/cancel.png", 1391, 715, 53, 53, "cancel", cancel)

        self.stackedwidgets.addWidget(self.ui_)

    def ui_enhance(self):
        self.enhance = QWidget()
        self.enhance.setGeometry(0, 0, 2135, 1551)

        self.image = cv2.imread(self.currentImage)
        frame_width, frame_height, left_margin, top_margin = self.resolution(self.image)

        self.en_label = QLabel(self.enhance)
        self.en_pix = QtGui.QPixmap(self.currentImage)
        self.en_label.setPixmap(self.en_pix)
        self.en_label.setScaledContents(True)
        self.en_label.setFixedSize(int(frame_width), int(frame_height))
        self.en_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

        self.probar = QProgressBar(self.enhance)
        self.probar.setGeometry(1191, 750, 350, 19)
        self.probar.setAlignment(QtCore.Qt.AlignCenter)
        self.probar.setStyleSheet(
            "QProgressBar{border:1px solid white;border-radius:9px;font-weight:bold;} QProgressBar::chunk{border-radius:7px;background-color:qlineargradient(x1:0 y1:0,x2:1 y2:1,stop:0 red,stop:1 #fc00ff);}")
        self.probar.hide()
        self.prolable = QLabel(self.enhance)
        self.prolable.setGeometry(1295, 795, 350, 19)
        self.prolable.setText("# Rendering")
        self.prolable.setStyleSheet("font-weight:bold;")
        self.prolable.hide()

        def probar(x=0):
            if x == 1:
                self.probar.show()
                self.prolable.show()
                self.probar.setValue(5)
                time.sleep(0.1)
                self.probar.setValue(50)
            else:
                self.probar.setValue(75)
                time.sleep(0.5)
                self.probar.setValue(95)
                time.sleep(0.1)
                self.probar.hide()
                self.prolable.hide()
        def button_(x):
            if x==True:
                self.button_2x.setEnabled(True)
                self.button_3x.setEnabled(True)
                self.button_4x.setEnabled(True)
            else:
                self.button_2x.setEnabled(False)
                self.button_3x.setEnabled(False)
                self.button_4x.setEnabled(False)

        def enhance_2x():
            probar(1)
            button_(False)
            Image_cv2.enhance(self.image, 2)
            probar()
            button_(True)
            self.en_pix = QtGui.QPixmap(self.path+"enhanced_image.jpg")
            self.en_label.setPixmap(self.en_pix)
            self.currentImage = self.path+"enhanced_image.jpg"
            self.lable_update_thread()

        def enhance_3x():
            probar(1)
            button_(False)
            Image_cv2.enhance(self.image, 3)
            probar()
            button_(True)
            self.en_pix = QtGui.QPixmap(self.path+"enhanced_image.jpg")
            self.en_label.setPixmap(self.en_pix)
            self.currentImage = self.path+"enhanced_image.jpg"
            self.lable_update_thread()

        def enhance_4x():
            probar(1)
            button_(False)
            Image_cv2.enhance(self.image, 4)
            probar()
            button_(True)
            self.en_pix = QtGui.QPixmap(self.path+"enhanced_image.jpg")
            self.en_label.setPixmap(self.en_pix)
            self.currentImage = self.path+"enhanced_image.jpg"
            self.lable_update_thread()

        def thread_2x():
            thread=threading.Thread(target=enhance_2x)
            thread.daemon=True
            thread.start()
        def thread_3x():
            thread=threading.Thread(target=enhance_3x)
            thread.daemon=True
            thread.start()
        def thread_4x():
            thread=threading.Thread(target=enhance_4x)
            thread.daemon=True
            thread.start()

        self.button_2x = QPushButton(self.enhance)
        self.button_2x.setGeometry(1281,150,179,54)
        self.button_2x.setText("enhance_2x")
        self.button_2x.setStyleSheet("QPushButton{border-radius:25px;font-weight:bold;background-color:black;color:white;} QPushButton::hover{background-color:white;color:black;border:1px solid black;}")
        self.button_2x.clicked.connect(thread_2x)

        self.button_3x = QPushButton(self.enhance)
        self.button_3x.setGeometry(1281, 250, 179, 54)
        self.button_3x.setText("enhance_3x")
        self.button_3x.setStyleSheet("QPushButton{border-radius:25px;font-weight:bold;background-color:black;color:white;} QPushButton::hover{background-color:white;color:black;border:1px solid black;}")
        self.button_3x.clicked.connect(thread_3x)

        self.button_4x = QPushButton(self.enhance)
        self.button_4x.setGeometry(1281,350,179,54)
        self.button_4x.setText("enhance_4x")
        self.button_4x.setStyleSheet("QPushButton{border-radius:25px;font-weight:bold;background-color:black;color:white;} QPushButton::hover{background-color:white;color:black;border:1px solid black;}")
        self.button_4x.clicked.connect(thread_4x)

        def back():
            self.lable_update_thread()
            self.stackedwidgets.setCurrentIndex(0)

        self.iconbutton(self.enhance, "icons/back.svg", 1, 1, 53, 53, "Back", back)

        self.stackedwidgets.addWidget(self.enhance)

    def ui_flip(self):
        self.flip = QWidget()
        self.flip.setGeometry(0, 0, 2135, 1551)

        self.image = cv2.imread(self.currentImage)
        frame_width, frame_height, left_margin, top_margin = self.resolution(self.image)

        self.flip_label = QLabel(self.flip)
        self.flip_pix = QtGui.QPixmap(self.currentImage)
        self.flip_label.setPixmap(self.flip_pix)
        self.flip_label.setScaledContents(True)
        self.flip_label.setFixedSize(int(frame_width), int(frame_height))
        self.flip_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

        def flip_():
            Image_cv2.flip(self.image)
            self.flip_pix = QtGui.QPixmap(self.path+"fliped_image.jpg")
            self.flip_label.setPixmap(self.flip_pix)

        def Hflip_():
            Image_cv2.flip(self.image, 0)
            self.flip_pix = QtGui.QPixmap(self.path+"fliped_image.jpg")
            self.flip_label.setPixmap(self.flip_pix)

        def back():
            self.stackedwidgets.setCurrentIndex(0)

        def checked():
            if os.path.isfile(self.path+"fliped_image.jpg"):
                self.currentImage = self.path+"fliped_image.jpg"
                self.lable_update_thread()

        def cancel():
            self.flip_pix = QtGui.QPixmap(self.currentImage)
            self.flip_label.setPixmap(self.flip_pix)

        self.iconbutton(self.flip, "icons/back.svg", 1, 1, 53, 53, "Back", back)
        self.iconbutton(self.flip, "icons/checked.png", 1291, 715, 53, 53, "save", checked)
        self.iconbutton(self.flip, "icons/cancel.png", 1391, 715, 53, 53, "cancel", cancel)
        self.iconbutton(self.flip, "icons/flip.png", 1381,150,53,53, "Horizontal-flip", Hflip_)
        self.iconbutton(self.flip, "icons/horizontal-flip.png", 1381,250,53,53, "Vertical-flip", flip_)

        self.stackedwidgets.addWidget(self.flip)

    def ui_rotate(self):
        self.rotate = QWidget()
        self.rotate.setGeometry(0, 0, 2135, 1551)

        self.image = cv2.imread(self.currentImage)
        frame_width, frame_height, left_margin, top_margin = self.resolution(self.image)

        self.rotate_label = QLabel(self.rotate)
        self.rotate_pix = QtGui.QPixmap(self.currentImage)
        self.rotate_label.setPixmap(self.rotate_pix)
        self.rotate_label.setScaledContents(True)
        self.rotate_label.setFixedSize(int(frame_width), int(frame_height))
        self.rotate_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

        self.clicked = 0

        def rotate_():
            Image_cv2.rotate(self.image, self.clicked)

            frame_width, frame_height, left_margin, top_margin = self.resolution(cv2.imread(self.path+"rotated_image.jpg"))

            self.rotate_pix = QtGui.QPixmap(self.path+"rotated_image.jpg")
            self.rotate_label.setPixmap(self.rotate_pix)
            self.rotate_label.setScaledContents(True)
            self.rotate_label.setFixedSize(int(frame_width), int(frame_height))
            self.rotate_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))
            self.clicked += 1


        def back():
            self.stackedwidgets.setCurrentIndex(0)

        def checked():
            if os.path.isfile(self.path+"rotated_image.jpg"):
                self.currentImage = self.path+"rotated_image.jpg"
                self.lable_update_thread()

        def cancel():
            frame_width, frame_height, left_margin, top_margin = self.resolution(self.image)
            self.rotate_pix = QtGui.QPixmap(self.currentImage)
            self.rotate_label.setPixmap(self.rotate_pix)
            self.rotate_label.setScaledContents(True)
            self.rotate_label.setFixedSize(int(frame_width), int(frame_height))
            self.rotate_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))
            self.clicked = 0


        self.iconbutton(self.rotate, "icons/back.svg", 1, 1, 53, 53, "Back", back)
        self.iconbutton(self.rotate, "icons/checked.png", 1291, 715, 53, 53, "save", checked)
        self.iconbutton(self.rotate, "icons/cancel.png", 1391, 715, 53, 53, "cancel", cancel)
        self.iconbutton(self.rotate, "icons/rotate.png", 1381,150, 53, 53, "rotate", rotate_)

        self.stackedwidgets.addWidget(self.rotate)

    def ui_blur(self):
        self.blur = QWidget()
        self.blur.setGeometry(0, 0, 2135, 1551)

        self.image = cv2.imread(self.currentImage)
        frame_width, frame_height, left_margin, top_margin = self.resolution(self.image)

        self.blur_label = QLabel(self.blur)
        self.blur_pix = QtGui.QPixmap(self.currentImage)
        self.blur_label.setPixmap(self.blur_pix)
        self.blur_label.setScaledContents(True)
        self.blur_label.setFixedSize(int(frame_width), int(frame_height))
        self.blur_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

        def sliderx(blur):
            if blur % 2 != 0:
                Image_cv2.blur(self.image, blur)
            else:
                Image_cv2.blur(self.image, blur+1)
            self.blur_pix = QtGui.QPixmap(self.path+"Blured_image.jpg")
            self.blur_label.setPixmap(self.blur_pix)


        self.blur_slider = QSlider(self.blur)
        self.blur_slider.setGeometry(50, 795, 550, 15)
        self.blur_slider.setOrientation(QtCore.Qt.Horizontal)
        self.blur_slider.setMinimum(0)
        self.blur_slider.setMaximum(150)
        self.blur_slider.setValue(0)
        self.blur_slider.setStyleSheet(
            "*::handle:horizontal{background-color:red;border:1px solid red;border-radius:7px;}")  # "*::groove:horizontal{border-radius:5px;}"+"*::add-page:horizontal{background-color:black;}"+"*::sub-page:horizontal{background-color:red;}"
        self.blur_slider.valueChanged.connect(sliderx)

        def back():
            self.stackedwidgets.setCurrentIndex(0)

        def checked():
            if os.path.isfile(self.path+"Blured_image.jpg"):
                self.currentImage = self.path+"Blured_image.jpg"
                self.lable_update_thread()

        def cancel():
            self.blur_slider.setValue(0)
            self.blur_pix = QtGui.QPixmap(self.currentImage)
            self.blur_label.setPixmap(self.blur_pix)

        self.iconbutton(self.blur, "icons/back.svg", 1, 1, 53, 53, "Back", back)
        self.iconbutton(self.blur, "icons/checked.png", 1291, 715, 53, 53, "save", checked)
        self.iconbutton(self.blur, "icons/cancel.png", 1391, 715, 53, 53, "cancel", cancel)

        self.stackedwidgets.addWidget(self.blur)

    def ui_BW(self):
        self.BW = QWidget()
        self.BW.setGeometry(0, 0, 2135, 1551)

        self.image = cv2.imread(self.currentImage)
        frame_width, frame_height, left_margin, top_margin = self.resolution(self.image)

        self.bwlabel = QLabel(self.BW)
        self.bwpix = QtGui.QPixmap(self.currentImage)
        self.bwlabel.setPixmap(self.bwpix)
        self.bwlabel.setScaledContents(True)
        self.bwlabel.setFixedSize(int(frame_width), int(frame_height))
        self.bwlabel.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

        def bw_():
            Image_cv2.Black_and_White(self.image)
            self.bwpix = QtGui.QPixmap(self.path+"bw_image.jpg")
            self.bwlabel.setPixmap(self.bwpix)

        button_ = QPushButton(self.BW)
        button_.setGeometry(1281,150,179,54)
        button_.setText("Black & White")
        button_.setStyleSheet("QPushButton{border-radius:25px;font-weight:bold;background-color:black;color:white;} QPushButton::hover{background-color:white;color:black;border:1px solid black;}")
        button_.clicked.connect(bw_)

        def back():
            self.stackedwidgets.setCurrentIndex(0)

        def checked():
            if os.path.isfile(self.path+"bw_image.jpg"):
                self.currentImage = self.path+"bw_image.jpg"
                self.lable_update_thread()

        def cancel():
            self.bwpix = QtGui.QPixmap(self.currentImage)
            self.bwlabel.setPixmap(self.bwpix)

        self.iconbutton(self.BW, "icons/back.svg", 1, 1, 53, 53, "Back", back)
        self.iconbutton(self.BW, "icons/checked.png", 1291, 715, 53, 53, "save", checked)
        self.iconbutton(self.BW, "icons/cancel.png", 1391, 715, 53, 53, "cancel", cancel)

        self.stackedwidgets.addWidget(self.BW)

    def ui_color_invert(self):
        self.invert = QWidget()
        self.invert.setGeometry(0, 0, 2135, 1551)

        self.image = cv2.imread(self.currentImage)
        frame_width, frame_height, left_margin, top_margin = self.resolution(self.image)

        self.colorinv_label = QLabel(self.invert)
        self.colorinv_pix = QtGui.QPixmap(self.currentImage)
        self.colorinv_label.setPixmap(self.colorinv_pix)
        self.colorinv_label.setScaledContents(True)
        self.colorinv_label.setFixedSize(int(frame_width), int(frame_height))
        self.colorinv_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

        def color_invert():
            Image_cv2.color_invert(self.image)
            self.colorinv_pix = QtGui.QPixmap(self.path+"inverted_image.jpg")
            self.colorinv_label.setPixmap(self.colorinv_pix)

        button_ = QPushButton(self.invert)
        button_.setGeometry(1281,150,179,54)
        button_.setText("color invert")
        button_.setStyleSheet("QPushButton{border-radius:25px;font-weight:bold;background-color:black;color:white;} QPushButton::hover{background-color:white;color:black;border:1px solid black;}")
        button_.clicked.connect(color_invert)

        def back():
            self.stackedwidgets.setCurrentIndex(0)

        def checked():
            if os.path.isfile(self.path+"inverted_image.jpg"):
                self.currentImage = self.path+"inverted_image.jpg"
                self.lable_update_thread()

        def cancel():
            self.colorinv_pix = QtGui.QPixmap(self.currentImage)
            self.colorinv_label.setPixmap(self.colorinv_pix)


        self.iconbutton(self.invert, "icons/back.svg", 1, 1, 53, 53, "Back", back)
        self.iconbutton(self.invert, "icons/checked.png", 1291, 715, 53, 53, "save", checked)
        self.iconbutton(self.invert, "icons/cancel.png", 1391, 715, 53, 53, "cancel", cancel)

        self.stackedwidgets.addWidget(self.invert)

    def ui_resize(self):
        self.resize=QWidget()
        self.resize.setGeometry(0, 0, 2135, 1551)

        self.image = cv2.imread(self.currentImage)
        frame_width, frame_height, left_margin, top_margin = self.resolution(self.image)

        self.resize_label = QLabel(self.resize)
        self.resize_pix = QtGui.QPixmap(self.currentImage)
        self.resize_label.setPixmap(self.resize_pix)
        self.resize_label.setScaledContents(True)
        self.resize_label.setFixedSize(int(frame_width), int(frame_height))
        self.resize_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

        self.combox=QComboBox(self.resize)
        self.combox.setGeometry(1291,100,190,54)
        h,w,s=self.image.shape
        self.res_li=[]
        self.res_=[]
        for x in range(7):
            res=str(w//(x+2))+"x"+str(h//(x+2))
            resx=(w//(x+2),h//(x+2))
            if w//(x+2) > 10 and h//(x+2) > 10:
                self.res_li.append(res)
                self.res_.append(resx)
        self.x=0
        def update_(res):
            self.x=res
        def update_res():
            if len(self.res_) != 0:
                w, h = self.res_[self.x]
                self.image = cv2.imread(self.currentImage)
                Image_cv2.resize(self.image, w, h)
                self.currentImage = self.path+"resized.jpg"
                self.lable_update_thread()


        self.combox.addItems(self.res_li)
        self.combox.currentIndexChanged.connect(update_)

        button=QPushButton(self.resize)
        button.setGeometry(1291,200,190,54)
        button.setText("resize")
        button.setStyleSheet("QPushButton{border-radius:25px;font-weight:bold;background-color:black;color:white;} QPushButton::hover{background-color:white;color:black;border:1px solid black;}")
        button.clicked.connect(update_res)


        def back():
            self.lable_update_thread()
            self.stackedwidgets.setCurrentIndex(0)


        self.iconbutton(self.resize, "icons/back.svg", 1, 1, 53, 53, "Back", back)

        self.stackedwidgets.addWidget(self.resize)

    def update_combox(self):
        h, w, s = self.image.shape
        self.res_li.clear()
        self.res_.clear()
        for x in range(7):
            res = str(w // (x + 2)) + "x" + str(h // (x + 2))
            resx = (w // (x + 2), h // (x + 2))
            if w // (x + 2) > 10 and h // (x + 2) > 10:
                self.res_li.append(res)
                self.res_.append(resx)
        self.combox.clear()
        self.combox.addItems(self.res_li)

    def update_sliderpos(self):
        self.slider.setGeometry(1151, 250, 375, 15)
        self.contrast_slider.setGeometry(1151, 250, 375, 15)
        self.blur_slider.setGeometry(1151, 250, 375, 15)

    def ui_ai(self):
        self.ai=QWidget()
        self.ai.setGeometry(0, 0, 2135, 1551)


        self.image = cv2.imread(self.currentImage)
        frame_width, frame_height, left_margin, top_margin = self.resolution(self.image)

        self.swap_label = QLabel(self.ai)
        self.swap_pix = QtGui.QPixmap(self.currentImage)
        self.swap_label.setPixmap(self.swap_pix)
        self.swap_label.setScaledContents(True)
        self.swap_label.setFixedSize(int(frame_width), int(frame_height))
        self.swap_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

        self.ai_probar = QProgressBar(self.ai)
        self.ai_probar.setGeometry(1191,450,350,19)
        self.ai_probar.setAlignment(QtCore.Qt.AlignCenter)
        self.ai_probar.setStyleSheet("QProgressBar{border:1px solid white;border-radius:9px;font-weight:bold;} QProgressBar::chunk{border-radius:7px;background-color:qlineargradient(x1:0 y1:0,x2:1 y2:1,stop:0 red,stop:1 #fc00ff);}")
        self.ai_probar.hide()
        self.ai_prolable = QLabel(self.ai)
        self.ai_prolable.setGeometry(1295,495,350,19)
        self.ai_prolable.setText("# processing")
        self.ai_prolable.setStyleSheet("font-weight:bold;")
        self.ai_prolable.hide()

        def face_swap():
            try:
                self.ai_probar.show()
                self.ai_prolable.show()
                self.ai_probar.setValue(25)
                button.setEnabled(False)
                button_.setEnabled(False)
                Image_cv2.faceSwap(self.src_image,self.currentImage)
                self.ai_probar.setValue(50)
                self.ai_prolable.setText("# Rendering")
                time.sleep(0.1)
                self.ai_probar.setValue(75)
                button.setEnabled(True)
                button_.setEnabled(True)
                image = cv2.imread(self.path+"face_swap.jpg")
                frame_width, frame_height, left_margin, top_margin = self.resolution(image)
                time.sleep(0.1)
                self.ai_probar.setValue(95)
                time.sleep(0.1)
                self.ai_probar.hide()
                self.ai_prolable.hide()
                self.swap_pix = QtGui.QPixmap(self.path+"face_swap.jpg")
                self.swap_label.setPixmap(self.swap_pix)
                self.swap_label.setScaledContents(True)
                self.swap_label.setFixedSize(int(frame_width), int(frame_height))
                self.swap_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

            except:
                self.ai_probar.hide()
                self.ai_prolable.hide()
                button.setEnabled(True)
                button_.setEnabled(True)
                pymsgbox.alert("Image has no face or more than one face select an image with a face")



        def image_selector():
            filename, x = QFileDialog.getOpenFileName(self, 'Select image', filter="Image (*.jpg *.jpeg *.png *.gif)")
            if filename:
                self.src_image=filename
                thread()

        def thread():
            thread=threading.Thread(target=face_swap)
            thread.daemon=True
            thread.start()

        def image_beautify():
            Image_cv2.beautify(self.image)
            image = cv2.imread(self.path+"beautify.jpg")
            frame_width, frame_height, left_margin, top_margin = self.resolution(image)
            self.swap_pix = QtGui.QPixmap(self.path+"beautify.jpg")
            self.swap_label.setPixmap(self.swap_pix)
            self.swap_label.setScaledContents(True)
            self.swap_label.setFixedSize(int(frame_width), int(frame_height))
            self.swap_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

        button=QPushButton(self.ai)
        button.setGeometry(1291, 200, 190, 54)
        button.setText("FaceSwap")
        button.setStyleSheet("QPushButton{border-radius:25px;font-weight:bold;background-color:black;color:white;} QPushButton::hover{background-color:white;color:black;border:1px solid black;}")
        button.clicked.connect(image_selector)

        button_ = QPushButton(self.ai)
        button_.setGeometry(1291, 300, 190, 54)
        button_.setText("Beautify")
        button_.setStyleSheet(
            "QPushButton{border-radius:25px;font-weight:bold;background-color:black;color:white;} QPushButton::hover{background-color:white;color:black;border:1px solid black;}")
        button_.clicked.connect(image_beautify)

        def back():
            self.stackedwidgets.setCurrentIndex(0)

        def checked():
            if os.path.isfile(self.path+"face_swap.jpg"):
                self.currentImage = self.path+"face_swap.jpg"
                self.lable_update_thread()
            if os.path.isfile(self.path+"beautify.jpg"):
                self.currentImage=self.path+"beautify.jpg"
                self.lable_update_thread()

        def cancel():
            self.swap_pix = QtGui.QPixmap(self.currentImage)
            self.swap_label.setPixmap(self.swap_pix)


        self.iconbutton(self.ai, "icons/back.svg", 1, 1, 53, 53, "Back", back)
        self.iconbutton(self.ai, "icons/checked.png", 1291, 715, 53, 53, "save", checked)
        self.iconbutton(self.ai, "icons/cancel.png", 1391, 715, 53, 53, "cancel", cancel)

        self.stackedwidgets.addWidget(self.ai)


    def ui_file(self):
        file = QWidget()
        file.setGeometry(0, 0, 2135, 1551)
        file.setStyleSheet("background-color:qlineargradient(x1:0 y1:0,x2:1 y2:1,stop:0 #fc00ff,stop:1 #00d2ff);")
        def image_selector():
            filename, x = QFileDialog.getOpenFileName(self, 'open file', directory=self.usr_path,filter="Image (*.jpg *.jpeg *.png *.gif)")
            if filename:
                self.currentImage = filename
                self.image_save=filename.split('/')[-1]
                self.stackedwidgets.setCurrentIndex(0)
                self.lable_update_thread()

        label=QLabel(file)
        label.setGeometry(615,230,250,55)
        label.setText("PixPro")
        label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        label.setStyleSheet("color:#FF15D9;font-weight:bold;font-family:'Brush Script MT',cursive;font-size:185px;")
        label.adjustSize()

        button = QPushButton(file)
        button.setGeometry(700, 575, 250, 55)
        button.setText("select image")
        button.setStyleSheet("QPushButton{background-color:qlineargradient(x1:0 y1:0,x2:1 y2:1,stop:0 #5414FA,stop:1 #D714FA);color:white;font-weight:bold;border:3px solid red;border-radius:25px;} QPushButton::hover{border:3px solid white;color:black;background-color:red;}")
        button.clicked.connect(image_selector)
        self.stackedwidgets.addWidget(file)


        if os.path.exists(self.usr_path + "/.PixPro") == False:
            os.mkdir(self.usr_path + "/.PixPro")


    def file_save(self):
        r=str(random.randint(1,1000))
        x=QFileDialog.getSaveFileName(self,"save Image",self.usr_path+"/"+self.image_save.split('.')[0]+"_x"+r,filter="Image (*.jpg *.jpeg)")
        if x[0]:
            shutil.copy(self.currentImage,x[0])
            pymsgbox.alert("image saved in path : "+x[0])



    def resolution(self, image):

        h, w, s= image.shape
        frame_width = None
        frame_height = None
        left_margin = 25
        top_margin = 55

        if w > h or w==h:
            if w <= 855:
                frame_width = w
                frame_height = h
                self.res=1
            if w >= 900:
                frame_width = w // 1.5
                frame_height = h // 1.5
                self.res = 1.5
            if w >=1200:
                frame_width = w // 2
                frame_height = h // 2
                self.res = 2
            if w > 1700:
                frame_width = w // 2.5
                frame_height = h // 2.5
                self.res = 2.5
            if w >= 2000:
                frame_width = w // 3
                frame_height = h // 3
                self.res = 3
            if w >= 3000:
                frame_width = w // 4
                frame_height = h // 4
                self.res = 4
            if w >= 4000:
                frame_width = w // 5
                frame_height = h // 5
                self.res = 5

        if h > w:
            if h > 700 & h < 851:
                frame_width = w
                frame_height = h
                self.res=1
            if h > 851:
                frame_width = w // 1.5
                frame_height = h // 1.5
                self.res = 1.5
            if h > 1200:
                frame_width = w // 2
                frame_height = h // 2
                self.res = 2
            if h > 1700:
                frame_width = w // 2.5
                frame_height = h // 2.5
                self.res = 2.5
            if h > 2000:
                frame_width = w // 3
                frame_height = h // 3
                self.res = 3
            if h > 2500:
                frame_width = w // 4
                frame_height = h // 4
                self.res = 4
            if h > 3000:
                frame_width = w // 5
                frame_height = h // 5
                self.res = 5

        frame_width=int(frame_width)
        frame_height=int(frame_height)
        x=875-frame_height
        top_margin=int(x/2)
        y=1000-frame_width
        left_margin=int(y/4)

        return (frame_width, frame_height, left_margin, top_margin)

    def iconbutton(self, widget, icon, l, r, w, h, tooltip, x,s=35):
        button = QPushButton(widget)
        button.setIcon(QtGui.QIcon(icon))
        button.setToolTip(tooltip)
        button.setGeometry(l, r, w, h)
        button.setIconSize(QtCore.QSize(s, s))
        button.clicked.connect(x)
        button.setStyleSheet("QPushButton{border-radius:25px;} QPushButton::hover{background-color:white;}")


    def lable_update(self):
        try:
            self.image = cv2.imread(self.currentImage)
            frame_width, frame_height, left_margin, top_margin = self.resolution(self.image)

            self.pix = QtGui.QPixmap(self.currentImage)
            self.label.setPixmap(self.pix)
            self.label.setScaledContents(True)
            self.label.setFixedSize(int(frame_width), int(frame_height))
            self.label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

            self.crop_pix = QtGui.QPixmap(self.currentImage).scaled(int(frame_width), int(frame_height),
                                                                    QtCore.Qt.KeepAspectRatio)
            self.crop_label.setPixmap(self.crop_pix)
            self.crop_label.setScaledContents(True)
            self.crop_label.setFixedSize(int(frame_width), int(frame_height))
            self.crop_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

            self.ui_pix = QtGui.QPixmap(self.currentImage)
            self.ui_label.setPixmap(self.ui_pix)
            self.ui_label.setScaledContents(True)
            self.ui_label.setFixedSize(int(frame_width), int(frame_height))
            self.ui_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

            self.contrast_pix = QtGui.QPixmap(self.currentImage)
            self.contrast_label.setPixmap(self.contrast_pix)
            self.contrast_label.setScaledContents(True)
            self.contrast_label.setFixedSize(int(frame_width), int(frame_height))
            self.contrast_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

            self.s_pix = QtGui.QPixmap(self.currentImage)
            self.s_label.setPixmap(self.s_pix)
            self.s_label.setScaledContents(True)
            self.s_label.setFixedSize(int(frame_width), int(frame_height))
            self.s_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

            self.cartoon_pix = QtGui.QPixmap(self.currentImage)
            self.cartoon_label.setPixmap(self.cartoon_pix)
            self.cartoon_label.setScaledContents(True)
            self.cartoon_label.setFixedSize(int(frame_width), int(frame_height))
            self.cartoon_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

            self.ad_pix = QtGui.QPixmap(self.currentImage)
            self.ad_label.setPixmap(self.ad_pix)
            self.ad_label.setScaledContents(True)
            self.ad_label.setFixedSize(int(frame_width), int(frame_height))
            self.ad_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

            self.swap_pix = QtGui.QPixmap(self.currentImage)
            self.swap_label.setPixmap(self.swap_pix)
            self.swap_label.setScaledContents(True)
            self.swap_label.setFixedSize(int(frame_width), int(frame_height))
            self.swap_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

            self.en_pix = QtGui.QPixmap(self.currentImage)
            self.en_label.setPixmap(self.en_pix)
            self.en_label.setScaledContents(True)
            self.en_label.setFixedSize(int(frame_width), int(frame_height))
            self.en_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

            self.flip_pix = QtGui.QPixmap(self.currentImage)
            self.flip_label.setPixmap(self.flip_pix)
            self.flip_label.setScaledContents(True)
            self.flip_label.setFixedSize(int(frame_width), int(frame_height))
            self.flip_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

            self.rotate_pix = QtGui.QPixmap(self.currentImage)
            self.rotate_label.setPixmap(self.rotate_pix)
            self.rotate_label.setScaledContents(True)
            self.rotate_label.setFixedSize(int(frame_width), int(frame_height))
            self.rotate_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

            self.blur_pix = QtGui.QPixmap(self.currentImage)
            self.blur_label.setPixmap(self.blur_pix)
            self.blur_label.setScaledContents(True)
            self.blur_label.setFixedSize(int(frame_width), int(frame_height))
            self.blur_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

            self.bwpix = QtGui.QPixmap(self.currentImage)
            self.bwlabel.setPixmap(self.bwpix)
            self.bwlabel.setScaledContents(True)
            self.bwlabel.setFixedSize(int(frame_width), int(frame_height))
            self.bwlabel.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

            self.colorinv_pix = QtGui.QPixmap(self.currentImage)
            self.colorinv_label.setPixmap(self.colorinv_pix)
            self.colorinv_label.setScaledContents(True)
            self.colorinv_label.setFixedSize(int(frame_width), int(frame_height))
            self.colorinv_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

            self.resize_pix = QtGui.QPixmap(self.currentImage)
            self.resize_label.setPixmap(self.resize_pix)
            self.resize_label.setScaledContents(True)
            self.resize_label.setFixedSize(int(frame_width), int(frame_height))
            self.resize_label.setGeometry(left_margin, top_margin, int(frame_width), int(frame_height))

            if frame_height > frame_width:
                self.update_sliderpos()

            self.update_combox()
        except:
            self.lable_update_thread()


    def lable_update_thread(self):
        thread=threading.Thread(target=self.lable_update)
        thread.daemon=True
        thread.start()

class Qlabel(QLabel):
    def __init__(self, widget):
        super(Qlabel, self).__init__(widget)
        self.rband = False
        self.x = False

    def mousePressEvent(self, eventQMouseEvent):
        self.hiderubberband(True)
        self.Qpoint = eventQMouseEvent.pos()
        self.currRubberband = QRubberBand(QRubberBand.Rectangle, self)
        self.currRubberband.setGeometry(QtCore.QRect(self.Qpoint, QtCore.QSize()))
        self.currRubberband.show()

    def mouseMoveEvent(self, eventQMouseEvent):
        self.currRubberband.setGeometry(QtCore.QRect(self.Qpoint, eventQMouseEvent.pos()).normalized())

    def mouseReleaseEvent(self, eventQMouseEvent):
        currRect = self.currRubberband.geometry()
        self.x = currRect
        self.rband = True


    def hiderubberband(self, x):
        if x == True & self.rband == True:
            self.currRubberband.deleteLater()
            self.rband = False
        else:
            pass

    def getpos(self):
        if self.x:
            x = len(str(self.x).split('.')[2]) - 1
            x = (str(self.x).split('.')[2][6:x].split(','))
            posx = []
            for pos in x:
                px = int(pos)
                posx.append(px)
                self.x = None
            return posx
        else:
            pass


class Image_cv2():

    @staticmethod
    def cartoon_effect(image):
        img=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        img = cv2.medianBlur(img, 5)
        img_edge = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 7)
        img_color = image
        img_color = cv2.bilateralFilter(img_color, d=9, sigmaColor=250, sigmaSpace=250)
        ct = cv2.bitwise_and(img_color, img_color, mask=img_edge)

        def colorizer(img, v):
            d = numpy.float32(img).reshape((-1, 3))
            c = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
            r, l, ce = cv2.kmeans(d, v, None, c, 10, cv2.KMEANS_RANDOM_CENTERS)
            center = numpy.uint8(ce)
            colorized = center[l.flatten()]
            colorized = colorized.reshape(ct.shape)
            return colorized

        cartoon=colorizer(ct, 9)
        cv2.imwrite((os.path.expanduser("~") + "/.PixPro/")+"cartoon_image.jpg",cartoon)

        # img=cv2.stylization(image,sigma_s=150,sigma_r=0.25)
        # cv2.imwrite("cartoon_image.jpg", img)

    @staticmethod
    def denoiser(img):
        img_shape = img.shape[2]
        if img_shape == 3:
            denoised = cv2.fastNlMeansDenoisingColored(img)
            cv2.imwrite((os.path.expanduser("~") + "/.PixPro/")+"adjusted_image.jpg",denoised)
        else:
            denoised = cv2.fastNlMeansDenoising(img)
            cv2.imwrite((os.path.expanduser("~") + "/.PixPro/")+"adjusted_image.jpg",denoised)

    @staticmethod
    def pencil_sketch(img):
        image_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        image_inv=255-image_gray
        image_=cv2.GaussianBlur(image_inv,ksize=(21,21),sigmaX=0,sigmaY=0)
        def dodging(im,mask):
            return cv2.divide(im,255-mask,scale=256)
        image=dodging(image_gray,image_)
        cv2.imwrite((os.path.expanduser("~") + "/.PixPro/")+"sketch_image.jpg",image)

    @staticmethod
    def sketch(img,t1=90, t2=150):
        image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        image=cv2.Canny(image,threshold1=t1,threshold2=t2)
        image=cv2.bitwise_not(image)
        cv2.imwrite((os.path.expanduser("~") + "/.PixPro/")+"sketch_image.jpg",image)

    @staticmethod
    def enhance(img, res):
        upscale_res = None
        if res == 2:
            upscale_res = "data_model/EDSR_x2.pb"
        if res == 3:
            upscale_res = "data_model/EDSR_x3.pb"
        if res == 4:
            upscale_res = "data_model/EDSR_x4.pb"
        upscale = cv2.dnn_superres.DnnSuperResImpl_create()
        upscale.readModel(upscale_res)
        upscale.setModel("edsr", res)
        image = upscale.upsample(img)

        cv2.imwrite((os.path.expanduser("~") + "/.PixPro/")+"enhanced_image.jpg",image)

    @staticmethod
    def flip(img, type=1):
        image = cv2.flip(img, type)
        cv2.imwrite((os.path.expanduser("~") + "/.PixPro/")+"fliped_image.jpg",image)

    @staticmethod
    def rotate(img, deg):
        degx = None
        if deg == 0:
            degx = cv2.ROTATE_90_COUNTERCLOCKWISE
        if deg == 1:
            degx = cv2.ROTATE_180

        image = cv2.rotate(img, degx)
        cv2.imwrite((os.path.expanduser("~") + "/.PixPro/")+"rotated_image.jpg",image)

    @staticmethod
    def brightness(img, brightness):
        bright = int((brightness) * (255 + 255)) / (510) + (-255)
        shadow = bright
        max = 255
        alpha = (max - shadow) / 255
        gamma = shadow
        img = cv2.addWeighted(img, alpha, img, 0, gamma)
        cv2.imwrite((os.path.expanduser("~") + "/.PixPro/")+"Brightned_image.jpg",img)

    @staticmethod
    def contrast(img, contrast):
        # contrast = 19 # int((c)*(127-(-127))/(254)-(-127))
        alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
        gamma = 127 * (1 - alpha)
        img = cv2.addWeighted(img, alpha, img, 0, gamma)
        cv2.imwrite((os.path.expanduser("~") + "/.PixPro/")+"contrast_image.jpg",img)

    @staticmethod
    def auto_BrightContrast(img, clip_hist=1):
        grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        hist = cv2.calcHist([grayscaled], [0], None, [256], [0, 256])
        hist_len = len(hist)

        accu = []
        accu.append(float(hist[0]))
        for index in range(1, hist_len):
            accu.append(accu[index - 1] + float(hist[index]))

        max = accu[-1]
        clip_hist *= (max / 100.0)
        clip_hist /= 2.0

        min_gray = 0
        while accu[min_gray] < clip_hist:
            min_gray += 1

        max_gray = hist_len - 1
        while accu[max_gray] >= (max - clip_hist):
            max_gray -= 1

        alpha = 255 / (max_gray - min_gray)
        beta = -min_gray * alpha

        image = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
        cv2.imwrite((os.path.expanduser("~") + "/.PixPro/")+"adjusted_image.jpg",image)

    @staticmethod
    def blur(img, blur):
        image = cv2.GaussianBlur(img, (blur, blur), 0)
        cv2.imwrite((os.path.expanduser("~") + "/.PixPro/")+"Blured_image.jpg",image)

    @staticmethod
    def Black_and_White(img):
        image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        cv2.imwrite((os.path.expanduser("~") + "/.PixPro/")+"bw_image.jpg",image)

    @staticmethod
    def color_invert(img):
        image = cv2.bitwise_not(img)
        cv2.imwrite((os.path.expanduser("~") + "/.PixPro/")+"inverted_image.jpg",image)

    @staticmethod
    def resize(img,w,h):
        image=cv2.resize(img,(w,h))
        cv2.imwrite((os.path.expanduser("~") + "/.PixPro/")+"resized.jpg",image)


    @staticmethod
    def faceSwap(src_img,dst_img):
        src_image = cv2.imread(src_img)
        dst_image = cv2.imread(dst_img)

        predictor = dlib.shape_predictor("data_model/shape_predictor_68_face_landmarks.dat")

        def face_detecor(img, r=10):
            def detector(im):
                detector = dlib.get_frontal_face_detector()
                faces = detector(im, 1)
                return faces

            def face_point(im, pos: dlib.rectangle):
                shape = predictor(im, pos)
                points = numpy.asarray(list([pts.x, pts.y] for pts in shape.parts()), dtype=numpy.int32)
                return points

            faces = detector(img)
            x = numpy.argmax([(face.right() - face.left()) * (face.bottom() - face.top()) for face in faces])
            pos = faces[x]
            points = numpy.asarray(face_point(img, pos))

            w, h, s = img.shape
            left, top = numpy.min(points, 0)
            right, bottom = numpy.max(points, 0)
            x, y = max(0, left - r), max(0, top - r)
            w, h = min(right + r, h) - x, min(bottom + r, w) - y

            return points - numpy.asarray([[x, y]]), (x, y, w, h), img[y:y + h, x:x + w]

        src_points, src_shape, src_face = face_detecor(src_image)
        dst_points, dst_shape, dst_face = face_detecor(dst_image)
        def face_swap(src_face, dst_face, src_points, dst_points, dst_shape, dst_img):
            def triangle(delx, src_points, dst_points):
                ones = [1, 1, 1]
                for z in delx:
                    src_tri = numpy.vstack((src_points[z, :].T, ones))
                    dst_tri = numpy.vstack((dst_points[z, :].T, ones))
                    mat = numpy.dot(src_tri, numpy.linalg.inv(dst_tri))[:2, :]
                    yield mat

            def grid(point):
                xmin = numpy.min(point[:, 0])
                xmax = numpy.max(point[:, 0]) + 1
                ymin = numpy.min(point[:, 1])
                ymax = numpy.max(point[:, 1]) + 1
                return numpy.asarray([(x, y) for y in range(ymin, ymax) for x in range(xmin, xmax)], numpy.uint32)

            def bilinear(im, cord):
                int_cords = numpy.int32(cord)
                x0, y0 = int_cords
                dx, dy = cord - int_cords
                q11 = im[y0, x0]
                q21 = im[y0, x0 + 1]
                q12 = im[y0 + 1, x0]
                q22 = im[y0 + 1, x0 + 1]
                bottom = q21.T * dx + q11.T * (1 - dx)
                top = q22.T * dx + q12.T * (1 - dx)
                inter = top * dy + bottom * (1 - dy)
                return inter.T

            def process(src_image, img, tri_aff, dst_points, delx):
                roi_cords = grid(dst_points)
                roi_tri = delx.find_simplex(roi_cords)
                for z in range(len(delx.simplices)):
                    cords = roi_cords[roi_tri == z]
                    num_cord = len(cords)
                    out_cord = numpy.dot(tri_aff[z], numpy.vstack((cords.T, numpy.ones(num_cord))))
                    x_, y_ = cords.T
                    img[y_, x_] = bilinear(src_image, out_cord)
                return None

            def warp_img(src_image, src_points, dst_points, dst_shape):
                rows, cols = dst_shape[:2]
                img = numpy.zeros((rows, cols, 3), dtype=numpy.uint8)
                delx = spatial.Delaunay(dst_points)
                tri_aff = numpy.asarray(list(triangle(delx.simplices, src_points, dst_points)))
                process(src_image, img, tri_aff, dst_points, delx)

                return img

            def mask_points(size, points):
                radius = 10
                kernel = numpy.ones((radius, radius), numpy.uint8)
                mask_ = numpy.zeros(size, numpy.uint8)
                cv2.fillConvexPoly(mask_, cv2.convexHull(points), 255)
                mask_ = cv2.erode(mask_, kernel, iterations=1)
                return mask_

            def apply_mask(img, mask_):
                mask_img = cv2.bitwise_and(img, img, mask=mask_)
                return mask_img

            def color_correct(im, im_, landmark):
                color = 0.75
                left = list(range(42, 48))
                right = list(range(36, 42))
                blur = color * numpy.linalg.norm(numpy.mean(landmark[left], axis=0) - numpy.mean(landmark[right], axis=0))
                blur = int(blur)
                if blur % 2 == 0:
                    blur += 1
                im_blur = cv2.GaussianBlur(im, (blur, blur), 0)
                im__blur = cv2.GaussianBlur(im_, (blur, blur), 0)

                im__blur = im__blur.astype(int)
                im__blur += 128 * (im__blur <= 1)
                res = im_.astype(numpy.float64) * im_blur.astype(numpy.float64) / im__blur.astype(numpy.float64)
                res = numpy.clip(res, 0, 255).astype(numpy.uint8)
                return res


            def transform(point1,point2):
                point1=point1.astype(numpy.float64)
                point2=point2.astype(numpy.float64)

                cx=numpy.mean(point1,axis=0)
                cy=numpy.mean(point2,axis=0)
                point1-=cx
                point2-=cy

                s_=numpy.std(point1)
                s__=numpy.std(point2)
                point1/=s_
                point2/=s__

                u,s,v=numpy.linalg.svd(numpy.dot(point1.T,point2))
                r__=(numpy.dot(u,v)).T
                return numpy.vstack([numpy.hstack([s__/s_*r__,(cy.T-numpy.dot(s__/s_*r__,cx.T))[:,numpy.newaxis]]),numpy.array([[0.,0.,1.]])])




            def warp_2d(im,x,dshape):
                resx=numpy.zeros(dshape,dtype=im.dtype)
                cv2.warpAffine(im,x[:2],(dshape[1],dshape[0]),dst=resx,borderMode=cv2.BORDER_TRANSPARENT,flags=cv2.WARP_INVERSE_MAP)
                return resx

            h, w, s = dst_face.shape

            warp_src = warp_img(src_face, src_points[:48], dst_points[:48], (h, w))
            mask = mask_points((h, w), dst_points)
            mask_src = numpy.mean(warp_src, axis=2) > 0
            mask = numpy.asarray(mask * mask_src, dtype=numpy.uint8)

            warp_src = apply_mask(warp_src, mask)
            dst_face_mask = apply_mask(dst_face, mask)
            warp_src = color_correct(dst_face_mask, warp_src, dst_points)


            unwarp_src=warp_img(warp_src,dst_points[:48],src_points[:48],src_face.shape[:2])
            warp_src=warp_2d(unwarp_src,transform(dst_points,src_points),(h,w,3))
            mask=mask_points((h,w),dst_points)
            mask_src=numpy.mean(warp_src,axis=2)>0
            mask=numpy.asarray(mask*mask_src,dtype=numpy.uint8)




            kernel = numpy.ones((10, 10), numpy.uint8)
            mask = cv2.erode(mask, kernel, iterations=1)
            r = cv2.boundingRect(mask)
            c = ((r[0] + int(r[2] / 2), r[1] + int(r[3] / 2)))
            res = cv2.seamlessClone(warp_src, dst_face, mask, c, cv2.NORMAL_CLONE)

            x, y, w, h = dst_shape
            dst_imgx = dst_img.copy()
            dst_imgx[y:y + h, x:x + w] = res

            return dst_imgx
        res = face_swap(src_face, dst_face, src_points, dst_points, dst_shape, dst_image)
        cv2.imwrite((os.path.expanduser("~") + "/.PixPro/")+"face_swap.jpg",res)


    @staticmethod
    def beautify(img):
        image=cv2.bilateralFilter(img,15,35,35)
        cv2.imwrite((os.path.expanduser("~") + "/.PixPro/")+"beautify.jpg",image)

    @staticmethod
    def clear_cache():
        cache_dir=(os.path.expanduser("~") + "/.PixPro")
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)



if __name__=="__main__":
    multiprocessing.freeze_support()
    app = QApplication([])
    win = window()
    win.show()
    atexit.register(Image_cv2.clear_cache)
    sys.exit(app.exec_())
