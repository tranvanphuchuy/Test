import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math

# Variables for user input entries
num_arms_entry = None
backbone_entry = None
side_chains_entry = None
side_chain_entries = []
backbone_points_entry = None
ring_points_entry = None
oxygen_points_entry = None

# Variables to store polymer data
coordinates = []
bonds = []
angles = []
oxygen_points = set()

# Function to draw star polymer
def draw_star_polymer(num_arms, arm_lengths):
    global coordinates, bonds, angles
    canvas.delete("all")
    coordinates = []
    bonds = []
    angles = []

    central_x = 300
    central_y = 150
    central_z = 0  # Assume z-coordinate is 0 for 2D representation
    ball_radius = 5
    arm_spacing = 20

    # Draw central node
    coordinates.append((central_x, central_y, central_z))
    color = "blue" if 1 in oxygen_points else "purple"
    canvas.create_oval(central_x - ball_radius * 2, central_y - ball_radius * 2,
                       central_x + ball_radius * 2, central_y + ball_radius * 2, fill=color, outline="")

    # Draw arms
    bead_index = 1
    for i, arm_length in enumerate(arm_lengths):
        angle = 2 * i * math.pi / num_arms
        for j in range(arm_length):
            x = central_x + (j + 1) * arm_spacing * math.cos(angle)
            y = central_y - (j + 1) * arm_spacing * math.sin(angle)
            coordinates.append((x, y, central_z))
            bead_index += 1
            color = "blue" if bead_index in oxygen_points else "purple"
            circle = canvas.create_oval(x - ball_radius, y - ball_radius, x + ball_radius, y + ball_radius, fill=color, outline="")
            bind_tooltip(canvas, circle, bead_index, x, y)
            if j == 0:
                canvas.create_line(central_x, central_y, x, y, width=2, fill="purple")
            else:
                prev_x, prev_y, _ = coordinates[-2]
                canvas.create_line(prev_x, prev_y, x, y, width=2, fill="purple")
            bonds.append((bead_index, bead_index + 1))

# Function to draw graft polymer
def draw_graft_polymer(backbone_length, num_side_chains, side_chain_positions, side_chain_lengths):
    global coordinates, bonds, angles
    canvas.delete("all")
    coordinates = []
    bonds = []
    angles = []

    ball_radius = 5
    backbone_length_px = 500
    backbone_length_scale = backbone_length_px / (backbone_length - 1)
    side_chain_spacing = 20

    # Draw backbone
    for i in range(backbone_length):
        x = 50 + i * backbone_length_scale
        y = 150
        z = 0  # Assume z-coordinate is 0 for 2D representation
        coordinates.append((x, y, z))
        color = "blue" if (i + 1) in oxygen_points else "purple"
        circle = canvas.create_oval(x - ball_radius, y - ball_radius, x + ball_radius, y + ball_radius, fill=color, outline="")
        bind_tooltip(canvas, circle, i + 1, x, y)
        if i < backbone_length - 1:
            next_x = 50 + (i + 1) * backbone_length_scale
            next_y = 150
            canvas.create_line(x, y, next_x, next_y, width=2, fill="purple")
            bonds.append((i + 1, i + 2))

    # Draw side chains
    bead_index = backbone_length
    for i in range(num_side_chains):
        position = side_chain_positions[i]
        length = side_chain_lengths[i]
        backbone_x = 50 + (position - 1) * backbone_length_scale
        backbone_y = 150
        side_chain_x = backbone_x
        side_chain_y = backbone_y + ball_radius + 10

        start_index = position
        for j in range(length):
            coordinates.append((side_chain_x, side_chain_y, z))
            bead_index += 1
            color = "blue" if bead_index in oxygen_points else "purple"
            circle = canvas.create_oval(side_chain_x - ball_radius, side_chain_y - ball_radius,
                                        side_chain_x + ball_radius, side_chain_y + ball_radius, fill=color, outline="")
            bind_tooltip(canvas, circle, bead_index, side_chain_x, side_chain_y)
            if j == 0:
                canvas.create_line(backbone_x, backbone_y, side_chain_x, side_chain_y, width=2, fill="purple")
            else:
                prev_x, prev_y, _ = coordinates[-2]
                canvas.create_line(prev_x, prev_y, side_chain_x, side_chain_y, width=2, fill="purple")
            bonds.append((start_index if j == 0 else bead_index - 1, bead_index))
            side_chain_y += side_chain_spacing

