# typed-cache

`typed-cache` is a lightweight framework designed for caching data locally, supporting explicit caching with a focus on Python's type hints. It simplifies the process of persisting data to disk by allowing easy integration into custom data classes, with automatic loading and manual saving of data.

## Features

- **Type Hinting**: Enhances code clarity and safety through the use of Python's type hints.
- **Automatic Caching**: Automatically loads cached data on initialization if the file exists.
- **Manual Data Saving**: Allows for explicit control over when data is saved via the `save()` method.
- **File Integrity Checks**: Ensures that cache files use the correct `.pickle` extension and manages errors properly.
- **Python 3.6+ Compatibility**: Works with Python 3.6 and above, making it accessible for most environments.

## Requirements

- Python 3.6+
- Standard libraries: `pickle`, `pathlib`

## Installation

To install `typed-cache`, you can use either `pip` or `poetry`:

### Using `pip`:
```bash
pip install typed-cache
```

### Using `poetry`:
```bash
poetry add typed-cache
```

Simply choose your preferred package manager to install the library.

## Usage

Here's a simple script demonstrating how to use `typed-cache` to persist and retrieve data in a custom class:

```python
from dataclasses import dataclass
from pathlib import Path

from typed_cache import TypedCache


@dataclass
class Settings(TypedCache):
    volume: int = 50
    brightness: float = 0.8
    username: str = "user"


# Specify cache file path
cache_path = Path.home() / 'settings_cache.pickle'

# Initialize settings, modify, and save
settings = Settings(path=cache_path)
settings.volume = 70
settings.save()  # Saves the modified settings to 'settings_cache.pickle'

# On subsequent runs, the previous settings will be automatically loaded
loaded_settings = Settings(path=cache_path)
print(f"Loaded volume: {loaded_settings.volume}")  # Output: Loaded volume: 70
```

### Key Functions:

1. **Initialization**: When you instantiate your class with a cache file path, `typed-cache` will automatically attempt to load data from that file.
2. **Saving**: Call `save()` on your object to persist the current state to the cache file.
3. **Loading**: Upon reinitialization with the same cache path, previously saved data will be loaded automatically.

## Exception Handling

- **`ValueError`**: Raised if the cache file does not have a `.pickle` extension.
- **`FileNotFoundError`**: Raised if trying to load a cache file that does not exist.

## Contributing

Contributions are welcome! Feel free to fork the repository, make improvements, and submit a pull request.

## License

This project is licensed under the MIT License.