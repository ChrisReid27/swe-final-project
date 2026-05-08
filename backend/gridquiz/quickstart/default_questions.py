from .models import Question


DEFAULT_QUESTION_DATA = [
	{
		"category": "movies",
		"value": 200,
		"question_text": "This Howard special movie question is about a Chadwick Boseman role.",
		"answer_text": "Black Panther",
		"howard": True,
	},
	{
		"category": "movies",
		"value": 400,
		"question_text": "This 1999 sci-fi film stars Keanu Reeves as Neo.",
		"answer_text": "The Matrix",
		"howard": False,
	},
	{
		"category": "movies",
		"value": 600,
		"question_text": "This 2010 Christopher Nolan film layers dreams within dreams.",
		"answer_text": "Inception",
		"howard": False,
	},
	{
		"category": "movies",
		"value": 800,
		"question_text": "This space epic follows a team traveling through a wormhole.",
		"answer_text": "Interstellar",
		"howard": False,
	},
	{
		"category": "movies",
		"value": 1000,
		"question_text": "This 1994 prison drama is based on a Stephen King novella.",
		"answer_text": "The Shawshank Redemption",
		"howard": False,
	},
	{
		"category": "music",
		"value": 200,
		"question_text": "This Howard special music question is about a singer, songwriter, and pianist who attended the school at just 15 years old.",
		"answer_text": "Roberta Flack",
		"howard": True,
	},
	{
		"category": "music",
		"value": 400,
		"question_text": "This singer released the album 'Thriller'.",
		"answer_text": "Michael Jackson",
		"howard": False,
	},
	{
		"category": "music",
		"value": 600,
		"question_text": "This artist released the song 'Blinding Lights'.",
		"answer_text": "The Weeknd",
		"howard": False,
	},
	{
		"category": "music",
		"value": 800,
		"question_text": "This rapper released the album 'To Pimp a Butterfly'.",
		"answer_text": "Kendrick Lamar",
		"howard": False,
	},
	{
		"category": "music",
		"value": 1000,
		"question_text": "This British singer is known for the album '25'.",
		"answer_text": "Adele",
		"howard": False,
	},
	{
		"category": "sports",
		"value": 200,
		"question_text": "This Howard special sports question is about the animal mascot that represents the school and it's sports teams.",
		"answer_text": "Bison",
		"howard": True,
	},
	{
		"category": "sports",
		"value": 400,
		"question_text": "This annual football championship game crowns the NFL champion.",
		"answer_text": "Super Bowl",
		"howard": False,
	},
	{
		"category": "sports",
		"value": 600,
		"question_text": "This Argentine soccer star led his country to the 2022 World Cup title.",
		"answer_text": "Lionel Messi",
		"howard": False,
	},
	{
		"category": "sports",
		"value": 800,
		"question_text": "This tennis tournament is the oldest major played on grass.",
		"answer_text": "Wimbledon",
		"howard": False,
	},
	{
		"category": "sports",
		"value": 1000,
		"question_text": "This golfer won 15 major championships.",
		"answer_text": "Tiger Woods",
		"howard": False,
	},
	{
		"category": "tv",
		"value": 200,
		"question_text": "This Howard special TV question is about a sitcom that aired on ABC starring alumnus Anthony Anderson.",
		"answer_text": "Black-ish",
		"howard": True,
	},
	{
		"category": "tv",
		"value": 400,
		"question_text": "This sitcom features the characters Ross, Rachel, and Chandler.",
		"answer_text": "Friends",
		"howard": False,
	},
	{
		"category": "tv",
		"value": 600,
		"question_text": "This fantasy series is based on George R. R. Martin novels.",
		"answer_text": "Game of Thrones",
		"howard": False,
	},
	{
		"category": "tv",
		"value": 800,
		"question_text": "This mockumentary sitcom follows the employees of Dunder Mifflin.",
		"answer_text": "The Office",
		"howard": False,
	},
	{
		"category": "tv",
		"value": 1000,
		"question_text": "This drama follows Walter White's transformation into Heisenberg.",
		"answer_text": "Breaking Bad",
		"howard": False,
	},
	{
		"category": "celebrities",
		"value": 200,
		"question_text": "This Howard special celebrity question is about an actor who played Black Panther.",
		"answer_text": "Chadwick Boseman",
		"howard": True,
	},
	{
		"category": "celebrities",
		"value": 400,
		"question_text": "This actress starred as Katniss Everdeen in The Hunger Games.",
		"answer_text": "Jennifer Lawrence",
		"howard": False,
	},
	{
		"category": "celebrities",
		"value": 600,
		"question_text": "This comedian and TV host is known for The Daily Show.",
		"answer_text": "Trevor Noah",
		"howard": False,
	},
	{
		"category": "celebrities",
		"value": 800,
		"question_text": "This actress and producer played Princess Leia in Star Wars.",
		"answer_text": "Carrie Fisher",
		"howard": False,
	},
	{
		"category": "celebrities",
		"value": 1000,
		"question_text": "This controversial entrepreneur founded SpaceX and Tesla.",
		"answer_text": "Elon Musk",
		"howard": False,
	},
]


def seed_default_questions():
	if Question.objects.exists():
		return Question.objects.count()

	Question.objects.bulk_create([Question(**question_data) for question_data in DEFAULT_QUESTION_DATA])
	return Question.objects.count()