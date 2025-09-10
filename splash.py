import time
from PyQt5.QtWidgets import QSplashScreen
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

def show_loading_screen(app):
    splash_pix = QPixmap(600, 200)
    splash_pix.fill(Qt.black)
    splash = QSplashScreen(splash_pix)
    splash.setFont(QFont("Courier", 10))
    splash.show()
    app.processEvents()

    steps = ["Loading...", "Assembling interface...", "Finalising..."]
    for step in steps:
        splash.showMessage(step, Qt.AlignCenter, Qt.white)
        app.processEvents()
        time.sleep(0.5)

    return splash

def show_title_screen(app):
    splash_pix = QPixmap(600, 200)
    splash_pix.fill(Qt.black)
    splash = QSplashScreen(splash_pix)
    splash.setFont(QFont("Courier", 10))
    splash.show()
    app.processEvents()

    splash.showMessage("Loading Completed", Qt.AlignCenter, Qt.white)
    time.sleep(2)
    app.processEvents()

    return splash