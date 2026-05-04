from __future__ import annotations

from datetime import timedelta

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Gameboard, Leaderboard, LeaderboardEntry, Question

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ("id", "username", "email")
		read_only_fields = fields

class LeaderboardEntrySerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)
	class Meta:
		model = LeaderboardEntry
		fields = (
			"id",
			"leaderboard",
			"user",
			"score",
			"time_taken",
		)
		read_only_fields = (
			"id",
		)

	def create(self, validated_data):
		time_taken = validated_data.get("time_taken")
		if isinstance(time_taken, int):
			validated_data["time_taken"] = timedelta(seconds=time_taken)
		return super().create(validated_data)


class LeaderboardSerializer(serializers.ModelSerializer):
	entries = LeaderboardEntrySerializer(many=True, read_only=True)
	class Meta:
		model = Leaderboard
		fields = (
			"id",
			"gameboard",
			"entries",
		)
		read_only_fields = ("id", "gameboard", "entries")

class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = (
			"id",
			"category",
			"value",
			"question_text",
			"answer_text",
			"howard",
		)
		read_only_fields = fields

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