# Function to draw linear polymer
def draw_linear_polymer(backbone_points):
    global coordinates, bonds, angles
    canvas.delete("all")
    coordinates = []
    bonds = []
    angles = []

    ball_radius = 5
    backbone_length_px = 500
    backbone_length_scale = backbone_length_px / (backbone_points - 1)

    # Draw backbone
    for i in range(backbone_points):
        x = 50 + i * backbone_length_scale
        y = 150
        z = 0  # Assume z-coordinate is 0 for 2D representation
        coordinates.append((x, y, z))
        color = "blue" if (i + 1) in oxygen_points else "purple"
        circle = canvas.create_oval(x - ball_radius, y - ball_radius, x + ball_radius, y + ball_radius, fill=color, outline="")
        bind_tooltip(canvas, circle, i + 1, x, y)
        if i < backbone_points - 1:
            next_x = 50 + (i + 1) * backbone_length_scale
            next_y = 150
            canvas.create_line(x, y, next_x, next_y, width=2, fill="purple")
            bonds.append((i + 1, i + 2))

# Function to draw ring polymer
def draw_ring_polymer(num_points):
    global coordinates, bonds, angles
    canvas.delete("all")
    coordinates = []
    bonds = []
    angles = []

    central_x = 300
    central_y = 150
    radius = 100
    ball_radius = 5
    z = 0  # Assume z-coordinate is 0 for 2D representation

    points = []
    for i in range(num_points):
        angle = 2 * i * math.pi / num_points
        x = central_x + radius * math.cos(angle)
        y = central_y + radius * math.sin(angle)
        coordinates.append((x, y, z))
        color = "blue" if (i + 1) in oxygen_points else "purple"
        circle = canvas.create_oval(x - ball_radius, y - ball_radius, x + ball_radius, y + ball_radius, fill=color, outline="")
        bind_tooltip(canvas, circle, i + 1, x, y)
        points.append((x, y))
        if i > 0:
            prev_x, prev_y = points[i - 1]
            canvas.create_line(prev_x, prev_y, x, y, width=2, fill="purple")
            bonds.append((i, i + 1))

    # Connect last point to first point to close the ring
    canvas.create_line(points[-1][0], points[-1][1], points[0][0], points[0][1], width=2, fill="purple")
    bonds.append((num_points, 1))

# Function to bind tooltips to canvas items
def bind_tooltip(canvas, item, index, x, y):
    tooltip = None
    def show_tooltip(event):
        nonlocal tooltip
        if tooltip is None:
            tooltip = canvas.create_text(x, y - 15, text=f"({index}, {x:.2f}, {y:.2f})", anchor="s", fill="black")

    def hide_tooltip(event):
        nonlocal tooltip
        if tooltip is not None:
            canvas.delete(tooltip)
            tooltip = None

    canvas.tag_bind(item, "<Enter>", show_tooltip)
    canvas.tag_bind(item, "<Leave>", hide_tooltip)

