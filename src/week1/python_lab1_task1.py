"""
Task 1 – Simple Function with Arithmetic
---------------------------------------
Write a function `circle_area(radius)` that returns the area of a circle.
Formula: area = π × radius²
Use the math module for π.
Ask user for radius and print result with 2 decimals.
"""

import math

def circle_area(radius):
    """return the area of a circle given its radius."""
    area = math.pi * radius ** 2
    return area

if __name__ == "__main__":
    radius = float(input("E,enter the radius of the circle: "))
    area = circle_area(radius)
    print(f"The area of the circle is: {area:.2f}")