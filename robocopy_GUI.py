import tkinter as tk
from tkinter import filedialog
import subprocess

source_folders = []
destination_folders = []

def select_source_folder():
    source_folder = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, source_folder)

def select_destination_folder():
    destination_folder = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, destination_folder)

def add_folder_to_backup():
    source_folder = source_entry.get()
    destination_folder = destination_entry.get()
    
    if source_folder and destination_folder:
        if (source_folder, destination_folder) in zip(source_folders, destination_folders):
            tk.messagebox.showwarning("Warning", "This path-pair has already been entered.")
        else:
            source_folders.append(source_folder)
            destination_folders.append(destination_folder)
            folder_list.insert(tk.END, f"Source: {source_folder} --> Destination: {destination_folder}")
            source_entry.delete(0, tk.END)
            destination_entry.delete(0, tk.END)
    else:
        tk.messagebox.showwarning("Warning", "Please select both source and destination folders.")

def remove_folder_from_backup():
    selected_index = folder_list.curselection()
    if selected_index:
        selected_index = int(selected_index[0])
        source_folders.pop(selected_index)
        destination_folders.pop(selected_index)
        folder_list.delete(selected_index)

def start_robocopy(flags=''):

    # Check if there are any entries in the source and destination entry boxes
    if source_entry.get() or destination_entry.get():
        tk.messagebox.showwarning("Warning", "Please add all folder pairs to backup before starting the backup.")
        return
    
    # Check if there are any path-pairs in the source_folders and destination_folders lists
    if not source_folders or not destination_folders:
        tk.messagebox.showwarning("Warning", "Please add at least one folder pair to backup before starting the backup.")
        return

    robocopy_flags = ['/MIR']  # add flags here
    robocopy_flags.extend(flags.split())
    
    for i, (source, destination) in enumerate(zip(source_folders, destination_folders)):
        subprocess.run(['robocopy', source, destination, *robocopy_flags])

def start_backup():
    start_robocopy()

# Create the main window
window = tk.Tk()
window.title("Robocopy GUI")

# source folder selection
source_label = tk.Label(window, text="Source Folder:")
source_label.grid(row=0, column=0, sticky="e")
source_entry = tk.Entry(window)
source_entry.grid(row=0, column=1)
source_button = tk.Button(window, text="Select Folder", command=select_source_folder)
source_button.grid(row=0, column=2)

# destination folder selection
destination_label = tk.Label(window, text="Destination Folder:")
destination_label.grid(row=0, column=4, sticky="e")
destination_entry = tk.Entry(window)
destination_entry.grid(row=0, column=5)
destination_button = tk.Button(window, text="Select Folder", command=select_destination_folder)
destination_button.grid(row=0, column=6)

folder_list = tk.Listbox(window)
folder_list.grid(row=3, columnspan=7, sticky="ew")  # Set sticky="ew" to make the list wider
folder_list.configure(height=len(source_folders)) # Configure the listbox to adjust its height based on the number of entries

# remove folder from backup button
remove_button = tk.Button(window, text="Remove", command=remove_folder_from_backup)
remove_button.grid(row=3, column=7)

# add folder to backup button
add_button = tk.Button(window, text="Add Folder-Pair to Backup", command=add_folder_to_backup)
add_button.grid(row=2, column=2, columnspan=3)

# start button
start_button = tk.Button(window, text="Start Backup", command=start_backup, fg="red")
start_button.grid(row=4, column=2, columnspan=3)

# Start the GUI event loop
window.mainloop()
