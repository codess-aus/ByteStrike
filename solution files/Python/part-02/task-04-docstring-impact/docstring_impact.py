def calculate(a: float, b: float, c: float) -> float:
    """
    Calculate the area of a triangle given three side lengths using Heron's formula.

    Args:
        a: Length of side A
        b: Length of side B
        c: Length of side C

    Returns:
        The area of the triangle
    """
    s = (a + b + c) / 2
    return (s * (s - a) * (s - b) * (s - c)) ** 0.5
