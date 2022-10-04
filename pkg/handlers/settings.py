from typing import List

import requests
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from ..commons import URL_PATH
from ..gui import Ui_SettingsWindow

__all__ = ["UiSettingsWindowImpl"]


class UiSettingsWindowImpl(QMainWindow, Ui_SettingsWindow):
    text_message: str = ""

    def __init__(self, client):
        super().__init__()
        self.setupUi(self)
        self.client = client
        self.send_new_password.clicked.connect(self.send_new_pass)
        self.send_new_email.clicked.connect(self.send_new_mail)

    def send_new_pass(self):
        new_pass = self.new_password_value.toPlainText()
        real_pass = self.real_pass_value.toPlainText()
        if self.validate_data([self.new_password_value, self.real_pass_value]):
            r = requests.put(
                url=URL_PATH(f"api/users/{self.client['id']}/password"),
                cookies={"JWT": self.client["secret"]},
                json={"old_password": real_pass, "new_password": new_pass},
            )
            if r.status_code == 200:
                self.text_message = "Ваш пароль обновлен"
                self._message(True)
            else:
                json_r = r.json()
                self.text_message = json_r["message"]
                self._message()
        else:
            self._message()

    def send_new_mail(self):
        new_email = self.new_email_value.toPlainText()
        if self.validate_data([self.new_email_value]):
            r = requests.put(
                url=URL_PATH(f"api/users/{self.client['id']}/email"),
                cookies={"JWT": self.client["secret"]},
                json={"email": new_email},
            )
            if r.status_code == 200:
                self.text_message = "Ваша почта обновлена"
                self._message(True)
            else:
                json_r = r.json()
                self.text_message = json_r["message"]
                self._message()
        else:
            self._message()

    def validate_data(self, field_list: List[object]) -> bool:
        """

        Args:
            field_list: list of text edit objects

        Returns: False if text edit value is empty else True

        """
        self.text_message = ""
        for filed_text_edit in field_list:
            if not filed_text_edit.toPlainText():
                self.text_message += (
                    "Поле "
                    + filed_text_edit.placeholderText()
                    + " не должно быть пустым. \n"
                )
                return False
        return True

    def _message(self, success=False):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical if not success else QMessageBox.Information)
        msg.setInformativeText(self.text_message)
        msg.setWindowTitle("Ошибка" if not success else "Успешно")
        msg.show()
