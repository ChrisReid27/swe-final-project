from django.urls import path
from .views import (
	CreateNewGameboardView,
	HistoryView,
	GameboardByIdView,
	GameboardByBoardCodeView,
	LeaderboardView,
)

urlpatterns = [
	# Create a new gameboard
	# Example: GET /game/
	path("game/", CreateGameboardView.as_view(), name="create-new-game"),
	
	# Get history of a user by id
	# Example: GET /history/{user:id}
	path("history/<uuid:id>/", HistoryView.as_view(), name="get-history-by-user-id"),

	# Get game by id
	# Example: GET /game/{id}
	path("game/<uuid:id>/", GameboardByIdView.as_view(), name="gameboard-detail"),

	# Get game by boardcode
	# Example: GET /game/{boardcode}
	path("game/<string:code>", GameboardByBoardCodeView.as_view(), name="gameboard_boardcode-detail"),

	# Retrieve or submit leaderboard entries
	# GET /games/{uuid}/leaderboard/
	# POST /games/{uuid}/leaderboard/
	path(
		"games/<uuid:id>/leaderboard/",
		GameboardLeaderboardView.as_view(),
		name="game-leaderboard",
	),
]
