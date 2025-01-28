import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import engine, Base, get_db
from app.models import CachedResult

@pytest.mark.asyncio
async def test_database_schema_creation():
    """
    Test if the database schema is created successfully.
    """
    async with engine.begin() as conn:
        # Ensure the tables are created
        await conn.run_sync(Base.metadata.create_all)

    # Check if the CachedResult table exists by attempting to insert data
    async with AsyncSession(bind=engine) as session:
        cached_result = CachedResult(input="test_input", output="TEST_OUTPUT")
        session.add(cached_result)
        await session.commit()

        # Verify that the record exists in the database
        result = await session.execute(select(CachedResult).where(CachedResult.input == "test_input"))
        record = result.scalars().first()
        assert record is not None
        assert record.output == "TEST_OUTPUT"

    # Clean up
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


