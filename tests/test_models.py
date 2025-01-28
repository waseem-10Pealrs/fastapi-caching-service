from app.models import CachedResult, Payload

def test_cached_result_model():
    """Test CachedResult model attributes."""
    cached_result = CachedResult(id=1, input="test", output="TEST")
    assert cached_result.id == 1
    assert cached_result.input == "test"
    assert cached_result.output == "TEST"

def test_payload_model():
    """Test Payload model attributes."""
    payload = Payload(id="abc123", output="A, B, C")
    assert payload.id == "abc123"
    assert payload.output == "A, B, C"
