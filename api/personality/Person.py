class Person:
	def __init__(self, 
				full_name: list = ["Bob", "Brown"], age: int = 22, gender: str = "male", mbti: str = "ESFP",
				hobbies: list = ["painting"], occupation: str = "writing", address: str = "",
				description: str = "Average Person", languages: list = ["English"], main_language: str = "English",
				education: str = "Math", interests: list = ["reading"], skills: list = ["sports"],
				personality_traits: list = ["extroverted", "average", "friendly"]):
		self._full_name = full_name
		self._age = age
		self._gender = gender
		self._mbti = mbti
		self._hobbies = hobbies
		self._occupation = occupation
		self._address = address
		self._description = description
		self._languages = languages
		self._main_language = main_language
		self._education = education
		self._interests = interests
		self._skills = skills
		self._personality_traits = personality_traits

	def get_name(self): return ' '.join(self._full_name)
	def get_first_name(self): return self._full_name[1]
	def get_last_name(self): return self._full_name[0]

	def get_age(self): return self._age

	def get_gender(self): return self._gender
	def get_mbti(self): return self._mbti

	def get_hobbies(self): return self._hobbies
	def get_occupation(self): return self._occupation

	def get_address(self): return self._address
	def get_description(self): return self._description

	def get_languages(self): return self._languages
	def get_main_language(self): return self._main_language

	def get_education(self): return self._education
	def get_interests(self): return self._interests
	def get_skills(self): return self._skills
	def get_personality_traits(self): return self._personality_traits

	def get_summary(self) -> dict:
		return {
			"full_name": self._full_name, "age": self._age, "gender": self._gender, "mbti": self._mbti,
			"hobbies": self._hobbies, "occupation": self._occupation, "address": self._address, "description": self._description,
			"languages": self._languages, "main_language": self._main_language, "education": self._education, "interests": self._interests,
			"skills": self._skills, "personality_traits": self._personality_traits
		}
	
	def __str__(self) -> str:
		return f"""{' '.join(self._full_name)}, age {self._age}, gender {self._gender},
mbti: {self._mbti}, hobbies: {self._hobbies}, occupation: {self._occupation},
address: {self._address}, description: {self._description},
languages: {self._languages}, main language: {self._main_language},
education: {self._education}, interests: {self._interests},
skills: {self._skills}, personality_traits: {self._personality_traits}
"""