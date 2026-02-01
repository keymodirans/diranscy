"""
Test UI Debug untuk melihat apa yang terjadi dengan CustomTkinter.
"""

import customtkinter as ctk
import tkinter as tk

print("=" * 50)
print("TEST UI DEBUG")
print("=" * 50)

# Test 1: Simple CustomTkinter window
print("\n[1] Testing simple CustomTkinter window...")
try:
    app = ctk.CTk()
    app.title("Test 1 - Simple CTK")
    app.geometry("400x300")

    label = ctk.CTkLabel(app, text="Hello from CustomTkinter!")
    label.pack(pady=50)

    print("   Window created successfully")
    print("   Close the window to continue...")
    app.mainloop()
    print("   Window closed")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 2: CustomTkinter with Entry and Button
print("\n[2] Testing CustomTkinter with Entry and Button...")
try:
    app2 = ctk.CTk()
    app2.title("Test 2 - Entry & Button")
    app2.geometry("600x200")

    # Input frame
    input_frame = ctk.CTkFrame(app2)
    input_frame.pack(pady=20, padx=20, fill="x")

    label = ctk.CTkLabel(input_frame, text="Keyword:")
    label.pack(side="left", padx=10)

    entry_var = tk.StringVar(value="test")
    entry = ctk.CTkEntry(input_frame, textvariable=entry_var, width=300)
    entry.pack(side="left", padx=10)

    button = ctk.CTkButton(input_frame, text="Submit", width=100)
    button.pack(side="left", padx=10)

    print("   Window with Entry and Button created")
    print("   Close the window to continue...")
    app2.mainloop()
    print("   Window closed")
except Exception as e:
    print(f"   ERROR: {e}")

print("\n" + "=" * 50)
print("TEST SELESAI")
print("=" * 50)
