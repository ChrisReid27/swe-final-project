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
    before = Question.objects.count()
    for q in DEFAULT_QUESTION_DATA:
        Question.objects.update_or_create(question_text=q['question_text'], defaults=q)
    after = Question.objects.count()
    print(f"Synced default questions. Before: {before}, After: {after}")

if __name__ == '__main__':
    sync_defaults()
