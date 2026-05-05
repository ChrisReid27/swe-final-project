from __future__ import annotations 
from rest_framework import serializers 
from .models import Gameboard, Leaderboard, LeaderboardEntry, Question 
from django.contrib.auth import get_user_model # import the current User as well 
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ("id", "username", "email")
		read_only_fields = ("id", "username", "email") 

class LeaderboardEntrySerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)
	class Meta:
		model = LeaderboardEntry
		fields = (
			"user",
			"score",
 			"time_taken",
		)
	def create(self, data):
		leaderboard_entry = LeaderboardEntry.objects.create(
			user=User.objects.get(id=data['id']),
			score=data['score'],
			time_taken=data['time_taken']
		)
		return leaderboard_entry

class LeaderboardSerializer(serializers.ModelSerializer):
	leaderboard_entries = LeaderboardEntrySerializer(many=True, read_only=True)
	class Meta:
		model = Leaderboard
		fields = (
			"gameboard",
			"leaderboard_entries",
		)

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
	
	class Meta:
		model = Gameboard
		fields = (
			"board_code",
			"name",
			"date_created",
			"questions",
		)
		read_only_fields = (
			"board_code",
			"name",
			"date_created",
			"questions",
		)	
