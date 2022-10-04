import requests
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from ..commons import URL_PATH
from ..gui import Ui_AuthWindow
from .content import UiContentWindowImpl
from .help import UiHelpWindowImpl
from .registration import UiRegistrationWindowImpl

__all__ = ["UiAuthWindowImpl"]


class UiAuthWindowImpl(QMainWindow, Ui_AuthWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.SignIn.clicked.connect(self.login)
        self.RegistrationBtn.clicked.connect(self.on_registration)
        self.HelpBtn.clicked.connect(self.on_help)
        self.session = requests.Session()
        self.error = ""
        self.client = {"id": -1, "email": ""}
        self.content = UiContentWindowImpl
        self.help = UiHelpWindowImpl
        self.registration = UiRegistrationWindowImpl

        self.Email.setText("admin@example.com")
        self.Password.setText("admin")

    def login(self):
        try:
            email = self.Email.toPlainText()
            password = self.Password.toPlainText()
            response = requests.post(
                URL_PATH("api/auth/login"), json={"email": email, "password": password}
            )
            if response.status_code == 202:
                jwt_secret = response.cookies.get_dict()["JWT"].split(".")[2]
                self.client["id"] = response.json()["id"]
                self.client["email"] = email
                self.client["secret"] = jwt_secret
                self.content = self.content(self.client)
                self.content.show()
                self.hide()
            else:
                self.error = response.json()["message"]
                self.errorOperation()
        except Exception as e:
            self.error = e
            self.errorOperation()

    def validate_data(self):
        if len(self.Email.toPlainText()) == 0:
            self.error += "Поле почты пустое"
        if len(self.Password.toPlainText()) == 0:
            self.error += "Поле пароля пустое"
        if self.error != "":
            return False
        return True

    def on_registration(self):
        self.registration = self.registration()
        self.registration.show()
        self.hide()

    def on_help(self):
        self.help = self.help()
        self.help.show()
        self.hide()

    def errorOperation(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Неверные данные")
        msg.setInformativeText(str(self.error))
        msg.setWindowTitle("Ошибка")
        msg.show()

    # def closeEvent(self, event):
    #     dialog = QMessageBox
    #     ret = QMessageBox.question(
    #         self, "", "Уверены что хотите выйти?", dialog.Yes | dialog.No
    #     )
    #     if ret == dialog.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()
