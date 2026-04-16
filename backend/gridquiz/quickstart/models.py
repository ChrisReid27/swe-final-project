from __future__ import annotations

import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

User = get_user_model()

class Gameboard(models.Model):
	"""
	A single board instance.
	Stores the grid (of question references), leaderboard reference
	"""

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
	name = models.CharField(max_length=200)
	board_code = models.CharField(max_length=20, unique=True) # board code is limited to 20 characters and must be unique
	
	date_created = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	CATEGORY_CHOICES = [
		("MV", "Movies"),
		("MU", "Music"),
		("SP", "Sports"),
		("TV", "TV"),
		("CE", "Celebrities"),
	]

	category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)

	VALUE_CHOICES = [
		(1, 200),
		(2, 400),
		(3, 600),
		(4, 800),
		(5, 1000),
	]
	
	value = models.PositiveIntegerField(validators=[MaxValueValidator(5)], choices=VALUE_CHOICES)
	question_text = models.CharField(max_length=300)
	answer_text = models.CharField(max_length=50)

	# reference to the gameboard so that each gameboard can have 25 questions
	gameboard = models.ManyToManyField(GameBoard, related_name="questions")
  
class Leaderboard(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	gameboard = models.OneToOneField(
		Gameboard,
		on_delete=models.CASCADE,
		related_name="leaderboard"
	)

class LeaderboardEntry(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	score = models.IntegerField()
	time_taken = models.DurationField()
	
	leaderboard = models.ForeignKey(
		Leaderboard,
		on_delete=models.CASCADE,
		related_name="leaderboard"
	)

	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name="leaderboard_entries"
	)

	history = models.ForeignKey(
		History,
		on_delete=models.CASCADE,
		related_name="leaderboard_entries"
	)

class User(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	username = models.CharField(max_length=30)

class History(models.Model): # might also need a history entry OR history might not be needed because we can query the database based on user, sorted by time
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name="user"
	)	
