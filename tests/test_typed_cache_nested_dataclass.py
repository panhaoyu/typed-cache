import tempfile
from dataclasses import dataclass
from pathlib import Path

from typed_cache import TypedCache


# Assuming TypedCache is imported from the module where it's defined
# from typed_cache_module import TypedCache

@dataclass
class NestedData:
    x: int
    y: str


@dataclass
class TestDataWithNested(TypedCache):
    path: Path
    a: int = None
    nested: NestedData = None


def test_nested_dataclass_attribute():
    """
    Test that an attribute which is an instance of another dataclass
    can be saved and loaded correctly.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_file = Path(temp_dir) / 'cache.pickle'

        # Create an instance with nested dataclass
        nested_instance = NestedData(x=10, y='nested')
        data = TestDataWithNested(path=cache_file, a=42, nested=nested_instance)
        data.save()

        # Load the data from the cache
        loaded_data = TestDataWithNested(path=cache_file)

        # Assertions
        assert loaded_data.a == 42
        assert isinstance(loaded_data.nested, NestedData)
        assert loaded_data.nested.x == 10
        assert loaded_data.nested.y == 'nested'
