import requests
import json
import os

class EatPlusBot:

    def __init__(self):

        token = '5700849117:AAGyTAPHlWpF0IoTnogZ8aN-EU0QL_m1zwk'
        self.url = f'https://api.telegram.org/bot{token}/'

    def Start(self):

        update_id = None

        while True:

            update = self.read_new_messages(update_id)
            data = update["result"]

            if data:

                for info in data:

                    update_id = info['update_id']
                    message = str(info["message"]["text"])
                    chat_id = info["message"]["from"]["id"]
                    print(chat_id)
                    first_message = int(info["message"]["message_id"]) == 1
                    answer = self.create_answer(message, first_message)
                    self.response(answer, chat_id)

    def read_new_messages(self, update_id):

        link_req = f'{self.url}getUpdates?timeout=5'

        if update_id:

            link_req = f'{link_req}&offset={update_id + 1}'

        result = requests.get(link_req)

        return json.loads(result.content)

    def start_register(self,message):

        print('client message: ' + str(message))

        return "Qual o seu nome?"

    def create_answer(self, message, first_message):

        print('client message: ' + str(message))

        if first_message == True or message.lower() in ('oi','Oi','oi.','Oi.','oi!','Oi!'):
            return f'Eu me chamo Rafaela.{os.linesep}Vou preencher sua ficha pra você, então preciso que você me fale as informações que te pedir.{os.linesep}Podemos começar, Sim ou não?'

        if message == message in ('sim','s','Sim','sim.','Sim.'):

            self.response(self,"Qual o seu nome?")
                self.create_answer(self,"1")

            return "FINALIZADO"

        if message == message in "1":
            self.response(self,"Agora qual seu E-mail?")
             return  self.create_answer(self,"2")

        if message == message in "2":
            self.response(self,"Por fim digite sua Senha")
                return  self.create_answer(self,"3")

        if message == message in "3":
            return "Cadastro finalizado com sucesso!"



        elif message == message in ('não','n','Não','não.','Não.','nao','Nao','Nao.','nao.'):
            return 'Quando estiver pronto(a), me diga "oi" que eu venho!'

        else:
            return 'Se quiser falar comigo, só dizer "oi"!'




    def response(self, answer, chat_id):

        link_req = f'{self.url}sendMessage?chat_id={chat_id}&text={answer}'
        requests.get(link_req)
        print("answer: " + str(answer))