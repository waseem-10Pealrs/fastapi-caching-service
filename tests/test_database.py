from app.database import engine, Base, SessionLocal

def test_database_initialization():
    """
    Test that the database tables are created without errors.
    Why?
    - Ensure database schema is correctly initialized during app startup.
    """
    try:
        Base.metadata.create_all(bind=engine)  # Create tables
        assert True  # If no exception, test passes
    except Exception as e:
        assert False, f"Database initialization failed: {e}"

def test_database_session():
    """
    Test that the database session can be created and closed.
    Why?
    - Ensure the session lifecycle works without issues.
    """
    try:
        db = SessionLocal()
        db.close()  # Close session
        assert True  # If no exception, test passes
    except Exception as e:
        assert False, f"Database session creation failed: {e}"
