import pint
import pandas as pd

convert = pint.UnitRegistry().Quantity


class UnitConverter:

    @staticmethod
    def convert_vector(vector, from_unit:'str', to_unit:'str') -> pd:
        """
        Convert a list, tuple, or pandas Series of numbers from one unit to another.
        Raises:
            TypeError: if input is not a valid sequence
            ValueError: if units are not valid
        """

        # Check if vector is list-like
        if not isinstance(vector, (list, tuple, pd.Series)):
            raise TypeError("Input must be a list, tuple, or pandas Series.")

        # Check if units are valid using Pint
        try:
            pint.UnitRegistry().Unit(from_unit)
            pint.UnitRegistry().Unit(to_unit)

        except convert.UndefinedUnitError as e:
            raise ValueError(f"Typed Invalid unit: {e}")

        # Convert each value in vector 
        return [convert(value, from_unit).to(to_unit).magnitude for value in vector]
    


    @staticmethod
    def convert_value(var, from_unit:'str', to_unit:'str') -> float:
        """
        Convert a value from one unit to another.
        Returns magnitudes (floats).
        Raises:
            TypeError: if input is not a valid sequence
            ValueError: if units are not valid
        """

        # Check if vector is list-like
        if not isinstance(var, (int, float)):
            raise TypeError("Input must be a float and integer.")

        # Check if units are valid using Pint
        try:
            pint.UnitRegistry().Unit(from_unit)
            pint.UnitRegistry().Unit(to_unit)

        except pint.errors.UndefinedUnitError as e:
            raise ValueError(f"Typed Invalid unit: {e}")

        # Convert each value
        return float(convert(var, from_unit).to(to_unit).magnitude)
    
    