# Function to set up input fields for graft polymer
def setup_graft_input(root, input_frame):
    global backbone_entry, side_chains_entry, side_chain_entries

    for widget in input_frame.winfo_children():
        widget.destroy()

    ttk.Label(input_frame, text="Backbone Length:").grid(row=0, column=0, pady=5, sticky='w')
    backbone_entry = ttk.Entry(input_frame, width=10)
    backbone_entry.grid(row=0, column=1, pady=5, sticky='w')

    ttk.Label(input_frame, text="Number of Side Chains:").grid(row=1, column=0, pady=5, sticky='w')
    side_chains_entry = ttk.Entry(input_frame, width=10)
    side_chains_entry.grid(row=1, column=1, pady=5, sticky='w')

    def add_side_chain_fields():
        try:
            backbone_length = int(backbone_entry.get())
            num_side_chains = int(side_chains_entry.get())

            if backbone_length < 0 or num_side_chains < 0:
                tk.messagebox.showerror("Error", "Values cannot be negative.")
                return

            if num_side_chains > backbone_length:
                tk.messagebox.showerror("Error", "Number of side chains cannot be higher than the backbone length.")
                return

            side_chain_entries.clear()

            for i in range(num_side_chains):
                ttk.Label(input_frame, text=f"Position of Side Chain {i + 1}:").grid(row=i + 2, column=0, pady=5, sticky='w')
                position_entry = ttk.Entry(input_frame, width=10)
                position_entry.grid(row=i + 2, column=1, pady=5, sticky='w')
                side_chain_entries.append(position_entry)

                ttk.Label(input_frame, text=f"Length of Side Chain {i + 1}:").grid(row=i + 2, column=2, pady=5, sticky='w')
                length_entry = ttk.Entry(input_frame, width=10)
                length_entry.grid(row=i + 2, column=3, pady=5, sticky='w')
                side_chain_entries.append(length_entry)

        except ValueError:
            tk.messagebox.showerror("Error", "Please enter valid numbers for backbone length and side chains.")

    add_button = ttk.Button(input_frame, text="Add Side Chains", command=add_side_chain_fields)
    add_button.grid(row=2, column=0, columnspan=4, pady=10)

# Function to set up input fields for star polymer
def setup_star_input(root, input_frame):
    global num_arms_entry, arm_length_entries
    for widget in input_frame.winfo_children():
        widget.destroy()

    ttk.Label(input_frame, text="Number of Arms:").grid(row=0, column=0, pady=5, sticky='w')
    num_arms_entry = ttk.Entry(input_frame, width=10)
    num_arms_entry.grid(row=0, column=1, pady=5, sticky='w')

    def add_arm_fields():
        try:
            num_arms = int(num_arms_entry.get())

            if num_arms < 0:
                tk.messagebox.showerror("Error", "Values cannot be negative.")
                return

            for widget in input_frame.winfo_children()[2:]:
                widget.destroy()

            for i in range(1, 1 + num_arms):
                ttk.Label(input_frame, text=f"Length of Arm {i}:").grid(row=i, column=0, pady=5, sticky='w')
                entry = ttk.Entry(input_frame, width=10)
                entry.grid(row=i, column=1, pady=5, sticky='w')
                arm_length_entries.append(entry)

        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid number for arms.")

    add_button = ttk.Button(input_frame, text="Add Arm Lengths", command=add_arm_fields)
    add_button.grid(row=1, column=0, columnspan=2, pady=10)

# Function to set up input fields for linear polymer
def setup_linear_input(root, input_frame):
    global backbone_points_entry
    for widget in input_frame.winfo_children():
        widget.destroy()

    ttk.Label(input_frame, text="Number of Backbone Points:").grid(row=0, column=0, pady=5, sticky='w')
    backbone_points_entry = ttk.Entry(input_frame, width=10)
    backbone_points_entry.grid(row=0, column=1, pady=5, sticky='w')

# Function to set up input fields for ring polymer
def setup_ring_input(root, input_frame):
    global ring_points_entry
    for widget in input_frame.winfo_children():
        widget.destroy()

    ttk.Label(input_frame, text="Number of Points on Ring:").grid(row=0, column=0, pady=5, sticky='w')
    ring_points_entry = ttk.Entry(input_frame, width=10)
    ring_points_entry.grid(row=0, column=1, pady=5, sticky='w')

