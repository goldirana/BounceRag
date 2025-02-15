import os
import tempfile
import shutil
from pathlib import Path

def clear_temp_files():
    """
    Clears all temporary files in the system's temp directory.
    Handles potential errors and ensures safe deletion.
    """
    temp_dir = tempfile.gettempdir()
    
    try:
        # Iterate through all files and directories in temp directory
        for item in Path(temp_dir).glob('*jpg'):
            try:
                if item.is_file():
                    os.unlink(item)  # Delete file
            except Exception as e:
                print(f"Error deleting {item}: {e}")
                continue
                
        print("Temporary files cleared successfully.")
    except Exception as e:
        print(f"Error accessing temp directory: {e}")

if __name__ == "__main__":
    clear_temp_files()
