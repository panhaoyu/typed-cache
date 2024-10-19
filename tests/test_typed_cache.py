import pickle
import tempfile
from dataclasses import dataclass
from pathlib import Path

import pytest

from typed_cache import TypedCache


# Test subclass of TypedCache
@dataclass
class TestData(TypedCache):
    path: Path
    a: int = None
    b: float = None
    c: str = None
    d: bool = None


def test_initialization_valid_path():
    """
    Test that the TypedCache initializes correctly with a valid '.pickle' path.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_file = Path(temp_dir) / 'cache.pickle'
        data = TestData(path=cache_file)
        assert data.path == cache_file


def test_initialization_invalid_path():
    """
    Test that initializing with an invalid path (not ending with '.pickle') raises ValueError.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        invalid_cache_file = Path(temp_dir) / 'cache.invalid'
        with pytest.raises(ValueError, match="Cache file must have a '.pickle' suffix"):
            data = TestData(path=invalid_cache_file)


def test_save_and_load():
    """
    Test that data is saved and loaded correctly using the save() method and automatic loading.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_file = Path(temp_dir) / 'cache.pickle'

        # Initialize and set attributes
        data = TestData(path=cache_file)
        data.a = 42
        data.b = 3.14
        data.c = 'hello'
        data.d = True
        data.save()

        # Create a new instance to load the saved data
        loaded_data = TestData(path=cache_file)
        assert loaded_data.a == 42
        assert loaded_data.b == 3.14
        assert loaded_data.c == 'hello'
        assert loaded_data.d is True


def test_path_attribute_not_saved():
    """
    Test that the 'path' attribute is not included in the saved pickle data.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_file = Path(temp_dir) / 'cache.pickle'
        data = TestData(path=cache_file)
        data.save()

        with cache_file.open('rb') as f:
            saved_data = pickle.load(f)

        assert 'path' not in saved_data


def test_clear():
    """
    Test that the clear() method deletes the cache file if it exists.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_file = Path(temp_dir) / 'cache.pickle'
        data = TestData(path=cache_file)
        data.a = 100
        data.save()
        assert cache_file.exists()
        data.clear()
        assert not cache_file.exists()


def test_nonexistent_cache_file():
    """
    Test that when the cache file does not exist, the object initializes with default attribute values.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_file = Path(temp_dir) / 'nonexistent_cache.pickle'
        data = TestData(path=cache_file)
        assert data.a is None
        assert data.b is None
        assert data.c is None
        assert data.d is None


def test_corrupted_cache_file():
    """
    Test that an exception is raised when attempting to load a corrupted cache file.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_file = Path(temp_dir) / 'cache.pickle'

        # Write invalid data to the cache file
        with cache_file.open('wb') as f:
            f.write(b'not a valid pickle')

        # Attempt to initialize and expect an exception
        with pytest.raises(Exception):
            data = TestData(path=cache_file)


def test_save_update_and_load():
    """
    Test that updating attributes and saving again correctly updates the cached data.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_file = Path(temp_dir) / 'cache.pickle'

        # Initial save
        data = TestData(path=cache_file)
        data.a = 1
        data.b = 2.0
        data.c = 'initial'
        data.d = False
        data.save()

        # Update and save again
        data.a = 10
        data.b = 20.0
        data.c = 'updated'
        data.d = True
        data.save()

        # Load new instance to verify updated data
        loaded_data = TestData(path=cache_file)
        assert loaded_data.a == 10
        assert loaded_data.b == 20.0
        assert loaded_data.c == 'updated'
        assert loaded_data.d is True


def test_cache_file_creation():
    """
    Test that the cache file is created in the correct location and that parent directories are created if necessary.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        subdir = Path(temp_dir) / 'nested' / 'subdir'
        cache_file = subdir / 'cache.pickle'
        data = TestData(path=cache_file)
        data.a = 999
        data.save()
        assert cache_file.exists()


def test_loading_when_cache_file_missing():
    """
    Test that initializing an object when the cache file is missing does not raise an exception and attributes remain default.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_file = Path(temp_dir) / 'missing_cache.pickle'
        data = TestData(path=cache_file)
        assert data.a is None
        assert data.b is None
        assert data.c is None
        assert data.d is None


def test_loading_with_empty_cache_file():
    """
    Test that an exception is raised when the cache file is empty.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_file = Path(temp_dir) / 'empty_cache.pickle'
        cache_file.touch()  # Create an empty file
        with pytest.raises(EOFError):
            data = TestData(path=cache_file)


def test_cache_file_with_unexpected_data():
    """
    Test that loading from a cache file with unexpected data sets attributes accordingly.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_file = Path(temp_dir) / 'cache.pickle'

        # Save unexpected data
        unexpected_data = {'x': 123, 'y': 'abc'}
        with cache_file.open('wb') as f:
            pickle.dump(unexpected_data, f)

        # Initialize and check that attributes are set
        data = TestData(path=cache_file)
        assert hasattr(data, 'x')
        assert hasattr(data, 'y')
        assert data.x == 123
        assert data.y == 'abc'


def test_loading_with_partial_data():
    """
    Test that loading from a cache file with partial data only updates the provided attributes.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_file = Path(temp_dir) / 'cache.pickle'

        partial_data = {'a': 100, 'c': 'partial'}
        with cache_file.open('wb') as f:
            pickle.dump(partial_data, f)

        data = TestData(path=cache_file)
        assert data.a == 100
        assert data.b is None  # Should remain default
        assert data.c == 'partial'
        assert data.d is None  # Should remain default


def test_setting_undeclared_attributes():
    """
    Test that setting attributes not declared in the dataclass does not include them in the saved data.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_file = Path(temp_dir) / 'cache.pickle'
        data = TestData(path=cache_file)
        data.a = 1
        data.b = 2.0
        data.c = 'test'
        data.d = True
        data.e = 'undeclared'  # Attribute not declared in dataclass
        data.save()

        # Load saved data directly
        with cache_file.open('rb') as f:
            saved_data = pickle.load(f)

        # 'e' should not be in saved_data
        assert 'e' not in saved_data
        # Now load the data using the class
        loaded_data = TestData(path=cache_file)
        assert not hasattr(loaded_data, 'e')
        assert loaded_data.a == 1
        assert loaded_data.b == 2.0
        assert loaded_data.c == 'test'
        assert loaded_data.d is True
