from api.REHOBAAM import REHOBAAM
from api.remote_client.OllamaClient import OllamaClient
from api.GUIManager import GUIManager
from api.Integrable import Integrable
from api.schedule.RandTimer import RandTimer
from api.ai_tools.DateTool import date_now, time_now
from api.ai_tools.WebTools import search_the_web, go_to
import time


class Test(Integrable):
	def __init__(self, core: REHOBAAM):
		self._enabled = True
		self._core = core

	def start(self):
		separator = "-"
		while self._enabled:
			try:
				prompt = input(f"{separator*30}\nyou: ")

				result = self._core.getBotManager().getMainBot().sendMessage(prompt)

				print(f"{separator*30}\nai: {result}")
			except KeyboardInterrupt:
				self._core.stop()

	def stop(self):
		self._enabled = False


class Telegram(Integrable):
	def __init__(self, core: REHOBAAM, ollama_client: str, model: str, token: str):
		super().__init__(core)
		import asyncio
		from telebot import TeleBot

		self._telebot = TeleBot(token)

		self._bot = core.getBotManager().create_author(model, ollama_client, True)
		self._core = core


	def start(self) -> None:
		#from pynput.keyboard import Key, Listener
		import asyncio, logging, keyboard
		channel_id = -5120050573

		def random_post(integration: Telegram, channel_id):
			print("Generating post...")

			text = integration._bot.generate_idea(
				"Post for Telegram channel",
				"normal",
				addotional="1000 character limit. It's important that you write the post yourself, don't add unnecessary details, and write using a minimum of characters!"
			)[1]

			cs = 1024
			chunks = [text[i:i + cs] for i in range(0, len(text), cs)]
			for chunk in chunks:
				integration._telebot.send_message(channel_id, chunk)

			print("Generated post!")


		# from 4 minutes to 20 minutes
		rt = RandTimer(60*60*2, 60*60*5, random_post, (self, channel_id))
		#rt.start()


		def on_press(event):
			if event.name.lower() == "f1":
				random_post(self, channel_id)
			elif event.name.lower() == "d":
				if keyboard.is_pressed("ctrl"):
					self.stop()
		#keyboard.on_press(on_press, False)


		def send_msg(target_chat: int, msg: str) -> None:
			"""
			Send message to chat by id by username

			target_chat: int - id of chat
			msg: str - message content
			"""
			self._telebot.send_message(chat_id=target_chat, text=msg)

		self._core.getToolsMan().add_tool(send_msg)


		@self._telebot.message_handler(content_types=["text"])
		def on_msg(msg):
			if msg.text.startswith('/'):
				return
			print(f"{msg.from_user.first_name}:", msg.text)
			res = self._bot.sendMessage(msg.text, tools_man=self._core.getToolsMan())
			if res == "":
				self._telebot.reply_to(msg, "ERROR HAS OCCORUPTED")
				return
			print("Response:", res)
			self._telebot.reply_to(msg, res)

		try:
			self._telebot.infinity_polling()
		except KeyboardInterrupt:
			self.stop()
		except Exception as e:
			print(f"Bot crashed: {e}")
			import traceback
			traceback.print_exc()

	def stop(self) -> None:
		print("Stop")
		self._telebot.stop_polling()
		self._telebot.stop_bot()
		exit(0)


def clear_console():
	import os
	import platform

	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")

def main():
	ip = input("Enter AI-server ip (default: localhost): ") or "localhost"
	port = int(input("Enter AI-server port (default: 11434): ") or 11434)
	sleep_time = 0.2

	ollama = OllamaClient(ip, port, "")

	models = ollama.getModels().models
	select_models = {}
	last_id = 0
	for model in models:
		print(str(last_id)+". "+model.model)
		select_models[last_id] = model.model
		last_id += 1

	selected_id = int(input("select model by id: "))
	model = select_models[selected_id]

	ollama.loadModel(model)

	api = REHOBAAM()
	api.getToolsMan().add_tools([
		date_now, time_now,
		search_the_web, go_to
	])

	bot_api = api.getBotManager()
	bot = bot_api.create_normal(model, ollama, fancy_mode=False)

	clear_console()

	print(f"{api.getName()} {api.getVersion()}")
	print()
	print("Press Ctrl+D to exit at any time")

	bot_api.setMainBot(bot)

	#api.integrate(GUIManager(api, 'original', mode='console', bot=bot))
	#api.integrate("Test", Test)
	api.integrate("Telegram", Telegram, ollama_client=ollama, model=model, token='8491872176:AAFDEg9rfNZMppJcw4j7ONMQtBywhZRyJYk')

	api.start()
	if api.is_started():
		api.stop()

	#clear_console()
	ollama.unloadModel(model)

if __name__ == "__main__":
	main()
