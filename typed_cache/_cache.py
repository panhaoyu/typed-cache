import pickle
from pathlib import Path

from ._compatibility import dataclass, fields


@dataclass
class TypedCache:
    """
    A base class for caching data to disk. Subclasses can inherit this class to easily implement data persistence.
    Requires a file path to determine the location of the cache file. Automatically loads cached data (if available) during initialization
    and provides a manual save function to persist the data.

    Attributes:
        path (Path): The file path for the cached data, must have a '.pickle' suffix.

    Methods:
        save(): Manually save the current object's attributes to the cache file.

    Usage:
        1. Define a data class inheriting from TypedCache and specify the attributes that need to be persisted:

            @dataclass
            class Data(TypedCache):
                a: int = None
                b: float = None
                c: str = None
                d: bool = None

        2. When initializing the data class, pass the cache file path and call `save()` when needed to save data:

            data = Data(path=Path.home() / 'Desktop/cache.pickle')
            data.a = 213
            data.save()  # Save data to the specified path

            # When reinitializing, the previously saved data will be automatically loaded
            data = Data(path=Path.home() / 'Desktop/cache.pickle')
            assert data.a == 213

    Raises:
        ValueError: If the path does not have a '.pickle' suffix, this exception is raised.
        FileNotFoundError: If the cache file is not found when attempting to load, this exception is raised.
    """

    path: Path

    def __post_init__(self):
        if self.path.suffix != '.pickle':
            raise ValueError("Cache file must have a '.pickle' suffix")
        self.__load_data()

    def save(self) -> None:
        """
        Manually save the current object's attributes to the cache.
        Automatically excludes the `path` attribute from being saved.
        """
        # Collect the fields without recursively converting nested dataclasses
        data = {
            field.name: getattr(self, field.name)
            for field in fields(self)
            if field.name != 'path'
        }
        self.__save(data)

    def __save(self, data: dict) -> None:
        """
        Save the given data to the cache file.

        Args:
            data (dict): The data to be cached, provided as a dictionary.
        """
        self.path.parent.mkdir(parents=True, exist_ok=True)  # Create parent directories if necessary
        with self.path.open('wb') as f:
            pickle.dump(data, f)

    def __load(self) -> dict:
        """
        Load data from the cache file.

        Returns:
            dict: The data loaded from the cache, returned as a dictionary.

        Raises:
            FileNotFoundError: If the cache file does not exist, this exception is raised.
        """
        if self.path.exists():
            with self.path.open('rb') as f:
                return pickle.load(f)
        else:
            raise FileNotFoundError(f"Cache file {self.path} not found")

    def __load_data(self) -> None:
        """
        Load data from the cache and update the current object's attributes.
        If the cache file does not exist, the object's attributes will not be changed.
        """
        try:
            data = self.__load()
            for key, value in data.items():
                setattr(self, key, value)
        except FileNotFoundError:
            pass  # Ignore if cache does not exist

    def clear(self):
        """Delete the cache file if it exists."""
        self.path.exists() and self.path.unlink()
