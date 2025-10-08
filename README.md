📌 lazyT API
overview

This is a task manager API, written using python framework Django and DjangoRESTFRAMEWORK. This is mainly an api so no frontend.

🚀 Features
Add Task
View all and specific task
Edit task, mark the task done
Delete Task
📁 Project Structure

    lazyT_api/
    │
    ├── lazyT_api/
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    │
    ├── tasks/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── authentication.py
    │   ├── migrations/
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   ├── utils.py
    │   └── views.py
    │
    ├── manage.py
    │
    ├── setup.py
    ├── requirements.txt
    ├── README.md
    └── .gitignore

🛠 Installation And Setup

(just look or use the requirements.txt)

Installation

# Clone the repository

git clone https://github.com/78RainDrops/lazyT_api.git
cd lazyT_api

# Install dependencies

# Create a venv or virtual environment

python -m venv .venv

# or

python3 -m venv .venv

# Enable the venv

source .venv/bin/activate

# install pip packages using requirements.txt

pip install -r requirements.txt # Python

▶ Usage

Run the django server:

python manage.py runserver

👨‍💻 Author
78RainDrops - https://github.com/78RainDrops
