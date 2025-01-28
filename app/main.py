from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db, Base, engine
from app.schemas import PayloadRequest, PayloadResponse
from app.service import generate_payload, get_payload,get_cached_payload

# Initialize the FastAPI application
app = FastAPI()

# Ensure database tables are created during application startup
@app.on_event("startup")
async def startup_event():
    """
    Create database tables at application startup.
    Why?
    - Ensures the database schema is in place before any API call.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/payload", response_model=PayloadResponse)
async def create_payload(payload_request: PayloadRequest, db: AsyncSession = Depends(get_db)):
    """
    Create a new payload.
    - Accepts two lists in the request body.
    - Returns the unique ID and the interleaved output.
    """
    payload_id = await generate_payload(payload_request.list_1, payload_request.list_2, db)

    # Fetch the full payload from the database to include the output
    result = await get_cached_payload(payload_id, db)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to cache or retrieve payload")

    return {"id": result.id, "output": result.output}



@app.get("/payload/{id}", response_model=PayloadResponse)
async def read_payload(id: str, db: AsyncSession = Depends(get_db)):
    """
    Endpoint to retrieve an existing payload by its unique identifier.

    - Fetches the payload from the database if it exists.
    - Returns a 404 error if the payload is not found.

    Args:
    - id (str): The unique identifier for the payload.
    - db (AsyncSession): Database session injected via dependency.

    Returns:
    - PayloadResponse: JSON response containing the payload ID and the interleaved output.
    """
    payload_output = await get_payload(id, db)
    if not payload_output:
        raise HTTPException(status_code=404, detail="Payload not found")
    return {"id": id, "output": payload_output}
