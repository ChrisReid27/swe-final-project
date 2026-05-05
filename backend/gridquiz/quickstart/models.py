from __future__ import annotations

import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

import datetime

from django.contrib.auth.models import User

class Gameboard(models.Model):
	"""
	A single board instance.
	Stores the grid (of question references), leaderboard reference
	"""
	board_code = models.AutoField(primary_key=True, editable=False)
	name = models.CharField(max_length=200)
	date_created = models.DateTimeField(default=datetime.datetime.min)
	
  
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
	time_taken = models.IntegerField()
	
	leaderboard = models.ForeignKey(
		Leaderboard,
		on_delete=models.CASCADE,
		related_name="leaderboard_entries"
	)

	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name="leaderboard_entries"
	)

class Question(models.Model): 
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	category = models.CharField(max_length=20)
	value = models.PositiveIntegerField()
	question_text = models.CharField(max_length=500)
	answer_text = models.CharField(max_length=100)

	howard = models.BooleanField(default=False)

	gameboards = models.ManyToManyField(
		Gameboard,
		related_name='questions'
	)	
