"""Generic test function."""



def test(output: str | None, function, *args, **kwargs) -> None | AssertionError:
    """Test given function against provided output."""

    assert function(*args, **kwargs) == output, f"Should be {output}" if output else "Incorrect output"



def inc(n): return n + 1


test(None, inc, 1)
