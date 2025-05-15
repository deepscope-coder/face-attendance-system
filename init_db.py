from app import create_app, db

app = create_app()

def initialize_database():
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")

if __name__ == '__main__':
    initialize_database()