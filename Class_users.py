import json
import os.path


def users_setup(user_id):
    if os.path.exists('trainers.json'):
        with open('trainers.json', 'r') as trainers_json:
            data = json.load(trainers_json)
            for user_data in data:
                if user_data.get('Id') == user_id:
                    user = User(user_data['Имя пользователя'],
                                user_data['Права админа'],
                                user_data['Id'])
                    return user
    return None
    #tfile = загружаю файл treiners_json (в файле содержаться данные по тренерам)
    #находим в файле bot_id (идентификатор пользователя ТГ)
    #user = User (tfile.name, false, db_name)
    #return user


class User():
    def __init__(self, username, is_admin, user_id, add_to_file = False):
        self.name = username
        self.user_id = user_id
        self.is_admin = is_admin
        self.client_db_name = f'{self.user_id}_clients_json'
        if add_to_file : self.__Save_user_to_file()

    def __Save_user_to_file(self):
        new_user = self.User_to_dict()
        if os.path.exists('trainers.json'):
            with open('trainers.json', 'r') as trainers_json:

                users_data = json.load(trainers_json)
        else :
            users_data = []
        #for elem in users_data:
        #    if elem['id'] == self.user_id: return
        users_data.append(new_user)
        with open('trainers.json', 'w') as trainers_json:
            json.dump(users_data, trainers_json, ensure_ascii=False, indent=4)

    def User_to_dict(self):
        return {'Имя пользователя' : self.name,
                'Id' : self.user_id,
                'Клиентская база' : self.client_db_name,
                'Права админа' : self.is_admin
                }

    # def User_save(self):
    #     with open('trainers.json', 'w') as trainers_json