from datetime import datetime

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.staticfiles import finders

# import models and serializers
from .models import Gameboard, Leaderboard, LeaderboardEntry, Question, User

from .serializers import (
	UserSerializer, 
	LeaderboardEntrySerializer, 
	LeaderboardSerializer, 
	QuestionSerializer, 
	GameboardSerializer,	
)

User = get_user_model()

# import other scripts
from .randomBoard import *


class CreateGameboardView(APIView):
	"""
	GET /game/
	Creates and stores a game with
		-a grid of random questions sorted by the categories
		-leaderboard
		-board_code
	"""
	permission_classes = [AllowAny]

	def get(self, request):
		try:
			with transaction.atomic():

				questions = Question.objects.all()
				board = createNewBoard(questions)

				game_name = f"Gameboard:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
				# create gameboard
				new_gameboard = Gameboard.objects.create(
					name=game_name,
					date_created=datetime.now()
				)
				# link all of the questions to the board
				for question in board:
					question.gameboards.add(new_gameboard)
				# create leaderboard
				leaderboard = Leaderboard.objects.create(
					gameboard=new_gameboard 
				)
	
				return Response(
					GameboardSerializer(new_gameboard).data,
					status=status.HTTP_201_CREATED,
				)
		except Exception as e:
			return Response(
				{"detail": f"Game creation failed: {str(e)}"},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR,
			)

class HistoryView(APIView):
	"""
	GET /history/
	Gets the all of the games that the current user has played (leaderboard entries) sorted by date
	"""
	permission_classes = [AllowAny]

	def get(self, request):

		serializer = UserSerializer(
			data = {**request.data, "user_id" : str(

		user = None
		if request.user and request.user.is_authenticated:
			user = request.user
		else:
			user_id = UserSerializer.validated_data.pop("user_id")
			user = get_object_or_404(User, id=user_id)
		entries = LeaderboardEntry.objects.get(user=user)
		
		return Response(
			LeaderboardEntrySerializer(entries).data,
			status=status.HTTP_200_OK
		)

"""
class GameboardByIdView(APIView):
"""
#	GET /game/{id}
"""
	def get(self, request, board_code):
		gameboard = get_object_or_404(Gameboard, board_code=id)
		return Response(
			GameboardSerializer(gameboard).data,
			status=status.HTTP_200_OK
		)
"""		


class GameboardByIdView(APIView):
	"""
	GET /game/{board_code}
	"""
	def get(self, request, board_code):
		gameboard = Gameboard.objects.get(board_code=board_code)
		return Response(
			GameboardSerializer(gameboard).data,
			status=status.HTTP_200_OK
		)

class LeaderboardView(APIView):
	"""
	GET /game/{board_code}/leaderboard
	POST /game/{board_code}/leaderboard
	"""
	def get(self, request, board_code):
		gameboard = get_object_or_404(Gameboard, board_code=board_code)
		leaderboard = getattr(gameboard, "leaderboard", None)

		if leaderboard is None:
			leaderboard = Leaderboard.objects.create(
				gameboard=gameboard
			)
		
		return Response(LeaderboardSerializer(leaderboard).data)

	def post(self, request, board_code):
		gameboard = get_object_or_404(Gameboard, board_code=board_code)
		leaderboard = getattr(gameboard, "leaderboard", None)

		if leaderboard is None:
			leaderboard = Leaderboard.objects.create(
				gameboard=gameboard
			)
		
		serializer = LeaderboardEntrySerializer(
			data={**request.data, "leaderboard": str(leaderboard.id)},
			context={"request": request},
		)
		serializer.is_valid(raise_exception=True)

		# find user
		if request.user and request.user.is_authenticated:
			user = request.user
		else:
			user_id = serializer.validated_data.pop("user_id")
			user = get_object_or_404(User, id=user_id)

		entry = LeaderboardEntry.objects.create(
			leaderboard=leaderboard,
			user=user,
			score=serializer.validated_data.get("score", 0),
			total_time_seconds=serializer.validated_data.get("total_time_seconds", 0),
		)

		return Response(
			LeaderboardEntrySerializer(entry).data,
			status=status.HTTP_201_CREATED,
		)

