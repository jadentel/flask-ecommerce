from app import app, db
from app.models import initialize_data, initialise_user

if __name__ == '__main__':
    # Initialize the database when the application starts
    with app.app_context():
        initialize_data()
        initialise_user()

    app.run(debug=True)
