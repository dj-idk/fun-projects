from collections import Counter
from typing import Optional


class SmartList(list):
    """
    An enhanced list class that extends Python's built-in list with additional functionality.

    SmartList supports mathematical operations between lists, statistical methods,
    custom slicing behavior, and advanced filtering capabilities.

    Examples:
        >>> nums = SmartList([1, 2, 3, 4, 5])
        >>> nums.mean()
        3.0
        >>> nums.where(lambda x: x > 3)
        [4, 5]
        >>> nums + SmartList([10, 20, 30, 40, 50])
        [11, 22, 33, 44, 55]
    """

    def __add__(self, other):
        """
        Add corresponding elements of two lists.

        Args:
            other: Another list-like object of the same length

        Returns:
            SmartList: A new SmartList with the sum of corresponding elements

        Example:
            >>> SmartList([1, 2, 3]) + SmartList([4, 5, 6])
            [5, 7, 9]
        """
        return type(self)([a + b for a, b in zip(self, other)])

    def __sub__(self, other):
        """
        Subtract corresponding elements of another list from this list.

        Args:
            other: Another list-like object of the same length

        Returns:
            SmartList: A new SmartList with the difference of corresponding elements

        Example:
            >>> SmartList([10, 20, 30]) - SmartList([1, 2, 3])
            [9, 18, 27]
        """
        return type(self)([a - b for a, b in zip(self, other)])

    def __mul__(self, other):
        """
        Multiply corresponding elements of two lists.

        Args:
            other: Another list-like object of the same length

        Returns:
            SmartList: A new SmartList with the product of corresponding elements

        Example:
            >>> SmartList([1, 2, 3]) * SmartList([4, 5, 6])
            [4, 10, 18]
        """
        return type(self)([a * b for a, b in zip(self, other)])

    def __truediv__(self, other):
        """
        Divide corresponding elements of this list by another list.

        Args:
            other: Another list-like object of the same length

        Returns:
            SmartList: A new SmartList with the quotient of corresponding elements

        Example:
            >>> SmartList([10, 20, 30]) / SmartList([2, 5, 10])
            [5.0, 4.0, 3.0]
        """
        return type(self)([a / b for a, b in zip(self, other)])

    def __floordiv__(self, other):
        """
        Floor divide corresponding elements of this list by another list.

        Args:
            other: Another list-like object of the same length

        Returns:
            SmartList: A new SmartList with the floor quotient of corresponding elements

        Example:
            >>> SmartList([10, 20, 30]) // SmartList([3, 7, 4])
            [3, 2, 7]
        """
        return type(self)([a // b for a, b in zip(self, other)])

    def __getitem__(self, key):
        """
        Enhanced indexing and slicing behavior.

        Provides custom handling for slices with step values.

        Args:
            key: An index or slice object

        Returns:
            The item at the specified index or a new SmartList for slices

        Example:
            >>> SmartList([1, 2, 3, 4, 5])[1:5:2]
            [2, 4]
        """
        if isinstance(key, slice):
            start, stop, step = key.start, key.stop, key.step
            if step is not None:
                result = []
                i = start if start is not None else 0
                while i < (stop if stop is not None else len(self)) and i < len(self):
                    result.append(self[i])
                    i += step
                return type(self)(result)
            return super().__getitem__(key)
        else:
            return super().__getitem__(key)

    def mean(self):
        """
        Calculate the arithmetic mean of the list elements.

        Returns:
            float: The mean value of all elements

        Raises:
            ValueError: If the list is empty

        Example:
            >>> SmartList([1, 2, 3, 4, 5]).mean()
            3.0
        """
        if not self:
            raise ValueError("Cannot calculate mean of empty list")
        return sum(self) / len(self)

    def median(self):
        """
        Calculate the median value of the list elements.

        For lists with an even number of elements, returns the average of the two middle values.

        Returns:
            float or numeric: The median value

        Example:
            >>> SmartList([1, 3, 5, 7]).median()
            4.0
            >>> SmartList([1, 3, 5]).median()
            3
        """
        sorted_list = sorted(self)
        length = len(sorted_list)
        if length % 2 == 0:
            return (sorted_list[length // 2 - 1] + sorted_list[length // 2]) / 2
        else:
            return sorted_list[length // 2]

    def mode(self):
        """
        Return the most common element(s) in the list.

        If multiple elements appear with the same frequency, all are returned.

        Returns:
            list: The most frequent element(s)

        Raises:
            ValueError: If the list is empty

        Example:
            >>> SmartList([1, 2, 2, 3, 3, 3, 4]).mode()
            [3]
            >>> SmartList([1, 1, 2, 2]).mode()
            [1, 2]
        """
        if not self:
            raise ValueError("Cannot calculate mode of empty list")

        counter = Counter(self)
        max_count = max(counter.values())
        return [item for item, count in counter.items() if count == max_count]

    def where(self, predicate=None, operator=None, value=None):
        """
        Filter list elements based on a predicate function or comparison.

        This method supports two filtering approaches:
        1. Using a predicate function that returns True/False for each element
        2. Using a comparison operator and value (e.g., ">", 5)

        Args:
            predicate: A function that returns True/False for each element
            operator: Comparison operator (">", "<", "==", "!=", ">=", "<=")
            value: Value to compare against

        Returns:
            SmartList: A new SmartList containing only elements that match the filter

        Raises:
            ValueError: If invalid arguments are provided

        Examples:
            >>> SmartList([1, 2, 3, 4, 5]).where(lambda x: x % 2 == 0)
            [2, 4]
            >>> SmartList([1, 2, 3, 4, 5]).where(operator=">", value=3)
            [4, 5]
        """
        match (predicate, operator, value):
            case (callable, None, None):
                return type(self)([item for item in self if predicate(item)])
            case (None, str(), _):
                return type(self)(
                    [
                        item
                        for item in self
                        if self._evaluate_condition(item, operator, value)
                    ]
                )
            case _:
                raise ValueError(
                    "Invalid arguments. Provide either a predicate function or an operator and value."
                )

    def _evaluate_condition(self, item, operator, value):
        """
        Evaluate a condition based on operator and value.

        Internal helper method used by the where() method to evaluate comparison conditions.

        Args:
            item: The item to compare
            operator: String representation of the comparison operator
            value: The value to compare against

        Returns:
            bool: Result of the comparison

        Raises:
            ValueError: If an unsupported operator is provided
        """
        match operator:
            case "==":
                return item == value
            case "!=":
                return item != value
            case ">":
                return item > value
            case "<":
                return item < value
            case ">=":
                return item >= value
            case "<=":
                return item <= value
            case _:
                raise ValueError(f"Unsupported operator: {operator}")
