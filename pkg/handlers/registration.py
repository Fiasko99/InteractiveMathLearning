import requests
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from ..commons import URL_PATH
from ..gui import Ui_RegistrationWindow

__all__ = ["UiRegistrationWindowImpl"]


class UiRegistrationWindowImpl(QMainWindow, Ui_RegistrationWindow):
    text_message: str = ""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        from .auth import UiAuthWindowImpl

        self.window = UiAuthWindowImpl
        self.LoginBtn.clicked.connect(self.on_login)
        self.SignUp.clicked.connect(self.registration_new_user)

    def on_login(self):
        self.prev_page()

    def closeEvent(self, event):
        self.prev_page()

    def prev_page(self):
        self.window = self.window()
        self.window.show()
        self.hide()

    def registration_new_user(self):
        self.text_message = ""
        try:
            email = self.Email.toPlainText()
            password = self.Password.toPlainText()
            if self.check_validate():
                json = {"email": email, "password": password, "role": "user"}
                r = requests.post(url=URL_PATH("api/users"), json=json)
                if r.status_code == 200:
                    self.text_message = "Ваш профиль зарегистрирован"
                    self._message(True)
                else:
                    json_r = r.json()
                    self.text_message = str(r.status_code) + " " + json_r["message"]
                    self._message()
            else:
                self._message()
        except Exception as e:
            print(e)

    def check_validate(self):
        if self.Password.toPlainText() != self.PasswordConfirm.toPlainText():
            self.text_message += "Пароли не совпадают.\n"
        if len(self.Email.toPlainText()) == 0:
            self.text_message += "Поле почты пустое.\n"
        if len(self.Password.toPlainText()) == 0:
            self.text_message += "Поле почты пустое.\n"
        if len(self.PasswordConfirm.toPlainText()) == 0:
            self.text_message += "Поле почты пустое.\n"
        if self.text_message != "":
            return False
        return True

    def _message(self, success=False):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical if not success else QMessageBox.Information)
        msg.setInformativeText(str(self.text_message))
        msg.setWindowTitle("Ошибка" if not success else "Успешно")
        msg.show()
