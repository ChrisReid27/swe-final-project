from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# import models and serializers
from .models import Gameboard, Leaderboard, LeaderboardEntry, Question

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
from .default_questions import seed_default_questions

import uuid

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
				seed_default_questions()

				questions = Question.objects.all()
				board = createNewBoard(questions)

				game_name = f"Gameboard:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
				# create gameboard
				new_gameboard = Gameboard.objects.create(
					name=game_name,
					date_created=timezone.now()
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

	def get(self, request):

		user = None
		if request.user and request.user.is_authenticated:
			user = request.user
		else:
			user_id = UserSerializer.validated_data.pop("id")
			user = get_object_or_404(User, id=user_id)
		entries = LeaderboardEntry.objects.filter(user=user)
		
		return Response(
			LeaderboardEntrySerializer(entries, many=True).data,
			status=status.HTTP_200_OK
		)

class GameboardByIdView(APIView):
	"""
	GET /game/{board_code}
	"""
	def get(self, request, board_code):
		gameboard = get_object_or_404(Gameboard, board_code=board_code)
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
		
		payload = {**request.data, "leaderboard": str(leaderboard.id)}
		serializer = LeaderboardEntrySerializer(data=payload, context={"request": request})
		serializer.is_valid(raise_exception=True)

		# find user
		if request.user and request.user.is_authenticated:
			user = request.user
		else:
			user_id = request.data.get("user_id")
			if not user_id:
				return Response(
					{"detail": "user_id is required when not authenticated."},
					status=status.HTTP_400_BAD_REQUEST,
				)
			user = get_object_or_404(User, id=user_id)

		time_taken = serializer.validated_data.get("time_taken", timedelta())
		entry = LeaderboardEntry.objects.create(
			leaderboard=leaderboard,
			user=user,
			score=serializer.validated_data.get("score", 0),
			time_taken=serializer.validated_data.get("time_taken", 0),
		)

		entry.leaderboard.add(leaderboard)

		return Response(
			LeaderboardSerializer(leaderboard).data,
			status=status.HTTP_201_CREATED,
		)

