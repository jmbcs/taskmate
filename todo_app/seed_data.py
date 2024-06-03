# seed_data.py
import os

# from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todo_app.settings")
import django

django.setup()


import random

from django.contrib.auth.models import User
from django_seed import Seed
from todo.models import Todo

# Initialize seeder
seeder = Seed.seeder()

# Get all admin users
admin_users = User.objects.filter(is_staff=True, is_superuser=True)

# If there are no admin users, create one
if not admin_users:
    admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
    admin_users = [admin_user]

# Add todos
seeder.add_entity(
    Todo,
    10,
    {
        'assigned_user': lambda x: random.choice(admin_users),
        'description': lambda x: seeder.faker.sentence(),
        'status': lambda x: random.choice(
            ['TO_DO', 'STALLED', 'IN_PROGRESS', 'COMPLETED']
        ),
        'due_date': lambda x: seeder.faker.date_this_month(
            before_today=True, after_today=True
        ),
        'priority': lambda x: random.randint(1, 3),
        'notes': lambda x: seeder.faker.text(),
        'category': lambda x: random.choice(
            ['work', 'personal', 'shopping', 'health', 'other']
        ),
    },
)

# Execute seeding
inserted_pks = seeder.execute()

# Print inserted primary keys
print(inserted_pks)