# Function to generate the polymer based on user input
def generate():
    try:
        global oxygen_points
        oxygen_points = set()
        if oxygen_points_entry.get():
            oxygen_points = set(map(int, oxygen_points_entry.get().split(',')))

        if polymer_type.get() == "star":
            num_arms = int(num_arms_entry.get())
            arm_lengths = [int(entry.get()) for entry in arm_length_entries]
            if num_arms < 0 or any(length < 0 for length in arm_lengths):
                tk.messagebox.showerror("Error", "Values cannot be negative.")
                return
            generate_polymer("star", num_arms, arm_lengths)
        elif polymer_type.get() == "graft":
            backbone_length = int(backbone_entry.get())
            num_side_chains = int(side_chains_entry.get())
            side_chain_positions = []
            side_chain_lengths = []
            for i in range(len(side_chain_entries) // 2):
                position_entry = side_chain_entries[i * 2]
                length_entry = side_chain_entries[i * 2 + 1]
                if position_entry.get().isdigit() and length_entry.get().isdigit():
                    position = int(position_entry.get())
                    length = int(length_entry.get())
                    if position < 0 or length < 0:
                        tk.messagebox.showerror("Error", "Values cannot be negative.")
                        return
                    side_chain_positions.append(position)
                    side_chain_lengths.append(length)
                else:
                    tk.messagebox.showerror("Error", "Invalid input for side chain position or length.")
                    return

            if any(length > backbone_length for length in side_chain_lengths):
                tk.messagebox.showerror("Error", "Side chain length cannot be higher than backbone length.")
                return

            generate_polymer("graft", backbone_length, num_side_chains, side_chain_positions, side_chain_lengths)
        elif polymer_type.get() == "linear":
            backbone_points = int(backbone_points_entry.get())
            if backbone_points < 0:
                tk.messagebox.showerror("Error", "Values cannot be negative.")
                return
            generate_polymer("linear", backbone_points)
        elif polymer_type.get() == "ring":
            ring_points = int(ring_points_entry.get())
            if ring_points < 0:
                tk.messagebox.showerror("Error", "Values cannot be negative.")
                return
            generate_polymer("ring", ring_points)
        show_tables()
    except ValueError:
        tk.messagebox.showerror("Error", "Please enter valid numbers.")

# Function to call the appropriate drawing function
def generate_polymer(polymer_type, *args):
    if polymer_type == "star":
        draw_star_polymer(*args)
    elif polymer_type == "graft":
        draw_graft_polymer(*args)
    elif polymer_type == "linear":
        draw_linear_polymer(*args)
    elif polymer_type == "ring":
        draw_ring_polymer(*args)

# Function to save coordinate file
def save_coordinate_file():
    coord_file_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Save Coordinate File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if coord_file_path:
        with open(coord_file_path, 'w') as coord_file:
            coord_file.write("Beads\tx\ty\tz\n")
            for index, (x, y, z) in enumerate(coordinates, start=1):
                coord_file.write(f"{index}\t{x:.2f}\t{y:.2f}\t{z:.2f}\n")

# Function to save bond file
def save_bond_file():
    bond_file_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Save Bond File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if bond_file_path:
        with open(bond_file_path, 'w') as bond_file:
            bond_file.write("Node\tNeighbors\tChemical Bond\n")
            for i in range(1, len(coordinates) + 1):
                neighbors = [str(j) for j in range(1, len(coordinates) + 1) if (i, j) in bonds or (j, i) in bonds]
                bond_types = [2 if j in oxygen_points else 1 for j in range(1, len(coordinates) + 1) if (i, j) in bonds or (j, i) in bonds]
                bond_file.write(f"{i}\t{','.join(neighbors)}\t{','.join(map(str, bond_types))}\n")

# Function to display tables of coordinates and bonds
def show_tables():
    coordinate_table.delete(*coordinate_table.get_children())
    bond_table.delete(*bond_table.get_children())

    for index, (x, y, z) in enumerate(coordinates, start=1):
        coordinate_table.insert("", "end", values=(index, f"{x:.2f}", f"{y:.2f}", f"{z:.2f}"))

    for i in range(1, len(coordinates) + 1):
        neighbors = [str(j) for j in range(1, len(coordinates) + 1) if (i, j) in bonds or (j, i) in bonds]
        bond_types = [2 if j in oxygen_points else 1 for j in range(1, len(coordinates) + 1) if (i, j) in bonds or (j, i) in bonds]
        bond_table.insert("", "end", values=(i, ','.join(neighbors), ','.join(map(str, bond_types))))

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Polymer Generator")
root.geometry("800x600")

# Create a style for the widgets
style = ttk.Style(root)
style.configure('TFrame', background='#f0f0f0')
style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
style.configure('TButton', font=('Arial', 10))
style.configure('TRadiobutton', background='#f0f0f0', font=('Arial', 10))

# Create and pack frames for buttons, inputs, and canvas
button_frame = ttk.Frame(root, padding="10 10 10 10")
button_frame.pack(side='top', fill='x', padx=10, pady=5)

input_frame = ttk.Frame(root, padding="10 10 10 10")
input_frame.pack(fill='both', expand=True, padx=10, pady=5)

canvas_frame = ttk.Frame(root, padding="10 10 10 10")
canvas_frame.pack(fill='both', expand=True, padx=10, pady=5)

# Table frames for coordinates and bonds
table_frame = ttk.Frame(root, padding="10 10 10 10")
table_frame.pack(fill='both', expand=True, padx=10, pady=5)

coordinate_table_label = ttk.Label(table_frame, text="Coordinate Table")
coordinate_table_label.pack()

coordinate_table = ttk.Treeview(table_frame, columns=("Beads", "x", "y", "z"), show='headings', height=5)
coordinate_table.heading("Beads", text="Beads")
coordinate_table.heading("x", text="x")
coordinate_table.heading("y", text="y")
coordinate_table.heading("z", text="z")
coordinate_table.pack(side='left', fill='both', expand=True)

bond_table_label = ttk.Label(table_frame, text="Bond Table")
bond_table_label.pack()

bond_table = ttk.Treeview(table_frame, columns=("Node", "Neighbors", "Chemical Bond"), show='headings', height=5)
bond_table.heading("Node", text="Node")
bond_table.heading("Neighbors", text="Neighbors")
bond_table.heading("Chemical Bond", text="Chemical Bond")
bond_table.pack(side='left', fill='both', expand=True)

# Radio buttons to select the polymer type
polymer_type = tk.StringVar()
star_radio_button = ttk.Radiobutton(button_frame, text="Star", variable=polymer_type, value="star",
                                    command=lambda: setup_star_input(root, input_frame))
star_radio_button.pack(side=tk.LEFT, padx=5, pady=5)
graft_radio_button = ttk.Radiobutton(button_frame, text="Graft", variable=polymer_type, value="graft",
                                     command=lambda: setup_graft_input(root, input_frame))
graft_radio_button.pack(side=tk.LEFT, padx=5, pady=5)
linear_radio_button = ttk.Radiobutton(button_frame, text="Linear", variable=polymer_type, value="linear",
                                      command=lambda: setup_linear_input(root, input_frame))
linear_radio_button.pack(side=tk.LEFT, padx=5, pady=5)
ring_radio_button = ttk.Radiobutton(button_frame, text="Ring", variable=polymer_type, value="ring",
                                    command=lambda: setup_ring_input(root, input_frame))
ring_radio_button.pack(side=tk.LEFT, padx=5, pady=5)

# Button to generate the polymer
generate_button = ttk.Button(button_frame, text="Generate", command=generate)
generate_button.pack(side=tk.LEFT, padx=5, pady=5)

# Button to save the coordinate file
save_coord_button = ttk.Button(button_frame, text="Save Coordinate File", command=save_coordinate_file)
save_coord_button.pack(side=tk.LEFT, padx=5, pady=5)

# Button to save the bond file
save_bond_button = ttk.Button(button_frame, text="Save Bond File", command=save_bond_file)
save_bond_button.pack(side=tk.LEFT, padx=5, pady=5)

# Entry and button to specify oxygen points
ttk.Label(button_frame, text="Oxygen Points (comma-separated):").pack(side=tk.LEFT, padx=5, pady=5)
oxygen_points_entry = ttk.Entry(button_frame, width=20)
oxygen_points_entry.pack(side=tk.LEFT, padx=5, pady=5)
apply_oxygen_button = ttk.Button(button_frame, text="Apply Oxygen Points", command=generate)
apply_oxygen_button.pack(side=tk.LEFT, padx=5, pady=5)

# Canvas to draw the polymer
canvas = tk.Canvas(canvas_frame, width=600, height=300, bg="white")
canvas.pack()

# Initialize entry lists for dynamic input fields
arm_length_entries = []

# Start the Tkinter event loop
root.mainloop()
