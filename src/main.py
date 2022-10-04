from PyQt5 import QtWidgets

from pkg import UiAuthWindowImpl

__all__ = ["Application"]


class Application:
    @staticmethod
    def run():
        import sys

        app = QtWidgets.QApplication(sys.argv)
        window = UiAuthWindowImpl()
        window.show()
        app.exec_()

    ...
