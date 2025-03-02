@echo off
echo Setting up app...

:: Create virtual environment
python -m venv .venv
call .venv\Scripts\activate

:: Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

:: Create .env file if not exists
if not exist .env (
    copy .env.example .env
    echo Created .env file from .env.example.
)

echo Setup complete! Run '.venv\Scripts\activate' to activate the environment.