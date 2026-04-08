from __future__ import annotations

import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

User = get_user_model()

class GameBoard(models.Model):
	"""
	A single board instance.
	Stores the grid (of question references), leaderboard reference
	"""

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
	name = models.CharField(max_length=200)
	board_code = models.CharField(max_length=20, unique=True) # board code is limited to 20 characters and must be unique
	
	date_created = models.DateTimeField(auto_now_add=True)

class Questions(models.Model):
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
#class Leaderboard(models.Model):
#	GameBoard
#
#class Leaderboard_Entry(models.Model):
#
#class User(models.Model):
#
#class History(models.Model):	
