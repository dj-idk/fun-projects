class SmartDict(dict):

    def __getattr__(self, key):
        try:
            match self[key]:
                case str():
                    return self[key]
                case dict():
                    return SmartDict(self[key])
                case _:
                    return self[key]

        except KeyError:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{key}'"
            )

    def __setattr__(self, key, value):
        self[key] = value

    def transform(
        self, transform_function, recursive=True, include_keys=None, exclude_keys=None
    ):
        """
        Apply a transformation function to dictionary values.

        Args:
            transform_function: Function to apply to each value
            recursive: If True, apply to nested dictionaries as well
            include_keys: List of keys to include (if None, include all)
            exclude_keys: List of keys to exclude

        Returns:
            A new SmartDict with transformed values
        """
        result = SmartDict()

        for key, value in self.items():
            if exclude_keys and key in exclude_keys:
                result[key] = value
                continue

            if include_keys is not None and key not in include_keys:
                result[key] = value
                continue

            if recursive and isinstance(value, dict):
                result[key] = SmartDict(value).transform(
                    transform_function, recursive, include_keys, exclude_keys
                )
            elif recursive and isinstance(value, list):
                new_list = []
                for item in value:
                    if isinstance(item, dict):
                        new_list.append(
                            SmartDict(item).transform(
                                transform_function,
                                recursive,
                                include_keys,
                                exclude_keys,
                            )
                        )
                    else:
                        new_list.append(transform_function(item))
                result[key] = new_list
            else:
                result[key] = transform_function(value)

        return result

    def merge(self, other, resolver=None):
        """
        Merge another dictionary into this one with custom conflict resolution.

        Args:
            other: Another dictionary to merge with
            resolver: Function to resolve conflicts. Takes (key, self_value, other_value)
                    and returns the value to use. If None, other's values override self's.

        Returns:
            A new SmartDict with merged values
        """
        result = SmartDict(self.copy())

        for key, other_value in other.items():
            if key in result:
                self_value = result[key]

                if isinstance(self_value, dict) and isinstance(other_value, dict):
                    result[key] = SmartDict(self_value).merge(
                        SmartDict(other_value), resolver
                    )
                elif resolver:
                    result[key] = resolver(key, self_value, other_value)
                else:
                    result[key] = other_value
            else:
                if isinstance(other_value, dict):
                    result[key] = SmartDict(other_value)
                else:
                    result[key] = other_value

        return result
