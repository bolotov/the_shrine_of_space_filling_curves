"""
Manual implementation of Hilbert curve mappings for 2D space.
Includes bidirectional conversion between curve index and (x, y) coordinates,
with partial compatibility functions for the `hilbertcurve` module.
"""

from typing import Tuple, Dict  # List


#### MARK: Static Reference / visual aid

# Numbers of steps along Hilbert curve of order 3.
HILBERT_3 = (
    ( 0,  3,  4,  5, 58, 59, 60, 63),  #  v┌─┐┌─┐^
    ( 1,  2,  7,  6, 57, 56, 61, 62),  #  └┘┌┘└┐└┘
    (14, 13,  8,  9, 54, 55, 50, 49),  #  ┌┐└┐┌┘┌┐
    (15, 12, 11, 10, 53, 52, 51, 48),  #  │└─┘└─┘│
    (16, 17, 30, 31, 32, 33, 46, 47),  #  └┐┌──┐┌┘
    (19, 18, 29, 28, 35, 34, 45, 44),  #  ┌┘└┐┌┘└┐
    (20, 23, 24, 27, 36, 39, 40, 43),  #  │┌┐││┌┐│
    (21, 22, 25, 26, 37, 38, 41, 42),  #  └┘└┘└┘└┘
)


#### MARK: Public API

def hilbert_index_to_point(order: int, index: int) -> Tuple[int, int]:
    """
    Convert a Hilbert curve index to a 2D point (x, y).

    Parameters:
    - order: Order of the Hilbert curve (n).
    - index: Index of the point along the Hilbert curve.

    Returns:
    - (x, y): Tuple representing the 2D point.
    """
    n = 2 ** order
    x, y = 0, 0
    t = index
    s = 1
    while s < n:
        rx = 1 & (t // 2)
        ry = 1 & (t ^ rx)
        x, y = _hilbert_rotate(s, x, y, rx, ry)
        x += s * rx
        y += s * ry
        t //= 4
        s *= 2
    return x, y

def point_to_hilbert_index(x: int, y: int, order: int) -> int:
    """
    Convert a 2D point (x, y) to a Hilbert curve index.

    Parameters:
    - x, y: Coordinates on a 2D grid.
    - order: Order of the Hilbert curve (n), where grid is 2^n x 2^n.

    Returns:
    - index: Position of the point along the Hilbert curve.
    """
    n = 2 ** order
    index = 0
    s = n // 2
    while s > 0:
        rx = 1 if (x & s) > 0 else 0
        ry = 1 if (y & s) > 0 else 0
        index += s * s * ((3 * rx) ^ ry)
        x, y = _hilbert_rotate(s, x, y, rx, ry)
        s //= 2
    return index

def generate_hilbert_points(order: int) -> Tuple[Tuple[int, int], ...]:
    """
    Generate all (x, y) points on the Hilbert curve for a given order.

    Parameters:
    - order: Order of the Hilbert curve.

    Returns:
    - List of (x, y) coordinates corresponding to the Hilbert curve traversal.
    """
    num_points = 2 ** (2 * order)
    return tuple(hilbert_index_to_point(order, i) for i in range(num_points))

def hilbert_curve_to_coordinates(grid: tuple[tuple[int]]) -> Dict[int, Tuple[int, int]]:
    """
    Convert a 2D array/grid of Hilbert indices to a mapping: index → (x, y)

    Parameters:
    - grid: Tuple of tuples or list of lists containing Hilbert indices.

    Returns:
    - Dictionary: {index: (x, y)} for all positions in the grid.
    """
    return {val: (x, y) for x, row in enumerate(grid) for y, val in enumerate(row)}

def hilbert_index_matrix(order: int) -> Tuple[Tuple[int, ...], ...]:
    """
    Returns a 2D matrix of shape (2^order x 2^order) where each cell
    contains the Hilbert index corresponding to that (x, y) coordinate.

    This is pedagogically useful for visualizing the curve layout.

    Parameters:
    - order: The order of the Hilbert curve.

    Returns:
    - matrix: 2D list such that matrix[x][y] = hilbert index
    """
    size = 2 ** order
    return tuple(
        tuple(point_to_hilbert_index(x, y, order) for y in range(size))
        for x in range(size)
    )


#### MARK: Internal

def _hilbert_rotate(n: int, x: int, y: int, rx: int, ry: int) -> Tuple[int, int]:
    """
    Rotate and flip quadrant as needed during Hilbert index computation.

    Parameters:
    - n: Grid size at this recursion level.
    - x, y: Coordinates.
    - rx, ry: Bit flags for quadrant rotation.

    Returns:
    - (x, y): Transformed coordinates.
    """
    if ry == 0:
        if rx == 1:
            x = n - 1 - x
            y = n - 1 - y
        x, y = y, x
    return x, y


#### MARK: Convenience and ompatibility Functions

def point_from_distance(order: int, index: int):
    """(hilbertcurve module compatible) Alias for `hilbert_index_to_point`."""
    return hilbert_index_to_point(order, index)

def distance_from_point(order: int, x: int, y: int):
    """(hilbertcurve module compatible) Alias for `point_to_hilbert_index`."""
    return point_to_hilbert_index(x, y, order)

def hilbert_position_at(x: int, y: int) -> int:
    """
    Test/educational function for 3rd-order Hilbert curve.
    Return the Hilbert index at a specific (x, y) position in order-3 layout.

    Returns:
    - Index (int)
    """
    return HILBERT_3[x][y]


### MARK: Main for Testing and Visualization

if __name__ == "__main__":
    order = 3
    print("Generating order-3 Hilbert curve points:\n")
    for i, pt in enumerate(generate_hilbert_points(order)):
        print(f"{i:02d} → {pt}")

    print("\nVerify inverse mapping:")
    for i in range(64):
        pt = hilbert_index_to_point(order, i)
        idx = point_to_hilbert_index(*pt, order)
        assert idx == i, f"Mismatch: {i} -> {pt} -> {idx}"

    print("✔ All index↔point mappings passed.")
