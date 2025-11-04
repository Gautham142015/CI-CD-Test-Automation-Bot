import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import SessionLocal, engine
from backend import models, schemas

# Create tables
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Check if tasks already exist to prevent duplicate seeding
if db.query(models.Task).count() == 0:
    tasks = [
      schemas.TaskCreate(
        description='Users should be able to log in with their email and password.',
        type='feature',
        priority='High',
        user_story='As a registered user, I want to log in with my credentials so that I can access my account.',
        acceptance_criteria='Given I am on the login page, when I enter my correct email and password and click "Log In", then I am redirected to my dashboard.'
      ),
      schemas.TaskCreate(
        description='The main dashboard loads very slowly, especially with more than 100 tasks.',
        type='pain_point',
        priority='High',
        user_story='As a user, I find that the dashboard is slow to load, which makes the app feel unresponsive.',
        acceptance_criteria='Given I have over 100 tasks, when I navigate to the dashboard, then the page should load in under 2 seconds.'
      ),
      schemas.TaskCreate(
        description='Add a "dark mode" option to the user settings.',
        type='enhancement',
        priority='Medium',
        user_story='As a user, I want to be able to switch to a dark mode to reduce eye strain, especially at night.',
        acceptance_criteria='Given I am in the settings page, when I toggle the "Dark Mode" switch, then the UI should immediately switch to a dark color scheme.'
      )
    ]

    for task in tasks:
        db_task = models.Task(**task.dict())
        db.add(db_task)

    db.commit()
    print('Database seeded with example tasks.')
else:
    print('Database already seeded.')

db.close()
