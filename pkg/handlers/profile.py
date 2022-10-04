from PyQt5.QtWidgets import QMainWindow

from ..gui import Ui_ProfileWindow
from .settings import UiSettingsWindowImpl

__all__ = ["UiProfileWindowImpl"]


class UiProfileWindowImpl(QMainWindow, Ui_ProfileWindow):
    window: UiSettingsWindowImpl

    def __init__(self, client):
        super().__init__()
        self.setupUi(self)
        self.client = client
        self.editProfile.clicked.connect(self.to_edit)

    def fill_profile(self):
        self.emailValue.setText(self.client["email"])

    def to_edit(self):
        self.window = UiSettingsWindowImpl(self.client)
        self.window.show()
        self.close()
