from api.utils.Translator import Translator
import urwid
import threading

class Console:
	def __init__(self, logger, title, translate_lang, bot=None):
		self.history_box = urwid.ListBox(urwid.SimpleFocusListWalker([]))
		self.title = title
		self.header = urwid.AttrMap(
			urwid.Text(self.title, align='center'), 'bios_title')
		self.edit = urwid.Edit("►")
		self.view = urwid.Frame(
			self.history_box,
			header=self.header,
			footer=urwid.AttrWrap(self.edit, 'edit')
		)
		self._bot = bot
		self._logger = logger
		self._stopped = False
		self._lang = translate_lang
		self._translate = Translator(self._logger, "en" if translate_lang == "original" else translate_lang)
		self._current_thread = None

	def setBot(self, bot):
		self._bot = bot

	def setTitle(self, title):
		self.title = title
		self.header.original_widget.set_text(self.title)

	def run(self):
		palette = [
			('background', 'default', 'light gray'),
			('edit', 'light gray', 'dark blue', 'bold'),
			('text', 'dark blue', 'light gray'),
			('bot', 'dark blue', 'light gray', 'bold'),
			('user', 'dark blue', 'light gray', 'bold'),
			('bios_title', 'light gray', 'dark blue', 'bold'),
		]
		main_widget = urwid.AttrMap(self.view, 'background')
		loop = urwid.MainLoop(main_widget, palette, unhandled_input=self.handle_input)
		self.loop = loop
		self.view.set_focus('footer')
		try:
			loop.run()
		finally:
			self._stopped = True

	def stop(self):
		if self._stopped:
			return
		self._stopped = True
		try:
			if hasattr(self, 'loop') and self.loop is not None:
				try:
					self.loop.stop()
					return
				except Exception:
					pass
		except Exception:
			pass
		raise urwid.ExitMainLoop()

	def handle_input(self, key):
		if key == 'enter':
			command = self.edit.edit_text
			if command == '': return
			self.add_user_message(command.strip())
			self.edit.edit_text = ""
			#asyncio.run(self.ai_response(command.strip()))
			if self._current_thread and self._current_thread.is_alive():
				self._current_thread.join()
			self._current_thread = threading.Thread(target=self.process_command, args=(command.strip(),))
			self._current_thread.start()
		elif key == 'ctrl enter':
			self.edit.edit_text += "\n"
		elif key == 'tab':
			self.edit.edit_text += '\t'
		elif key in ('esc', 'ctrl d'):
			self._logger.info("User stopped gui")
			self.stop()
		elif key == 'up':
			self._logger.debug("User shifted the focus up")
			self.history_box.focus_position = max(0, self.history_box.focus_position - 1)
		elif key == 'down':
			self._logger.debug("User shifted the focus down")
			self.history_box.focus_position = min(len(self.history_box.body) - 1, self.history_box.focus_position + 1)
		elif key == "f1":
			raise Exception("Manually called")
		
	def ai_response(self, message):
		if self._bot == None:
			self.bot_response(message)
			return
		response = self._bot.sendMessage(message)
		if self._lang == "original":
			response = response
		else:
			response = self._translate.translate(response)
		response = response.strip()
		self.add_bot_message(response)

	def process_command(self, command: str):
		command = command.strip()
		self.edit.edit_text = ""
		self.ai_response(command)

	def bot_response(self, command):
		response =  "Error, bot not initialized\n"
		self.add_bot_message(response)

	def add_user_message(self, message):
		msg_widget = urwid.Text(('user', "► " + message))
		self.history_box.body.append(msg_widget)
		self.history_box.focus_position = len(self.history_box.body) - 1

	def add_bot_message(self, message):
		msg_widget = urwid.Text(('bot', " "+message))
		self.history_box.body.append(msg_widget)
		self.history_box.focus_position = len(self.history_box.body) - 1
