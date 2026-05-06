/api/game/ -> generates a new game and returns it in json format
/api/game/{board_code} -> gets the gameboard of the given boardcode

The return is the same (see json below)

{
    "board_code": 8,
    "name": "Gameboard:2026-05-04 14:50:37",
    "date_created": "2026-05-04T14:50:37.065280Z",
    "questions": [
        {
            "category": "movies",
            "value": 200,
            "question_text": "Which Howard University Alumni played Black Panther in Marvel's Black Panther?",
            "answer_text": "Chadwick Boseman"
        },
        {
            "category": "movies",
            "value": 400,
            "question_text": "placeholder",
            "answer_text": "placeholder"
        },
        {
            "category": "movies",
            "value": 600,
            "question_text": "placeholder",
            "answer_text": "placeholder"
        },
        {
            "category": "movies",
            "value": 800,
            "question_text": "placeholder",
            "answer_text": "placeholder"
        },
        {
            "category": "movies",
            "value": 1000,
            "question_text": "placeholder",
            "answer_text": "placeholder"
        },
        {
            "category": "sports",
            "value": 200,
            "question_text": "Who won the 2026 Superbowl?",
            "answer_text": "Seattle Seahawks"
        },
        {
            "category": "sports",
            "value": 400,
            "question_text": "placeholder",
            "answer_text": "placeholder"
        },
        {
            "category": "sports",
            "value": 600,
            "question_text": "placeholder",
            "answer_text": "placeholder"
        },
        {
            "category": "sports",
            "value": 800,
            "question_text": "When is the most recent time, before 2026, that the Howard University Women's Basketball team made it to March Madness?",
            "answer_text": "2022"
        },
        {
            "category": "sports",
            "value": 1000,
            "question_text": "placeholder",
            "answer_text": "placeholder"
        },
        {
            "category": "tv",
            "value": 200,
            "question_text": "What is the name of the main character in Breaking Bad?",
            "answer_text": "Walter White"
        },
        {
            "category": "tv",
            "value": 400,
            "question_text": "placeholder",
            "answer_text": "placeholder"
        },
        {
            "category": "tv",
            "value": 600,
            "question_text": "placeholder",
            "answer_text": "placeholder"
        },
        {
            "category": "tv",
            "value": 800,
            "question_text": "placeholder",
            "answer_text": "placeholder"
        },
        {
            "category": "tv",
            "value": 1000,
            "question_text": "placeholder",
            "answer_text": "placeholder"
        },
        {
            "category": "celebrities",
            "value": 200,
            "question_text": "placeholder",
            "answer_text": "placeholder"
        },
        {
            "category": "celebrities",
            "value": 400,
            "question_text": "Who famously lost their diamond earrings off the coast of Bora Bora in French Polynesia?",
            "answer_text": "Kim Kardashian"
        },
        {
            "category": "celebrities",
            "value": 600,
            "question_text": "placeholder",
            "answer_text": "placeholder"
        },
        {
            "category": "celebrities",
            "value": 800,
            "question_text": "What are the names of the three books in Toni Morrison's Beloved Trilogy?",
            "answer_text": "Beloved, Jazz and Paradise"
        },
        {
            "category": "celebrities",
            "value": 1000,
            "question_text": "placeholder",
            "answer_text": "placeholder"
        },
        {
            "category": "music",
            "value": 200,
            "question_text": "Who sings the hit song California Gurls?",
            "answer_text": "Katy Perry"
        },
        {
            "category": "music",
            "value": 400,
            "question_text": "placeholder",
            "answer_text": "placeholder"
        },
        {
            "category": "music",
            "value": 600,
            "question_text": "placeholder",
            "answer_text": "placeholder"
        },
        {
            "category": "music",
            "value": 800,
            "question_text": "placeholder",
            "answer_text": "placeholder"
        },
        {
            "category": "music",
            "value": 1000,
            "question_text": "What is the name of the esteemed trumpet professor who taught at Howard for 51 years, from 1974 till 2025?",
            "answer_text": "Fred Irby III"
        }
    ]
}


/api/history/ -> gets the history of the current user in terms of leaderboard entries, formatted as such
[
    {
        "user": {
            "id": 1,
            "username": "john",
            "email": "sample@gmail.com"
        },
        "score": 200,
        "time_taken": 20
    }
]

/api/game/{board_code}/leaderboard -> GET -> gets leaderboard for given board

{
    "gameboard": 1,
    "leaderboard_entries": [
        {
            "user": {
                "id": 1,
                "username": "john",
                "email": "sample@gmail.com"
            },
            "score": 200,
            "time_taken": 20
        }
    ]
}

/api/game/{board_code}/leaderboard -> POST -> posts leaderboard information from json
{
	“score” : {number of dollars won}
	“time_taken” : {seconds taken}
}

/accounts/register/
{
	“username” : {username}
	“email” : {email address}
	“password” : {password}
	“password2” : {repeat of password to check if its the same}
}

/accounts/update_password/ -> user must be logged in to change their password
{
	“old_password” : {password}
	“new_password” : {new_password}
}

/accounts/update_email/   ->  user must be logged in to change their email
{
	“email” : {new email address}
}

/accounts/login/login -> sign in with a valid username and password

/accounts/login/logout -> signout if needed

You must create a file named “.env” in the backend/gridquiz/ folder and put the following line in it:
SECRET_KEY = secret_key_goes_here

Additionally you must create a variable in backend/gridquiz/settings.py called
LOGIN_REDIRECT_URL
Which redirects to where a successful login request should go.
