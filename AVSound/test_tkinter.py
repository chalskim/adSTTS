#!/usr/bin/env python3
"""
Simple Tkinter test script to check if Tkinter is working
"""

try:
    import tkinter as tk
    from tkinter import ttk
    
    def main():
        root = tk.Tk()
        root.title("Tkinter Test")
        root.geometry("300x200")
        
        label = ttk.Label(root, text="Tkinter is working!", font=("Arial", 16))
        label.pack(expand=True)
        
        button = ttk.Button(root, text="Close", command=root.destroy)
        button.pack(pady=10)
        
        root.mainloop()
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"Failed to import tkinter: {e}")
    print("Tkinter is not properly installed.")
    
except Exception as e:
    print(f"An error occurred: {e}")
    print("This might be a compatibility issue with your macOS version.")