# To be able to run it, pywin32 must be installed
# To do that just paste in 'pip install pywin32' into the python terminal

import os
import zipfile
import shutil
import json
import pywintypes
import win32file
import win32con
from datetime import datetime
from tkinter import filedialog, messagebox, Tk

def consolidate_files(src_folder, dest_folder):
    """
    Move all files from src_folder (including its subfolders) into dest_folder.
    """
    for root, _, files in os.walk(src_folder):
        for file in files:
            source_path = os.path.join(root, file)
            destination_path = os.path.join(dest_folder, file)

            # Handle duplicate filenames by appending a counter
            base, ext = os.path.splitext(file)
            counter = 1
            while os.path.exists(destination_path):
                destination_path = os.path.join(dest_folder, f"{base}_{counter}{ext}")
                counter += 1

            shutil.move(source_path, destination_path)

    # Remove empty folders after files are moved
    for root, dirs, _ in os.walk(src_folder, topdown=False):
        for dir in dirs:
            folder_path = os.path.join(root, dir)
            try:
                os.rmdir(folder_path)
            except OSError:
                pass  # Skip if the folder is not empty or cannot be removed

def unix_time_to_pywintypes(unix_time):
    """
    Convert UNIX timestamps to pywintypes time objects.
    """
    return pywintypes.Time(datetime.utcfromtimestamp(unix_time))

def process_files(metadata_only_folder, combined_files_folder, no_metadata_folder):
    """
    Process files from the metadata_only folder and update metadata timestamps.
    """
    # Ensure the output directories exist
    os.makedirs(combined_files_folder, exist_ok=True)
    os.makedirs(no_metadata_folder, exist_ok=True)

    # Map JSON metadata files to their corresponding image files
    json_files = {
        file.lower(): file for file in os.listdir(metadata_only_folder) if file.endswith(".json")
    }

    # Iterate over all files in the metadata_only folder
    for file_name in os.listdir(metadata_only_folder):
        # Skip JSON files during processing
        if file_name.endswith(".json"):
            continue

        # Look for a JSON metadata file with the exact format: imagename.extension.json
        json_file_name = f"{file_name}.json".lower()
        json_file = json_files.get(json_file_name)

        if json_file:
            # If metadata exists, process the file
            json_path = os.path.join(metadata_only_folder, json_file)
            image_path = os.path.join(metadata_only_folder, file_name)

            # Read the JSON file
            with open(json_path, 'r') as file:
                metadata = json.load(file)

            # Extract timestamps from metadata
            photo_taken_timestamp = int(metadata["photoTakenTime"]["timestamp"])
            creation_timestamp = int(metadata["creationTime"]["timestamp"])

            # Convert timestamps to pywintypes
            created_time = unix_time_to_pywintypes(creation_timestamp)
            modified_time = unix_time_to_pywintypes(photo_taken_timestamp)

            # Copy the file to the combined_files folder
            output_path = os.path.join(combined_files_folder, file_name)
            shutil.copy2(image_path, output_path)

            # Update timestamps
            handle = win32file.CreateFile(
                output_path,
                win32con.GENERIC_WRITE,
                win32con.FILE_SHARE_WRITE,
                None,
                win32con.OPEN_EXISTING,
                win32con.FILE_ATTRIBUTE_NORMAL,
                None
            )
            win32file.SetFileTime(handle, created_time, created_time, modified_time)
            handle.close()

            print(f"Updated timestamps for {file_name}")
            # Remove processed file and metadata
            os.remove(image_path)
        else:
            # If no metadata exists, move the file to the no_metadata folder
            file_path = os.path.join(metadata_only_folder, file_name)
            output_path = os.path.join(no_metadata_folder, file_name)
            shutil.move(file_path, output_path)
            print(f"Moved {file_name} to no_metadata folder.")

def main():
    # Set up the root Tkinter window (hidden)
    root = Tk()
    root.withdraw()

    # Step 1: Ask user to select ZIP files
    file_selection = filedialog.askopenfilenames(
        title="Select ZIP Files to Process",
        filetypes=[("ZIP files", "*.zip")]
    )
    if not file_selection:
        messagebox.showerror("Error", "No ZIP files selected.")
        return

    # Step 2: Ask user to select the destination folder
    destination_folder = filedialog.askdirectory(title="Select Destination Folder")
    if not destination_folder:
        messagebox.showerror("Error", "No destination folder selected.")
        return

    # Step 3: Create subfolders in the destination folder
    metadata_only_folder = os.path.join(destination_folder, "metadata_only")
    combined_files_folder = os.path.join(destination_folder, "combined_files")
    no_metadata_folder = os.path.join(destination_folder, "no_metadata")

    os.makedirs(metadata_only_folder, exist_ok=True)
    os.makedirs(combined_files_folder, exist_ok=True)
    os.makedirs(no_metadata_folder, exist_ok=True)

    # Step 4: Extract all selected ZIP files into the "metadata_only" subfolder
    for file_path in file_selection:
        if file_path.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(metadata_only_folder)

    # Step 5: Consolidate all extracted files into the "metadata_only" subfolder (redundant in this case)
    consolidate_files(metadata_only_folder, metadata_only_folder)

    # Step 6: Process files in the "metadata_only" folder and output to appropriate folders
    process_files(metadata_only_folder, combined_files_folder, no_metadata_folder)

    # Final Message
    messagebox.showinfo("Success", "Files processed successfully. Check the subfolders in your destination folder.")

if __name__ == "__main__":
    main()
