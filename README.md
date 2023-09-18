# Task manager backend

Backend of the task manager web application 🗃️🔧

## Run Locally

Clone the project

```bash
  https://github.com/sergiopmdev/task_manager_backend
```

Go to the project directory

```bash
  cd task_manager_backend
```

Create a Python virtual environment

```bash
  python -m venv env
```

Install the dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  uvicorn src.main:app --reload
```

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`MONGODB_URI`

`SECRET_KEY`

If you want to have access to the local execution of the project, create your own MongoDB instance as you prefer or contact me to give you access to the database address and a temporary user

## Features

- Register users and log in
- Temporary authorization based on OAuth and JWT
- Get all tasks of an user
- Eliminate task of an user
- Edit task of an user (coming soon...)
- Mark task of an user as completed (coming soon...)

## Tech Stack

Fastapi with Python 3.11.4
