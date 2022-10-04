import requests
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from ..commons import URL_PATH
from ..gui import Ui_HelpWindow

__all__ = ["UiHelpWindowImpl"]


class UiHelpWindowImpl(QMainWindow, Ui_HelpWindow):
    text_message: str = ""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        from .auth import UiAuthWindowImpl

        self.window = UiAuthWindowImpl
        self.LoginBtn.clicked.connect(self.on_login)
        self.SendMail.clicked.connect(self.restore_password)

    def on_login(self):
        self.prev_page()

    def closeEvent(self, event):
        self.prev_page()

    def prev_page(self):
        self.window = self.window()
        self.window.show()
        self.hide()

    def restore_password(self):
        self.text_message = ""
        email = self.Email.toPlainText()
        if self.validate_email():
            r = requests.patch(url=URL_PATH("api/users/reset"), json={"email": email})
            if r.status_code == 200:
                self.text_message = "Сообщение с новым паролем отправлено на вашу почту"
                self.__message(True)
            else:
                self.text_message = r.json().get("message", "Ошибка")
                self.__message()
        else:
            self.__message()

    def validate_email(self):
        if "@" not in self.Email.toPlainText() or "." not in self.Email.toPlainText():
            self.text_message += "Неккоретная почта"
        if len(self.Email.toPlainText()) < 3:
            self.text_message += "Неккоретная почта"
        if self.text_message != "":
            return False
        return True

    def __message(self, success=False):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical if not success else QMessageBox.Information)
        msg.setInformativeText(self.text_message)
        msg.setWindowTitle("Ошибка" if not success else "Успешно")
        msg.show()
