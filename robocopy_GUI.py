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
        elif source_folder == destination_folder:
            tk.messagebox.showwarning("Warning", "Source and destination folders cannot be the same.")
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
    if hard_copy_var.get()== 1:
        start_robocopy()

    if restore_point_var.get() == 1:
        subprocess.run(["powershell", "-Command", "Checkpoint-Computer -Description 'Restore Point by Python Prgram' -RestorePointType 'MODIFY_SETTINGS'"], check=True)

# Create the main window
window = tk.Tk() # Create the main window
window.title("An Easy Backup Program") # Change the title of the GUI
window.iconbitmap('D:\Projects\Github\Repos\Backup_Prgramm\icon.ico') # Change the icon of the GUI
window.resizable(0, 0)  # Disable resizing the GUI window

# Create a frame for the robocopy feature
robocopy_frame = tk.Frame(window, bd=2, relief=tk.GROOVE)
robocopy_frame.grid(row=1, column=0, columnspan=7, sticky="ew")

# Create a check button for enabling the robocopy feature
hard_copy_var = tk.IntVar()
hard_copy_var.set(1)  # Set the initial value to 1
hard_copy_checkbox = tk.Checkbutton(robocopy_frame, text="Hard Copy", variable=hard_copy_var)
hard_copy_checkbox.grid(row=0, column=0, sticky="w")


# source folder selection
source_label = tk.Label(robocopy_frame, text="Source Folder:")
source_label.grid(row=1, column=0, sticky="e")
source_entry = tk.Entry(robocopy_frame)
source_entry.grid(row=1, column=1)
source_button = tk.Button(robocopy_frame, text="Select Folder", command=select_source_folder)
source_button.grid(row=1, column=2)

# destination folder selection
destination_label = tk.Label(robocopy_frame, text="Destination Folder:")
destination_label.grid(row=1, column=3, sticky="e")
destination_entry = tk.Entry(robocopy_frame)
destination_entry.grid(row=1, column=4)
destination_button = tk.Button(robocopy_frame, text="Select Folder", command=select_destination_folder)
destination_button.grid(row=1, column=5)

folder_list = tk.Listbox(robocopy_frame)
folder_list.grid(row=3, columnspan=7, sticky="ew")  # Set sticky="ew" to make the list wider
folder_list.configure(height=len(source_folders)) # Configure the listbox to adjust its height based on the number of entries

# remove folder from backup button
remove_button = tk.Button(robocopy_frame, text="Remove", command=remove_folder_from_backup)
remove_button.grid(row=3, column=7)

# add folder to backup button
add_button = tk.Button(robocopy_frame, text="Add Folder-Pair to Backup", command=add_folder_to_backup)
add_button.grid(row=2, column=2, columnspan=3)

# start button
start_button = tk.Button(window, text="Start Backup", command=start_backup, fg="red")
start_button.grid(row=5, column=2, columnspan=3)

# Create a function to change the font color of the robocopy frame based on the value of the check button
def apply_font_color():
    if hard_copy_var.get() == 0:
        robocopy_frame.configure(highlightbackground="red", highlightthickness=1)
    else:
        robocopy_frame.configure(highlightbackground="green", highlightthickness=1)

apply_font_color() # Call the function to apply the initial font color

hard_copy_var.trace("w", lambda *args: apply_font_color()) # Apply the function whenever the check button is clicked


################### GUI for Windows Restore Point ###################

# Create a frame for the Windows Restore Point feature
restore_point_frame = tk.Frame(window, bd=2, relief=tk.GROOVE)
restore_point_frame.grid(row=3, column=0, columnspan=7, sticky="ew")

# Create a check button for enabling the Windows Restore Point feature
restore_point_var = tk.IntVar()
restore_point_var.set(0)  # Set the initial value to 0
restore_point_checkbox = tk.Checkbutton(restore_point_frame, text="Windows Restore Point", variable=restore_point_var)
restore_point_checkbox.grid(row=0, column=0, sticky="w")

start_button.grid(row=5, column=2, columnspan=3) # Move the start button to row 4

# Create a function to change the color of the restore point frame based on the value of the check button
def apply_restore_point_color():
    if restore_point_var.get() == 0:
        restore_point_frame.configure(highlightbackground="red", highlightthickness=1)
    else:
        restore_point_frame.configure(highlightbackground="green", highlightthickness=1)
apply_restore_point_color()  # Call the function to apply the initial color
restore_point_var.trace("w", lambda *args: apply_restore_point_color())  # Apply the function whenever the check button is clicked


################### General GUI Design ###################

#insert space between the two frames
empty_label = tk.Label(window)
empty_label.grid(row=0)

empty_label = tk.Label(window)
empty_label.grid(row=2)

empty_label = tk.Label(window)
empty_label.grid(row=4)

empty_label = tk.Label(window)
empty_label.grid(row=6)

robocopy_frame.grid(row=1, column=0, columnspan=7, sticky="ew", padx=10) # Add some horizontal padding to the robocopy frame
restore_point_frame.grid(row=3, column=0, columnspan=7, sticky="ew", padx=10) # Add some horizontal padding to the restore point frame

# Start the GUI event loop
window.mainloop()