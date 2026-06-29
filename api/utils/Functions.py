def get_top_three_shortest(strings):
	"""
	Returns the three shortest strings from a list of strings.
	If there are fewer than three strings, returns all of them.
	"""
	if not strings:
		return []

	sorted_strings = sorted(strings, key=len)
	return sorted_strings[:3]  # Return the first three shortest strings

# Get top three shortest chat messages
def GTTSCM(msgs) -> list[dict]:
	"""
	Returns the three shortest chat messages from a list of messages.
	If there are fewer than three messages, returns all of them.
	"""
	sorted_msgs = sorted(msgs, key=lambda x: len(x['content']))
	return sorted_msgs[:3]  # Return the first three shortest messages

# Get top three shortest chat messages in history
def GTTSCM_IH(history: dict) -> dict:
	"""
	Returns sorted history by the length of the 'content' field in each every messages.
	If the history is empty, returns an empty list.
	"""
	items = list(history.items())
	sorted_items = sorted(items, key=lambda item: len(item[1]['content']))
	return dict(sorted_items[:3])  # Return the first three sorted items

def get_key_in_dict(dict, value):
	"""
	Returns the key for a given value in a dictionary.
	If the value is not found, returns None.
	"""
	for k, v in dict.items():
		if v == value:
			return k
	return None

def get_key_in_list(list, value):
	"""
	Returns the index of a given value in a list.
	If the value is not found, returns None.
	"""
	try:
		return list.index(value)
	except ValueError:
		return None

def set_console_title(title):
	"""
	Sets the title of the console window.
	"""
	import sys
	if sys.platform == "win32":
		import ctypes
		ctypes.windll.kernel32.SetConsoleTitleW(title)
	elif sys.platform == "linux" or sys.platform == "darwin":
		print(f"\033]0;{title}\a", end='', flush=True)
	else:
		raise NotImplementedError("Unsupported platform for setting console title.")
	
def clear_console():
	import os
	import platform

	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")

def sha256_hash(text: str):
	"""
	Returns the SHA-256 hash of the given text.
	"""
	import hashlib
	return hashlib.sha256(text.encode('utf-8')).hexdigest()

def system_prompt(person):
	prompt = f"""You are {person.get_firstname()}, your features: 
{str(person)}
Your answers should be based on this information . You are a human-like, not an AI. Don't use RP talk.
When speaking like a human, the text should not be long if it is not necessary.
You don't have a creator, you have family: [{", ".join(person.get_family())}], but you don't remember them."""
	return prompt

def run(worker, *args):
	return worker.start(*args)

from multiprocessing import Process
def new_process(obj, *args) -> Process:
	return Process(target=run, args=(obj, *args))