import tkinter as tk

try:
    from hilbertcurve import generate_hilbert_points
except ImportError:
    from hilbert_curve import generate_hilbert_points


def draw_hilbert_curve(order, canvas_size=500):
    """
    Visualize the Hilbert curve of given order using Tkinter.

    Parameters:
    - order: Order of the Hilbert curve (e.g. 3 -> 8x8).
    - canvas_size: Size of the canvas in pixels (default 500x500).
    """
    points = generate_hilbert_points(order)

    root = tk.Tk()
    root.title(f"Hilbert Curve Visualization (Order {order})")

    margin = 20  # Margin for visualization
    canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg='white')
    canvas.pack()

    max_coord = 2 ** order - 1
    scale = (canvas_size - 2 * margin) / max_coord

    # Normalize and scale the points
    scaled_points = [
        (margin + scale * x, margin + scale * y)
        for x, y in points
    ]

    # Draw connecting lines
    for i in range(len(scaled_points) - 1):
        x0, y0 = scaled_points[i]
        x1, y1 = scaled_points[i + 1]
        canvas.create_line(x0, y0, x1, y1, fill="blue", width=2)

    return root  # Return the root window for mainloop to be called externally


if __name__ == "__main__":
    # Example usage when the script is run directly
    order = 3  # You can change the order here
    root_window = draw_hilbert_curve(order)
    root_window.mainloop()
