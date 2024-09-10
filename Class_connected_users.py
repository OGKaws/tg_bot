from Class_clients import Clients
from Class_users import User


class Connected_Users:
    def __init__(self):
        self.users_connected = {}

    def User_Connect(self, user):
        self.users_connected[user.user_id] = Clients(user.client_db_name)

    def Clear(self):
        self.users_connected.clear()

    def GetClients(self, userid):
        return self.users_connected[userid]


