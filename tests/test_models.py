from app.models import CachedResult, Payload
from app.database import SessionLocal, Base, engine

# Recreate the tables for testing
Base.metadata.create_all(bind=engine)

def test_cached_result_model():
    """
    Test the CachedResult model by inserting and retrieving a record.
    Why?
    - Ensure the CachedResult schema works as expected in the database.
    """
    db = SessionLocal()
    try:
        # Insert a record
        cached_result = CachedResult(input="test_input", output="TEST_OUTPUT")
        db.add(cached_result)
        db.commit()

        # Retrieve the record
        record = db.query(CachedResult).filter(CachedResult.input == "test_input").first()
        assert record.output == "TEST_OUTPUT", "CachedResult output mismatch"
    finally:
        db.rollback()  # Roll back changes to keep the database clean
        db.close()

def test_payload_model():
    """
    Test the Payload model by inserting and retrieving a record.
    Why?
    - Ensure the Payload schema works as expected in the database.
    """
    db = SessionLocal()
    try:
        # Insert a record
        payload = Payload(id="unique_id", output="test_output")
        db.add(payload)
        db.commit()

        # Retrieve the record
        record = db.query(Payload).filter(Payload.id == "unique_id").first()
        assert record.output == "test_output", "Payload output mismatch"
    finally:
        db.rollback()  # Roll back changes to keep the database clean
        db.close()
