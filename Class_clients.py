import os.path

from Class_client import Client
import json

class Clients():
    def __init__(self,fname):
        self.client_list = []
        self.__json_file_name = fname
        self.__load_from_json()

    def Clients_finde(self, name):
        for client in self.client_list:
            if client.name == name:
                return client

    def Clients_delete(self, name):
        client_for_delete = self.Clients_finde(name)
        self.client_list.remove(client_for_delete)
        return "Клиент удален"

    def Clients_create(self, name):
        client_obj = Client(name)
        self.client_list.append(client_obj)

    def Clients_mark_training(self, name):
        mark_for_client = self.Clients_finde(name)
        if mark_for_client:
            mark_for_client.Client_comp_training()

    def Clients_paid_done(self, name, paid, cost):
        paid_client = self.Clients_finde(name)
        if paid_client:
            paid_client.Client_paid_training(paid, cost)


    def Clients_rename(self, old_name, new_name):
        # Поиск объекта Client в списке client_list по имени
        client_for_rename = self.Clients_finde(old_name)
        if client_for_rename:
            client_for_rename.name = new_name

    def __load_from_json(self):
        if os.path.exists(self.__json_file_name):
           with open(self.__json_file_name, 'r') as client_json:
               data = json.load(client_json)
               for client in data:
                   client_obj = Client(client['Client name '])
                   client_obj.paid_training = client['paid training ']
                   client_obj.done_training = client['Complete training ']
                   self.client_list.append(client_obj)



    def save_to_json(self):
        with open(self.__json_file_name, 'w') as client_json:
            data = [client.Client_to_dict() for client in self.client_list]
            json.dump(data, client_json, ensure_ascii=False, indent=4)

    def Clients_info(self):
        cl_str = ""
        for client in self.client_list:
            cl_str += (f'Имя клиента:{client.name}\n'
                       f'Оплачено занятий:{client.paid_training}\n'
                       f'Пройдено занятий:{client.done_training}\n'
                       f'Депозит:{client.exp_money}\n'
                       )
        return cl_str.strip()

    def more_info(self):
        cl_str = ""
        for client in self.client_list:
            cl_str += (f'Имя клиента:{client.name}\n'
                       f'Оплачено занятий:{client.paid_training}\n'
                       f'Пройдено занятий:{client.done_training}\n'
                       f'Стоимость тренировки:{client.training_cost}\n'
                       f'Депозит:{client.exp_money}\n'
                       f'Заработано:{client.deposited_money}\n\n'
                       )
        return cl_str.strip()


    def IsThereClients(self):
        return len(self.client_list) != 0




# if __name__ == "__main__":
#     print("Запускай main_bot!!!")

