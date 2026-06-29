import pyttsx3

class Audio:
	def __init__(self):
		self.tts = pyttsx3.init()

	def tts(self, text: str):
		self.tts.say(text)
		self.tts.runAndWait()

	def stt(self, pre: function = None):
		import speech_recognition as sr
		audio = ""

		r = sr.Recognizer()
		with sr.Microphone() as source:
			if pre:
				pre(source)
			audio = r.listen(source)

		return audio