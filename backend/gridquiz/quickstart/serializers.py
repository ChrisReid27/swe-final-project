from __future__ import annotations

from rest_framework import serializers

from .models import Gameboard, Question, Leaderboard, LeaderboardEntry, History

from django.contrib.auth import get_user_model
# import the current User as well
User = get_user_model()

class HistorySerializer(serializers.ModelSerializer):
	entries = LeaderboardEntrySerializer(read_only=True, many=True)
	class Meta:
		fields = (
			"id",
			"entries"
		)

class UserSerializer(serializers.ModelSerializer):
	history = HistorySerializer(read_only=True)
	class Meta:
		model = User
		fields = ("id", "username", "email", "history")
		read_only_fields = ("id", "username", "email", "history") # store email in order to use firebase auth

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

class LeaderboardEntrySerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)
	class Meta:
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

class GameboardSerializer(serializers.ModelSerializer):
	questions = QuestionSerializer(many=True, read_only=True)
	leaderboard = LeaderboardSerializer(read_only=True)
	
	class Meta:
		model = GameBoard
		fields = (
			"id",
			"name",
			"boardcode",
			"date_created",
			"questions",
		)
		read_only_fields = (
			"id",
			"name",
			"boardcode",
			"date_created",
			"questions",
		)	
