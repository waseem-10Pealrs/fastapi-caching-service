import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import CachedResult, Payload

# ------------------- Helper Functions -------------------

def transformer_function(string: str) -> str:
    """
    Simulates an external service for string transformation.
    For this example, it converts the input string to uppercase.

    Args:
        string (str): The input string to be transformed.

    Returns:
        str: The transformed string (e.g., uppercase).

    Why?
    - Centralizes transformation logic for consistency.
    - Can be replaced with an actual service or complex logic in the future.
    """
    return string.upper()

def generate_interleaved_output(list_1: list[str], list_2: list[str]) -> str:
    """
    Interleave two lists of strings into a single output string.

    Args:
        list_1 (list[str]): First list of transformed strings.
        list_2 (list[str]): Second list of transformed strings.

    Returns:
        str: A single string with interleaved elements from the two lists.

    Example:
        list_1 = ["A", "B", "C"]
        list_2 = ["X", "Y", "Z"]
        Output: "A, X, B, Y, C, Z"

    Why?
    - Provides reusable functionality to interleave two lists for the payload.
    - Ensures the structure matches the API's output requirements.
    """
    interleaved = [item for pair in zip(list_1, list_2) for item in pair]
    return ", ".join(interleaved)

# ------------------- Caching Logic -------------------

async def get_cached_transformation(input_str: str, db: AsyncSession) -> str:
    """
    Retrieve a cached transformation for the given string from the database.

    Args:
        input_str (str): The input string.
        db (AsyncSession): The database session.

    Returns:
        str: The cached transformed string if it exists, else None.

    Why?
    - Prevents redundant transformations by reusing previously cached results.
    """
    result = await db.execute(select(CachedResult).where(CachedResult.input == input_str))
    cached_result = result.scalars().first()
    return cached_result.output if cached_result else None

async def cache_transformation(input_str: str, transformed_str: str, db: AsyncSession):
    """
    Cache the transformed result of a string in the database.

    Args:
        input_str (str): The original input string.
        transformed_str (str): The transformed string.
        db (AsyncSession): The database session.

    Why?
    - Saves results for future reuse, improving performance and efficiency.
    """
    cached_result = CachedResult(input=input_str, output=transformed_str)
    db.add(cached_result)
    await db.commit()

async def transform_and_cache(input_str: str, db: AsyncSession) -> str:
    """
    Transform a string and cache the result if not already cached.

    Args:
        input_str (str): The string to transform.
        db (AsyncSession): The database session.

    Returns:
        str: The transformed string.

    Why?
    - Combines transformation and caching into a single function for simplicity.
    - Reduces redundant logic when processing multiple strings.
    """
    # Check if the transformation is already cached
    cached_result = await get_cached_transformation(input_str, db)
    if cached_result:
        return cached_result

    # Perform the transformation and cache it
    transformed_str = transformer_function(input_str)
    await cache_transformation(input_str, transformed_str, db)
    return transformed_str

# ------------------- Payload Caching -------------------

async def get_cached_payload(input_hash: str, db: AsyncSession) -> Payload:
    """
    Retrieve a cached payload from the database by its hash.

    Args:
        input_hash (str): The unique hash of the input lists.
        db (AsyncSession): The database session.

    Returns:
        Payload: The cached payload if it exists, else None.

    Why?
    - Enables fast retrieval of previously generated outputs.
    """
    result = await db.execute(select(Payload).where(Payload.id == input_hash))
    return result.scalars().first()

async def cache_payload(input_hash: str, output: str, db: AsyncSession):
    """
    Cache the generated payload in the database.

    Args:
        input_hash (str): The unique hash of the input lists.
        output (str): The interleaved transformed output.
        db (AsyncSession): The database session.

    Why?
    - Saves the final payload for future reuse, reducing computation.
    """
    payload = Payload(id=input_hash, output=output)
    db.add(payload)
    await db.commit()

# ------------------- Core Business Logic -------------------

async def generate_payload(list_1: list[str], list_2: list[str], db: AsyncSession) -> str:
    """
    Generate a unique payload by:
    - Transforming strings from two input lists.
    - Interleaving transformed strings.
    - Caching results for reuse.

    Args:
        list_1 (list[str]): The first list of strings.
        list_2 (list[str]): The second list of strings.
        db (AsyncSession): The database session.

    Returns:
        str: The unique identifier (hash) of the generated payload.

    Why?
    - Centralized function to handle the complete process of payload creation.
    - Ensures caching and transformation logic are reused consistently.
    """
    # Generate a unique hash for the input lists
    input_key = f"{list_1}:{list_2}"
    input_hash = hashlib.md5(input_key.encode()).hexdigest()

    # Check if the payload is already cached
    existing_payload = await get_cached_payload(input_hash, db)
    if existing_payload:
        return existing_payload.id

    # Transform and cache strings from both lists
    transformed_1 = [await transform_and_cache(item, db) for item in list_1]
    transformed_2 = [await transform_and_cache(item, db) for item in list_2]

    # Generate the interleaved output
    output = generate_interleaved_output(transformed_1, transformed_2)

    # Cache the final payload
    await cache_payload(input_hash, output, db)

    return input_hash

async def get_payload(payload_id: str, db: AsyncSession) -> str:
    """
    Retrieve the payload by its unique identifier.

    Args:
        payload_id (str): The unique identifier for the payload.
        db (AsyncSession): The database session.

    Returns:
        str: The interleaved payload output.

    Why?
    - Allows clients to fetch previously generated results efficiently.
    """
    payload = await get_cached_payload(payload_id, db)
    return payload.output if payload else None
