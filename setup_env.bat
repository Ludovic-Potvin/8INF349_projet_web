@echo off
echo Setting up app...

:: Create .env file if not exists
if not exist .env (
    copy .env.example .env
    echo Created .env file from .env.example.
)

echo Setup .env complete!
