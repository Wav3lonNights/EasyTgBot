import requests
import threading
import time

last_message = ''

__version__ = "1.1.0"
print('EasyTgBot v' + __version__ + '\nMade with clean requests by wav3lon.\n')

class Exceptions():
	class BadRequest(Exception):
		pass
	class InvalidToken(Exception):
		pass

def get_updates(api,token,offset=0):
	global response
	response = None
	try: response = requests.get(f'{str(api)}getUpdates?offset={str(offset)}').json()
	except requests.exceptions.ConnectTimeout: 
		get_updates(api,token)
	if response['ok']==False:
		if response['error_code']==404:
			raise Exceptions.InvalidToken('Не удалось подключиться к телеграму. Правильно ли вы ввели токен бота?')
		else:
			raise Exceptions.BadRequest('Произошла неизвестная ошибка. Статус: ' + str(response.status_code))
	return response['result']

class создать(object):
	def __init__(self, token):
		super(создать, self).__init__()
		self.Token = token
		self.TelegramApiBot = f'https://api.telegram.org/bot{self.Token}/'
		if requests.get(f'{str(self.TelegramApiBot)}sendMessage?chat_id=0&text="0"').json()['error_code']==404: raise Exceptions.InvalidToken('Не удалось подключиться к телеграму. Правильно ли вы ввели токен бота?')

	def отправить_сообщение(self,айди_чата,сообщение):
		BotParams = {
			'chat_id': айди_чата,
			'text': сообщение
		}
		if not type(айди_чата) == int: raise ValueError('Айди чата должен быть числом. не ' + str(type(айди_чата)).replace("<class ",'').replace('>',''))
		if not type(сообщение) == str: raise ValueError('Сообщение должно быть строкой. не ' + str(type(сообщение)).replace("<class ",'').replace('>',''))
		response = requests.get(self.TelegramApiBot+'sendMessage', json=BotParams)
		if response.status_code == 200:
			pass
		else:
			raise Exceptions.BadRequest('Произошла неизвестная ошибка. Статус: ' + str(response.status_code))

		return response.status_code

	def триггер_сообщение(self, функция,оффсет=0):
		def check_message(функция,оффсет):
			global last_message
			if not type(оффсет) == int: raise ValueError('Оффсет должен быть числом. не ' + str(type(айди_чата)).replace("<class ",'').replace('>',''))
			Chatid = get_updates(self.TelegramApiBot,self.Token)[-1]['update_id']
			messages = get_updates(self.TelegramApiBot,self.Token,Chatid)
			for message in messages:
				if not last_message==message['message']['text']:
					if Chatid < message['update_id']:
						print('[log] сообщение найдено')
						update_id = message['update_id']
						try:
							# print(f"ID пользователя: {message['message']['chat']['id']}, Сообщение: {message['message']['text']}")
							last_message = message['message']['text']
							функция(message['message']['text'],message['message']['chat']['id'])
						except KeyError:
							pass
						break
		threading.Thread(target=check_message,args=[функция,оффсет]).start()
		time.sleep(0.15)