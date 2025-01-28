from app.service import (
    transformer_function,
    generate_interleaved_output,
)

def test_transformer_function():
    """Test the string transformer function."""
    assert transformer_function("hello") == "HELLO"

def test_generate_interleaved_output():
    """Test interleaving two lists of strings."""
    list_1 = ["A", "B"]
    list_2 = ["1", "2"]
    result = generate_interleaved_output(list_1, list_2)
    assert result == "A, 1, B, 2"

