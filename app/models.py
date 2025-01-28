from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class CachedResult(Base):
    """
    Stores transformed results of individual strings.
    Why?
    - Avoid repeated transformations for the same input, improving performance.
    - Ensures efficiency when processing large datasets or frequently repeated strings.
    """
    __tablename__ = "cached_results"

    id = Column(Integer, primary_key=True, index=True)  # Primary key for the table
    input = Column(Text, unique=True, nullable=False)  # Original string
    output = Column(Text, nullable=False)  # Transformed string (e.g., uppercase)

class Payload(Base):
    """
    Stores interleaved outputs for given input lists.
    Why?
    - Cache the final payload to prevent redundant computation of the same input combination.
    """
    __tablename__ = "payloads"

    id = Column(String, primary_key=True, index=True)  # Unique hash of input lists
    output = Column(Text, nullable=False)  # Interleaved transformed output
