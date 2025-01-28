import hashlib
from sqlalchemy.orm import Session
from app.models import CachedResult, Payload


def transformer_function(string: str) -> str:
    """
    Mock function to simulate transformation of a string.
    For example, it converts a string to uppercase.

    Args:
        string (str): Input string to be transformed.
    Returns:
        str: Transformed string.
    """
    return string.upper()


# ----------------------- HELPER FUNCTIONS ----------------------- #
def get_cached_transformation(input_str: str, db: Session) -> str:
    """
    Check if the transformation for the input string is already cached.

    Args:
        input_str (str): Input string to check in the cache.
        db (Session): SQLAlchemy database session.

    Returns:
        str: Cached transformed string if found, otherwise None.
    """
    cached_result = db.query(CachedResult).filter(CachedResult.input == input_str).first()
    return cached_result.output if cached_result else None


def cache_transformation(input_str: str, transformed_str: str, db: Session):
    """
    Cache the transformation result for future reuse.

    Args:
        input_str (str): Original input string.
        transformed_str (str): Transformed string to be cached.
        db (Session): SQLAlchemy database session.
    """
    new_cache = CachedResult(input=input_str, output=transformed_str)
    db.add(new_cache)
    db.commit()


def transform_and_cache(input_str: str, db: Session) -> str:
    """
    Transform a string and cache the result if not already cached.

    Args:
        input_str (str): Input string to be transformed and cached.
        db (Session): SQLAlchemy database session.

    Returns:
        str: Transformed string.
    """
    cached_result = get_cached_transformation(input_str, db)
    if cached_result:
        return cached_result

    # Perform transformation and cache it
    transformed_str = transformer_function(input_str)
    cache_transformation(input_str, transformed_str, db)
    return transformed_str


def generate_interleaved_output(list_1: list[str], list_2: list[str]) -> str:
    """
    Generate the interleaved output of two lists of strings.

    Args:
        list_1 (list[str]): First list of transformed strings.
        list_2 (list[str]): Second list of transformed strings.

    Returns:
        str: Interleaved output as a single string.
    """
    return ", ".join([item for pair in zip(list_1, list_2) for item in pair])


def cache_payload(input_hash: str, output: str, db: Session):
    """
    Cache the entire payload for reuse.

    Args:
        input_hash (str): Unique hash of the input lists.
        output (str): Final interleaved payload.
        db (Session): SQLAlchemy database session.
    """
    new_payload = Payload(id=input_hash, output=output)
    db.add(new_payload)
    db.commit()


def get_cached_payload(input_hash: str, db: Session) -> Payload:
    """
    Retrieve a cached payload from the database.

    Args:
        input_hash (str): Unique hash of the input lists.
        db (Session): SQLAlchemy database session.

    Returns:
        Payload: Cached payload if found, otherwise None.
    """
    return db.query(Payload).filter(Payload.id == input_hash).first()


# ----------------------- CORE FUNCTIONS ----------------------- #
def generate_payload(list_1: list[str], list_2: list[str], db: Session) -> str:
    """
    Generate a unique payload by transforming and interleaving two lists of strings.

    Args:
        list_1 (list[str]): First list of strings to transform.
        list_2 (list[str]): Second list of strings to transform.
        db (Session): SQLAlchemy database session.

    Returns:
        str: Unique identifier of the generated payload.
    """
    # Generate a hash for the input lists
    input_key = f"{list_1}:{list_2}"
    input_hash = hashlib.md5(input_key.encode()).hexdigest()

    # Check if the payload is already cached
    existing_payload = get_cached_payload(input_hash, db)
    if existing_payload:
        return existing_payload.id

    # Transform and cache individual strings
    transformed_1 = [transform_and_cache(item, db) for item in list_1]
    transformed_2 = [transform_and_cache(item, db) for item in list_2]

    # Generate interleaved output
    output = generate_interleaved_output(transformed_1, transformed_2)

    # Cache the final payload
    cache_payload(input_hash, output, db)

    return input_hash


def get_payload(payload_id: str, db: Session) -> str:
    """
    Retrieve a payload by its unique identifier.

    Args:
        payload_id (str): Unique identifier of the payload.
        db (Session): SQLAlchemy database session.

    Returns:
        str: Interleaved payload output if found, otherwise None.
    """
    payload = get_cached_payload(payload_id, db)
    return payload.output if payload else None
