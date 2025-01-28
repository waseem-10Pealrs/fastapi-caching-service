from dotenv import load_dotenv
import os

def test_env_variables():
    """
    Test that environment variables are loaded correctly from the .env file.
    Why?
    - Ensure the application can access database configuration securely.
    """
    load_dotenv()

    assert os.getenv("POSTGRES_USER") == "postgres", "POSTGRES_USER not loaded correctly"
    assert os.getenv("POSTGRES_PASSWORD") == "password", "POSTGRES_PASSWORD not loaded correctly"
    assert os.getenv("POSTGRES_HOST") == "localhost", "POSTGRES_HOST not loaded correctly"
    assert os.getenv("POSTGRES_PORT") == "5432", "POSTGRES_PORT not loaded correctly"
    assert os.getenv("POSTGRES_DB") == "caching_service", "POSTGRES_DB not loaded correctly"
