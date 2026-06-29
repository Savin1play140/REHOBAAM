from typing import Any

class AlivePerson:
	def __init__(self,
		name: dict[str, str], appearance: dict[str, str],
		personality: dict[str, list[str]],
		background: dict[str, list[str]],
		relationships: dict[str, Any],
		digitalProfile: dict[str, dict[str, dict[str, str]]],
		preferences: dict[str, list[str]], tech: dict[str, list[str]],
		notes: str):
		self._name = name
		self._app = appearance
		self._person = personality
		self._bg = background
		self._rs = relationships
		self._d_p = digitalProfile
		self._prefs = preferences
		self._tech = tech
		self._notes = notes

	def get_nickname(self)->str: return self._name.get("nickname", "Null001")
	def get_firstname(self)->str: return self._name.get("firstName", "Bob")
	def get_lastname(self)->str: return self._name.get("lastName", "Afton")
	def get_name(self)->str: return f"{self.get_firstname()} {self.get_lastname()}"

	def get_gender(self)->str: return self._app.get("gender", "male")
	def get_age(self)->int: return int(self._app.get("age", 34))
	def get_heigth(self)->str: return self._app.get("height", "174cm")
	def get_weight(self)->str: return self._app.get("weight", "70kg")
	def get_hair_color(self)->str: return self._app.get("hairColor", "black")
	def get_eye_color(self)->str: return self._app.get("eyeColor", "quarries")
	def get_style(self)->str: return self._app.get("style", "")

	def get_traits(self)->list: return self._person.get("traits", [])
	def get_communication_style(self)->list: return self._person.get("communicationStyle", [])
	def get_motivations(self)->list: return self._person.get("motivations", [])

	def get_life_events(self)->list: return self._bg.get("lifeEvents", [])
	def get_educations(self)->list: return self._bg.get("educations", [])
	def get_occupations(self)->list: return self._bg.get("occupations", [])

	def get_friends_now(self)->dict: return self._rs.get("friends").get("friend_now", {})
	def get_no_friends_more(self)->dict: return self._rs.get("friends").get("no_friends_more", {})
	def get_dead_friends(self)->dict: return self._rs.get("friends").get("dead_friends", {})
	def get_family(self)->list: return self._rs.get("family", [])
	def get_enemies(self)->list: return self._rs.get("enemies", [])

	def get_platforms(self)->dict: return self._d_p.get("platforms", {})

	def get_likes(self)->list: return self._prefs.get("likes", [])
	def get_dislikes(self)->list: return self._prefs.get("dislikes", [])

	def get_devices(self)->list: return self._tech.get("devices", [])
	def get_software(self)->list: return self._tech.get("software", [])

	def get_notes(self)->str: return self._notes


	def get_summary(self)->dict:
		return {
			"name": self._name, "appearance": self._app, "personality": self._person,
			"background": self._bg, "relationships": self._rs, "digitalProfile": self._d_p,
			"preferences": self._prefs, "tech": self._tech, "notes": self._notes
		}


	def __str__(self)->str:
		platforms = []
		for name, data in self.get_platforms().items():
			platforms.append(": ".join([name, data.get("socialmedia", "")]))
		platforms_str = ", ".join(platforms)

		return f"""{self.get_firstname()} {self.get_lastname}, nickname: {self.get_nickname()}.
Age: {str(self.get_age)} years, gender: {self.get_gender()}, height: {self.get_heigth()}, weight: {self.get_weight()},
Hair color: {self.get_hair_color()}, eye color: {self.get_eye_color()}, style: {self.get_style()}.
Traits: {str(self.get_traits())}, communication style: {str(self.get_communication_style())},
motivations: [{", ".join(self.get_motivations())}]. Live events: [{", ".join(self.get_life_events())}],
educations: [{", ".join(self.get_educations())}], occupations: [{", ".join(self.get_occupations())}].
Frends: [{", ".join(self.get_friends_now())}], former friends: [{", ".join(self.get_no_friends_more())}],
Dead friends: [{", ".join(self.get_dead_friends())}], family: [{", ".join(self.get_family())}],
enemies: [{", ".join(self.get_enemies())}]. Social platforms: [{platforms_str}].
Likes: [{", ".join(self.get_likes())}], dislikes: [{", ".join(self.get_dislikes())}].
Devices: [{", ".join(self.get_devices())}], software: [{", ".join(self.get_software())}].
Notes: {self.get_notes()}
"""