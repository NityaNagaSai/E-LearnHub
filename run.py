from app import create_app
from app.db.crud import create_tables, insert_users

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)