from app import create_app
from app.database import init_db

app = create_app()

init_db()

if __name__ == '__main__':
    app.run(use_reloader=False, host="0.0.0.0", port=5000)
