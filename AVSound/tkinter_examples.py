#!/usr/bin/env python3
"""
Tkinter Examples - A collection of simple Tkinter GUI examples
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

# Example 1: Simple Window
def simple_window():
    """Create a simple window with a label and button"""
    root = tk.Tk()
    root.title("Simple Window")
    root.geometry("300x200")
    
    # Add a label
    label = tk.Label(root, text="Hello, Tkinter!", font=("Arial", 16))
    label.pack(pady=20)
    
    # Add a button
    button = tk.Button(root, text="Click Me!", command=lambda: messagebox.showinfo("Info", "Button clicked!"))
    button.pack(pady=10)
    
    root.mainloop()

# Example 2: Using ttk Widgets
def ttk_example():
    """Demonstrate ttk widgets for a more modern look"""
    root = tk.Tk()
    root.title("TTK Widgets Example")
    root.geometry("400x300")
    
    # Create a frame for better layout
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # TTK Label
    title = ttk.Label(main_frame, text="TTK Widgets Demo", font=("Arial", 16, "bold"))
    title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
    
    # TTK Entry
    ttk.Label(main_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
    name_entry = ttk.Entry(main_frame, width=30)
    name_entry.grid(row=1, column=1, pady=5)
    
    # TTK Combobox
    ttk.Label(main_frame, text="Country:").grid(row=2, column=0, sticky=tk.W, pady=5)
    country_var = tk.StringVar()
    country_combo = ttk.Combobox(main_frame, textvariable=country_var, 
                                values=["USA", "Canada", "UK", "Germany", "Japan"])
    country_combo.grid(row=2, column=1, pady=5)
    country_combo.set("Select Country")
    
    # TTK Checkbuttons
    newsletter_var = tk.BooleanVar()
    newsletter_check = ttk.Checkbutton(main_frame, text="Subscribe to newsletter", 
                                      variable=newsletter_var)
    newsletter_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
    
    # TTK Radiobuttons
    gender_var = tk.StringVar()
    ttk.Label(main_frame, text="Gender:").grid(row=4, column=0, sticky=tk.W, pady=(10, 5))
    ttk.Radiobutton(main_frame, text="Male", variable=gender_var, value="Male").grid(row=5, column=0, sticky=tk.W)
    ttk.Radiobutton(main_frame, text="Female", variable=gender_var, value="Female").grid(row=5, column=1, sticky=tk.W)
    
    # TTK Button
    submit_btn = ttk.Button(main_frame, text="Submit", 
                           command=lambda: messagebox.showinfo("Form Data", 
                           f"Name: {name_entry.get()}\nCountry: {country_var.get()}\nNewsletter: {newsletter_var.get()}\nGender: {gender_var.get()}"))
    submit_btn.grid(row=6, column=0, columnspan=2, pady=20)
    
    root.mainloop()

# Example 3: Layout Management
def layout_example():
    """Demonstrate different layout managers"""
    root = tk.Tk()
    root.title("Layout Management")
    root.geometry("500x400")
    
    # Pack layout example
    pack_frame = ttk.LabelFrame(root, text="Pack Layout", padding="10")
    pack_frame.pack(fill=tk.X, padx=10, pady=5)
    
    tk.Label(pack_frame, text="Pack organizes widgets horizontally or vertically").pack()
    tk.Button(pack_frame, text="Button 1").pack(side=tk.LEFT, padx=5)
    tk.Button(pack_frame, text="Button 2").pack(side=tk.LEFT, padx=5)
    tk.Button(pack_frame, text="Button 3").pack(side=tk.RIGHT, padx=5)
    
    # Grid layout example
    grid_frame = ttk.LabelFrame(root, text="Grid Layout", padding="10")
    grid_frame.pack(fill=tk.X, padx=10, pady=5)
    
    tk.Label(grid_frame, text="Grid arranges widgets in rows and columns").grid(row=0, column=0, columnspan=3)
    for i in range(3):
        for j in range(3):
            tk.Button(grid_frame, text=f"Btn {i},{j}").grid(row=i+1, column=j, padx=2, pady=2)
    
    # Place layout example
    place_frame = ttk.LabelFrame(root, text="Place Layout", padding="10")
    place_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    tk.Label(place_frame, text="Place allows precise positioning").place(x=10, y=10)
    tk.Button(place_frame, text="Positioned Button").place(x=50, y=50)
    tk.Button(place_frame, text="Another Button").place(relx=0.8, rely=0.8, anchor=tk.SE)
    
    root.mainloop()

# Example 4: Event Handling
def event_handling():
    """Demonstrate event handling in Tkinter"""
    root = tk.Tk()
    root.title("Event Handling")
    root.geometry("400x300")
    
    # Create widgets
    entry = ttk.Entry(root, width=30)
    entry.pack(pady=10)
    
    label = ttk.Label(root, text="Type something above")
    label.pack(pady=10)
    
    # Event handlers
    def on_key_press(event):
        label.config(text=f"You pressed: {event.keysym}")
    
    def on_mouse_click(event):
        label.config(text=f"Mouse clicked at ({event.x}, {event.y})")
    
    def on_focus_in(event):
        label.config(text="Entry focused")
    
    def on_focus_out(event):
        label.config(text="Entry lost focus")
    
    # Bind events
    entry.bind("<Key>", on_key_press)
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    
    # Create a canvas for mouse events
    canvas = tk.Canvas(root, bg="lightblue", width=300, height=100)
    canvas.pack(pady=10)
    canvas.bind("<Button-1>", on_mouse_click)
    canvas.create_text(150, 50, text="Click me!", font=("Arial", 16))
    
    root.mainloop()

# Example 5: File Dialogs
def file_dialogs():
    """Demonstrate file dialogs"""
    root = tk.Tk()
    root.title("File Dialogs")
    root.geometry("400x300")
    
    def open_file():
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            messagebox.showinfo("File Selected", f"You selected:\n{file_path}")
    
    def save_file():
        file_path = filedialog.asksaveasfilename(
            title="Save file",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            messagebox.showinfo("File to Save", f"You will save to:\n{file_path}")
    
    def select_directory():
        dir_path = filedialog.askdirectory(title="Select a directory")
        if dir_path:
            messagebox.showinfo("Directory Selected", f"You selected:\n{dir_path}")
    
    # Create buttons
    ttk.Button(root, text="Open File", command=open_file).pack(pady=10)
    ttk.Button(root, text="Save File", command=save_file).pack(pady=10)
    ttk.Button(root, text="Select Directory", command=select_directory).pack(pady=10)
    
    root.mainloop()

# Main menu to select examples
def main():
    """Main menu to select which example to run"""
    root = tk.Tk()
    root.title("Tkinter Examples")
    root.geometry("400x300")
    
    # Title
    title = ttk.Label(root, text="Tkinter Examples", font=("Arial", 18, "bold"))
    title.pack(pady=20)
    
    # Description
    desc = ttk.Label(root, text="Select an example to run:", font=("Arial", 12))
    desc.pack(pady=10)
    
    # Example buttons
    examples = [
        ("Simple Window", simple_window),
        ("TTK Widgets", ttk_example),
        ("Layout Management", layout_example),
        ("Event Handling", event_handling),
        ("File Dialogs", file_dialogs)
    ]
    
    for text, func in examples:
        btn = ttk.Button(root, text=text, command=func, width=20)
        btn.pack(pady=5)
    
    # Quit button
    quit_btn = ttk.Button(root, text="Quit", command=root.destroy, width=20)
    quit_btn.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    main()