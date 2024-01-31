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
    source_folders.append(source_folder)
    destination_folders.append(destination_folder)
    source_entry.delete(0, tk.END)
    destination_entry.delete(0, tk.END)

def start_robocopy(flags=''):
    robocopy_flags = ['/MIR']  # add flags here
    robocopy_flags.extend(flags.split())
    
    for i in range(len(source_folders)):
        source = source_folders[i]
        destination = destination_folders[i]
        subprocess.run(['robocopy', source, destination, *robocopy_flags])

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
folder_list.grid(row=2, columnspan=7, sticky="ew")  # Set sticky="ew" to make the list wider
folder_list.configure(height=len(source_folders)) # Configure the listbox to adjust its height based on the number of entries

def add_folder_to_backup():
    source_folder = source_entry.get()
    destination_folder = destination_entry.get()
    source_folders.append(source_folder)
    destination_folders.append(destination_folder)
    folder_list.insert(tk.END, f"Source: {source_folder} --> Destination: {destination_folder}")
    source_entry.delete(0, tk.END)
    destination_entry.delete(0, tk.END)

# arrow
arrow_label = tk.Label(window, text="  -->  ")
arrow_label.grid(row=0, column=3, rowspan=2)

# add folder to backup button
add_button = tk.Button(window, text="Add Another Folder to Backup", command=add_folder_to_backup)
add_button.grid(row=1, columnspan=4)

# start button
start_button = tk.Button(window, text="Start Backup", command=start_robocopy)
start_button.grid(row=3, columnspan=4)

# Start the GUI event loop
window.mainloop()
