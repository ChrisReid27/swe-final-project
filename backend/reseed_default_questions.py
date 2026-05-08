import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gridquiz.settings')

import django
django.setup()

from gridquiz.quickstart.models import Question
from gridquiz.quickstart.default_questions import DEFAULT_QUESTION_DATA

def sync_defaults():
    Question.objects.all().delete()
    Question.objects.bulk_create([Question(**q) for q in DEFAULT_QUESTION_DATA])
    print(f"Reseeded {len(DEFAULT_QUESTION_DATA)} default questions")

if __name__ == '__main__':
    sync_defaults()
