from app.models import CachedResult
from app.service import get_cached_transformation, cache_transformation, transform_and_cache
from app.database import SessionLocal, Base, engine

Base.metadata.create_all(bind=engine)  # Recreate tables for testing

def test_get_cached_transformation():
    """
    Test retrieval of a cached transformation from the database.
    Why?
    - Ensure cached results are correctly fetched by input string.
    """
    db = SessionLocal()
    try:
        # Add a cached result
        cached_result = CachedResult(input="test_input", output="TEST_OUTPUT")
        db.add(cached_result)
        db.commit()

        # Fetch the cached result
        output = get_cached_transformation("test_input", db)
        assert output == "TEST_OUTPUT", "Cached transformation mismatch"
    finally:
        db.rollback()
        db.close()

def test_cache_transformation():
    """
    Test caching a new transformation in the database.
    Why?
    - Validate that new results can be stored for future reuse.
    """
    db = SessionLocal()
    try:
        # Cache a transformation
        cache_transformation("new_input", "NEW_OUTPUT", db)

        # Check if it's stored
        cached = db.query(CachedResult).filter(CachedResult.input == "new_input").first()
        assert cached.output == "NEW_OUTPUT", "Failed to cache transformation"
    finally:
        db.rollback()
        db.close()

def test_transform_and_cache():
    """
    Test the combined transformation and caching logic.
    Why?
    - Ensure transformations are performed and stored correctly in one process.
    """
    db = SessionLocal()
    try:
        # Test transforming and caching
        output = transform_and_cache("another_input", db)
        assert output == "ANOTHER_INPUT", "Transformation output mismatch"

        # Ensure it's cached
        cached = db.query(CachedResult).filter(CachedResult.input == "another_input").first()
        assert cached.output == "ANOTHER_INPUT", "Failed to cache transformation"
    finally:
        db.rollback()
        db.close()
