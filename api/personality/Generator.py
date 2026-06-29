from faker import Faker
from api.personality.Person import Person
from api.personality.CreatorPerson import CreatorPerson
from api.personality.AlivePerson import AlivePerson
from api.remote_client.OllamaClient import OllamaClient
import random
import json

class Generator:
	def __init__(self):
		self._faker = Faker()
		# locales содержит названия локалей; используем их как список языков для выбора
		self._languages = list(self._faker.locales)

		# Поддерживаемые интересы — расширенный и разнообразный набор
		self._interests_support = list({
			"reading", "traveling", "gaming", "cooking", "sports", "music", "art",
			"technology", "photography", "writing", "hiking", "gardening", "movies",
			"dancing", "yoga", "meditation", "fishing", "knitting", "board games",
			"programming", "DIY", "collecting", "astronomy", "history", "languages",
			"blogging", "podcasting", "volunteering", "baking", "coffee brewing"
		})

		# Образование — добавлены варианты и унифицированы названия
		self._educations_support = list({
			"High School", "Associate Degree", "Bachelor's Degree", "Master's Degree",
			"PhD", "Professional Certificate", "Diploma", "Vocational Training"
		})

		# Навыки — удалены пустые/повторяющиеся элементы, добавлены полезные навыки
		self._skills_support = list({
			"Python", "Java", "JavaScript", "C++", "C#", "Ruby", "Go", "Rust",
			"Data Analysis", "Machine Learning", "Web Development", "Mobile Development",
			"DevOps", "Cloud Computing", "Graphic Design", "UI/UX", "Project Management",
			"SQL", "NoSQL", "Cybersecurity", "Testing", "Embedded Systems", "PixelArt"
		})

		# Черты личности — расширенный набор
		self._personality_traits_support = list({
			"introverted", "extroverted", "agreeable", "disagreeable", "conscientious",
			"open-minded", "neurotic", "calm", "empathetic", "assertive", "curious",
			"practical", "idealistic", "optimistic", "pessimistic", "humorous",
			"serious", "adventurous", "cautious", "loyal", "independent"
		})


	def _unique_sample(self, source_list, k):
		if not source_list: return []
		if len(source_list) <= k: return random.sample(source_list, len(source_list))
		return random.sample(source_list, k)


	def generate(self) -> Person:
		description = self._faker.text(max_nb_chars=200)
		gender = self._faker.random_element(elements=["male", "female"])

		if gender == "male":
			first_name = self._faker.first_name_male()
			last_name = self._faker.last_name_male()
		else:
			first_name = self._faker.first_name_female()
			last_name = self._faker.last_name_female()

		age = self._faker.random_int(min=8, max=45)

		mbti_by_characters = [["I", "E"], ["S", "N"], ["T", "F"], ["J", "P"]]
		mbti = "".join([self._faker.random_element(elements=pair) for pair in mbti_by_characters])

		hobbies = self._unique_sample(self._interests_support, random.randint(1, 5))
		occupation = self._faker.job()
		interests = self._unique_sample(self._interests_support, random.randint(1, 5))

		address = self._faker.address()

		languages = self._unique_sample(self._languages, random.randint(1, 5))
		main_language = languages[0] if languages else None

		if age > 20:
			education = self._faker.random_element(elements=self._educations_support)
		else:
			education = "Haven't received it yet"

		if age > 10:
			skills = self._unique_sample(self._skills_support, random.randint(1, 5))
		else:
			education = "Haven't received it yet"

		personality_traits = self._unique_sample(self._personality_traits_support, random.randint(1, 5))
		return Person(
			full_name=[last_name, first_name], age=age, gender=gender, mbti=mbti, hobbies=hobbies,
			occupation=occupation, address=address, description=description,
			languages=languages, main_language=main_language, education=education,
			interests=interests, skills=skills, personality_traits=personality_traits
		)


	def generate_use_ai(self, is_creator: bool, model: str, ollama: OllamaClient) -> Person:
		prompt_live = """
Generate person according to the following format: \"
{
  "profile": {  
       // Общая информация о персонаже  
       "name": {  
         "nickname": "",          // Псевдоним
         "firstName": "",         // Реальное имя  
         "lastName": ""              // Фамилия  
       },  
       // Физическое описание персонажа  
       "appearance": {  
         "gender": "",               // Пол (male или female)  
         "age": "",                  // Возраст  
         "height": "",               // Рост (в см или м)  
         "weight": "",               // Вес (в кг)  
         "hairColor": "",         // Цвет волос  
         "eyeColor": "",          // Цвет глаз  
         "style": ""                 // Стили и визуальные характеристики (например, casual, urban, futuristic)  
       },  
       // Личностные особенности и мотивации  
       "personality": {  
         "traits": [],               // Черты характера (например, introverted, aggressive, friendly)  
         "communicationStyle": [], // Стиль общения (например, formal, sarcastic, direct)  
         "motivations": []        // Мотивации и цели персонажа  
       },  
       // Биографические данные и события из прошлого  
       "background": {  
         "lifeEvents": [],        // Ключевые события в жизни персонажа  
         "educations": [],         // Образования или профессиональные обучения, можно хоть, 3, хоть 1, хоть 10; но не перебарщиваем если не требуеться
         "occupations": []         // Род деятельностей или профессии, можно хоть, 3, хоть 1, хоть 10; но не перебарщиваем если не требуеться
       },  
       // Социальные связи и отношения  
       "relationships": {
         "friends": {
           "friends_now": {
          "friend1": "", // friend1 заменить на имя или ник, а в "" краткая информайия
          "friend2": "", // friend2 заменить на имя или ник, а в "" краткая информайия
          "friend3": "" // friend3 заменить на имя или ник, а в "" краткая информайия
          
          // продолжаем сколько угодно, можно хоть, 3, хоть 1, хоть 10; но не перебарщиваем если не требуеться
           }, // нынещние друзья
           "no_friends_more": {
          "friend1": "", // friend1 заменить на имя или ник, а в "" краткая информайия
          "friend2": "", // friend2 заменить на имя или ник, а в "" краткая информайия
          "friend3": "" // friend3 заменить на имя или ник, а в "" краткая информайия
          
          // продолжаем сколько угодно, можно хоть, 3, хоть 1, хоть 10; но не перебарщиваем если не требуеться
           }, // бывшие друзья
           "dead_friends": {
          "friend1": "", // friend1 заменить на имя или ник, а в "" краткая информайия
          "friend2": "", // friend2 заменить на имя или ник, а в "" краткая информайия
          "friend3": "" // friend3 заменить на имя или ник, а в "" краткая информайия
          
          // продолжаем сколько угодно, можно хоть, 3, хоть 1, хоть 0, хоть 10; но не перебарщиваем если не требуеться
           } // уже мертвые друзья
         }, // Друзья и контакты  
         "family": [],               // Семейные связи  
         "enemies": [] // Враждебные контакты или соперники, бывшин друзья в отдельном списке, и то бывшие друзья не обязательно враги 
       },  
       // Онлайн-профиль и цифровая идентичность. Может отсуствовать если не использует интернет.
       "digitalProfile": {  
          "platforms": {
            "account1": {
              "socialmedia": "", // url соцсети
              "info": "" // краткая информация
            }, // account1 меняем на ник.
            "account2": {
              "socialmedia": "", // url соцсети
              "info": "" // краткая информация
            }, // account2 меняем на ник.
            "account3": {
              "socialmedia": "", // url соцсети
              "info": "" // краткая информация
            } // account3 меняем на ник.
           // продолжаем сколько угодно, можно хоть, 3, хоть 1, хоть 10; но не перебарщиваем если самому боту не необходимо
          }         // Платформы и аккаунты (например, Twitter, Facebook, Instagram)
       },  
       // Предпочтения и увлечения  
       "preferences": {  
         "likes": [],                // Предпочтения и интересы  
         "dislikes": []              // Антипатии и нежелательные темы  
       },  
       // Технические данные, связанные с онлайн-деятельностью, если конечно использует
       "tech": {  
         "devices": [],              // Устройства, используемые персонажем (смартфоны, ПК и пр.)  
         "software": []              // Программное обеспечение и используемые платформы  
       },  
       // Дополнительные заметки или особая информация  
       "notes": ""                      // Дополнительная информация или комментарии  
  }
}
\"
Not using comments, spaces and line breaks
"""
		prompt_creator = """
Generate person according to the following format: \"
{
  "profile": {  
       // Общая информация о персонаже  
       "name": {  
         "nickname": "",          // Псевдоним
         "firstName": "",         // Реальное имя  
         "lastName": ""              // Фамилия  
       },  
       // Физическое описание персонажа  
       "appearance": {  
         "gender": "",               // Пол (male или female)  
         "age": "",                  // Возраст  
         "height": "",               // Рост (в см или м)  
         "weight": "",               // Вес (в кг)  
         "hairColor": "",         // Цвет волос  
         "eyeColor": "",          // Цвет глаз  
         "style": ""                 // Стили и визуальные характеристики (например, casual, urban, futuristic)  
       },  
       // Личностные особенности и мотивации  
       "personality": {  
         "traits": [],               // Черты характера (например, introverted, aggressive, friendly)  
         "communicationStyle": [], // Стиль общения (например, formal, sarcastic, direct)  
         "motivations": []        // Мотивации и цели персонажа  
       },  
       // Биографические данные и события из прошлого  
       "background": {  
         "lifeEvents": [],        // Ключевые события в жизни персонажа  
         "educations": [],         // Образования или профессиональные обучения, можно хоть, 3, хоть 1, хоть 10; но не перебарщиваем если не требуеться
         "occupations": []         // Род деятельностей или профессии, можно хоть, 3, хоть 1, хоть 10; но не перебарщиваем если не требуеться
       },  
       // Социальные связи и отношения  
       "relationships": {
         "friends": {
           "friends_now": {
          "friend1": "", // friend1 заменить на имя или ник, а в "" краткая информайия
          "friend2": "", // friend2 заменить на имя или ник, а в "" краткая информайия
          "friend3": "" // friend3 заменить на имя или ник, а в "" краткая информайия
          
          // продолжаем сколько угодно, можно хоть, 3, хоть 1, хоть 10; но не перебарщиваем если не требуеться
           }, // нынещние друзья
           "no_friends_more": {
          "friend1": "", // friend1 заменить на имя или ник, а в "" краткая информайия
          "friend2": "", // friend2 заменить на имя или ник, а в "" краткая информайия
          "friend3": "" // friend3 заменить на имя или ник, а в "" краткая информайия
          
          // продолжаем сколько угодно, можно хоть, 3, хоть 1, хоть 10; но не перебарщиваем если не требуеться
           }, // бывшие друзья
           "dead_friends": {
          "friend1": "", // friend1 заменить на имя или ник, а в "" краткая информайия
          "friend2": "", // friend2 заменить на имя или ник, а в "" краткая информайия
          "friend3": "" // friend3 заменить на имя или ник, а в "" краткая информайия
          
          // продолжаем сколько угодно, можно хоть, 3, хоть 1, хоть 0, хоть 10; но не перебарщиваем если не требуеться
           } // уже мертвые друзья
         }, // Друзья и контакты  
         "family": [],               // Семейные связи  
         "enemies": [] // Враждебные контакты или соперники, бывшин друзья в отдельном списке, и то бывшие друзья не обязательно враги 
       },  
       // Онлайн-профиль и цифровая идентичность. Может отсуствовать если не использует интернет.
       "digitalProfile": {  
          "platforms": {
            "account1": {
              "socialmedia": "", // url соцсети
              "info": "" // краткая информация
            }, // account1 меняем на ник.
            "account2": {
              "socialmedia": "", // url соцсети
              "info": "" // краткая информация
            }, // account2 меняем на ник.
            "account3": {
              "socialmedia": "", // url соцсети
              "info": "" // краткая информация
            } // account3 меняем на ник.
           // продолжаем сколько угодно, можно хоть, 3, хоть 1, хоть 10; но не перебарщиваем если самому боту не необходимо
          }         // Платформы и аккаунты (например, Twitter, Facebook, Instagram)
       },  
       // Предпочтения и увлечения  
       "preferences": {  
         "likes": [],                // Предпочтения и интересы  
         "dislikes": []              // Антипатии и нежелательные темы  
       },  
       // Технические данные, связанные с онлайн-деятельностью, если конечно использует
       "tech": {  
         "devices": [],              // Устройства, используемые персонажем (смартфоны, ПК и пр.)  
         "software": []              // Программное обеспечение и используемые платформы  
       },  
       // Дополнительные заметки или особая информация  
       "notes": ""                      // Дополнительная информация или комментарии  
  }
}
\"
Not using comments, spaces and line breaks
"""
		profile = ollama.generate(model, prompt_creator if is_creator else prompt_live, think=True, temperature=0.7).response
		data = json.loads(profile)

		if is_creator:
			return CreatorPerson(**data.get("profile", {}))
		return AlivePerson(**data.get("profile", {}))

	@staticmethod
	def get_person(is_creator: bool, **kwargs):
		if is_creator:
			return CreatorPerson(**kwargs)
		return AlivePerson(**kwargs)