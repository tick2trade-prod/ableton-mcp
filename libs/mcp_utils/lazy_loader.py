"""Lazy loader utility for deferred initialization with caching."""

from collections.abc import Callable
from typing import Any


class LazyLoader:
    """Lazy loader that defers initialization until first access.

    This class provides a simple way to lazily initialize expensive resources
    and cache them for subsequent access.

    Example:
        >>> loader = LazyLoader(lambda: expensive_operation())
        >>> value = loader.get()  # First call initializes
        >>> value2 = loader.get()  # Subsequent calls return cached value
    """

    def __init__(self, factory: Callable[[], Any]) -> None:
        """Initialize lazy loader with a factory function.

        Args:
            factory: Callable that returns the value to be lazily loaded.
                     Will be called only once on first access.
        """
        self._factory = factory
        self._value: Any | None = None
        self._initialized = False

    def get(self) -> Any:
        """Get the value, initializing it if necessary.

        Returns:
            The value returned by the factory function.
            Subsequent calls return the same cached value.
        """
        if not self._initialized:
            self._value = self._factory()
            self._initialized = True
        return self._value

    def reset(self) -> None:
        """Reset the loader, forcing re-initialization on next access."""
        self._value = None
        self._initialized = False
