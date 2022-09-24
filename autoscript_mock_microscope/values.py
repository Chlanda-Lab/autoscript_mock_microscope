from typing import List, Tuple, Optional
from collections import namedtuple

class ListValue:
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.available_values is None or new_value in self.available_values:
            self._value = new_value
        elif self.select_closest:
            # If the closest value is supposed to be set (e.g. ion beam apertures), find and set it
            diffs = [abs(available_value - new_value) for available_value in self.available_values]
            index = self.available_values.index(min(diffs))
            self._value = self.available_values[index]
        else:
            raise ValueError('new_value not in available_values')

    def __init__(self, initial_value, available_values: List, select_closest: bool=False):
        self.available_values = available_values
        self.select_closest = select_closest
        self.value = initial_value


class LimitValue:
    Limits = namedtuple('Limits', ['min', 'max'])

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.limits is not None and self.limits.min > new_value > self.limits.max:
            raise ValueError(f'The value {new_value} is outside the limits of {self.limits}')
        self._value = new_value

    def __init__(self, initial_value, limits: Optional[Tuple]=None):
        self.limits = LimitValue.Limits(min(limits), max(limits)) if limits is not None else None
        self.value = initial_value


