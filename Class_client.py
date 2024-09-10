import json
import os.path


class Client():
    def __init__(self,client_name):
        self.name = client_name
        self.paid_training = 0
        self.done_training = 0
        self.deposited_money = 0
        self.training_cost = 0
        self.exp_money = 0

    def Client_paid_training(self, session_paid, t_cost):
        self.paid_training = session_paid
        self.training_cost = t_cost
        self.money_expected()

    def Client_comp_training(self):
        self.paid_training -= 1
        self.done_training += 1
        self.Client_deposites_total()
        self.exp_money = self.exp_money - self.training_cost

    def Client_info(self):
        print(self.name, 'осталось оплачено', self.paid_training,'\nпройдено тренировок', self.done_training)

    def Client_to_dict(self):
        return {
                'Client name ' : self.name,
                'paid training ' : self.paid_training,
                'Complete training ' : self.done_training,
                'Deposited_money' : self.deposited_money,
                'Training_cost' : self.training_cost
                }

    def Client_deposites_total(self):
        self.deposited_money = self.done_training * self.training_cost


    def money_expected(self):
        self.exp_money = self.paid_training * self.training_cost



    # def Client_save_json(self, filename):
    #     if os.path.isfile(filename):
    #         with open(filename, 'r') as file:
    #             data = json.load(file)
    #         data.append(self.Client_to_dict())
    #     else:
    #         data = [self.Client_to_dict()]
    #     with open(filename, 'w') as file:
    #         json.dump(data,file,ensure_ascii=False, indent=4)

