from __future__ import annotations

from rest_framework import serializers

from .models import Gameboard, Leaderboard, LeaderboardEntry, Question, User 

from django.contrib.auth import get_user_model
# import the current User as well
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ("id", "username", "email", "history")
		read_only_fields = ("id", "username", "email", "history") # store email in order to use firebase auth

class LeaderboardEntrySerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)
	class Meta:
		model = LeaderboardEntry
		fields = (
			"id",
			"leaderboard",
			"user",
			"history",
			"score",
			"time_taken",
		)
		read_only_fields = (
			"id",
		)


class LeaderboardSerializer(serializers.ModelSerializer):
	entries = LeaderboardEntrySerializer(many=True, read_only=True)
	class Meta:
		model = Leaderboard
		fields = (
			"id",
			"gameboard",
			"entries",
		)
		read_only_fields = (
			"id",
		)

class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = (
			"category",
			"value",
			"question_text",
			"answer_text",
		)
		read_only_fields = (	
			"category",
			"value",
			"question_text",
			"answer_text",
		)

class GameboardSerializer(serializers.ModelSerializer):
	questions = QuestionSerializer(many=True, read_only=True)
	leaderboard = LeaderboardSerializer(read_only=True)
	
	class Meta:
		model = Gameboard
		fields = (
			"board_code",
			"name",
			"date_created",
			"questions",
			"leaderboard",
		)
		read_only_fields = (
			"board_code",
			"name",
			"date_created",
			"questions",
		)	
