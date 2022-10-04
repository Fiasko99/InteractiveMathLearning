from .. import users
from ..abs import User


class UserDAO(User):
    def __init__(self, u: users.User):
        self.__user = u

    # def login(self):
    #     self.__cookies = requests.post("URL", json=self.__user.json()).get_cookies
    #     return self
    #
    # def logout(self):
    #     requests.post("LOGOUT_URL", cookies=self.__cookies)
    # ...
