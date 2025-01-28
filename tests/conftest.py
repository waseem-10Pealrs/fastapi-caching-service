import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database import Base

@pytest.fixture(scope="session")
def test_engine():
    """Create a new SQLite in-memory database for testing."""
    return create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)

@pytest.fixture(scope="session")
async def test_db(test_engine):
    """Create tables and initialize the test database."""
    async with test_engine.begin() as conn:
        # Ensure tables are created
        await conn.run_sync(Base.metadata.create_all)
    yield test_engine
    await test_engine.dispose()

@pytest.fixture
async def db_session(test_db):
    """Provide a SQLAlchemy session for tests."""
    async_session = sessionmaker(
        bind=test_db, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session  # Properly yield the session object
