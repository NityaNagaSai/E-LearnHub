from app import create_app
from app.db.crud import create_tables, insert_users

app = create_app()

app.before_request
def initialize_database():
    with app.app_context():
        create_tables()
        insert_users()

if __name__ == "__main__":
    app.run(debug=True)