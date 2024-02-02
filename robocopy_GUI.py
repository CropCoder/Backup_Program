import tkinter as tk
from tkinter import filedialog
import subprocess
import string
import os

program_folder = os.path.dirname(os.path.abspath(__file__))

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
        return True # Return True to indicate that there was a warning
    
    # Check if there are any path-pairs in the source_folders and destination_folders lists
    if not source_folders or not destination_folders:
        tk.messagebox.showwarning("Warning", "Please add at least one folder pair to backup before starting the backup.")
        return True # Return True to indicate that there was a warning

    robocopy_flags = ['/MIR']  # add flags here
    robocopy_flags.extend(flags.split())
    
    for i, (source, destination) in enumerate(zip(source_folders, destination_folders)):
        subprocess.run(['robocopy', source, destination, *robocopy_flags])


################### back up main function ###################
def start_backup():
    if hard_copy_var.get()== 1:
        if start_robocopy():
            return # Return the start_backup-function if there was a warning from the start_robocopy-function

    if restore_point_var.get() == 1:
        subprocess.run(["powershell", "-Command", "Checkpoint-Computer -Description 'Restore Point by Python Prgram' -RestorePointType 'MODIFY_SETTINGS'"], check=True)

    if choco_update_var.get() == 1:
        subprocess.run(["powershell", "-Command", "choco upgrade all -y"], check=True)

    if windows_image_var.get() == 1:
        create_windows_image()

    if update_windows_var.get() == 1:
        subprocess.run(["powershell", "-Command", "Update-MpSignature"], check=True)
        ##subprocess.run(["powershell", "-Command", "Import-Module PSWindowsUpdate"], check=True)
        ##subprocess.run(["powershell", "-Command", "Get-WindowsUpdate -Install -AcceptAll -IgnoreReboot"], check=True)

    if defender_scan_var.get() == 1:
        print("Scanning for viruses. Please wait...")
        subprocess.run(["powershell", "-Command", "Start-MpScan -ScanType FullScan"], check=True)
        
        # C:\Program Files\Windows Defender\MpCmdRun.exe" -Scan -Cancel

    perform_shutdown()
    

# Create the main window
window = tk.Tk() # Create the main window
window.title("An Easy Backup Program") # Change the title of the GUI
icon_path = os.path.join(program_folder, 'icon.ico') # Set the path to the icon file
window.iconbitmap(icon_path)  # Change the icon of the GUI
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
add_button = tk.Button(robocopy_frame, text="+", fg="green", font=("Arial", 17, "bold"), command=add_folder_to_backup)
add_button.grid(row=2, column=3, columnspan=1)

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

# Create a function to change the color of the restore point frame based on the value of the check button
def apply_restore_point_color():
    if restore_point_var.get() == 0:
        restore_point_frame.configure(highlightbackground="red", highlightthickness=1)
    else:
        restore_point_frame.configure(highlightbackground="green", highlightthickness=1)
apply_restore_point_color()  # Call the function to apply the initial color
restore_point_var.trace("w", lambda *args: apply_restore_point_color())  # Apply the function whenever the check button is clicked


################ GUI for Choco Update All ################

# Create a frame for the Choco Update All feature
choco_update_frame = tk.Frame(window, bd=2, relief=tk.GROOVE)
choco_update_frame.grid(row=5, column=0, columnspan=7, sticky="ew", padx=10)

# Create a check button for enabling the Choco Update All feature
choco_update_var = tk.IntVar()
choco_update_var.set(0)  # Set the initial value to 0
choco_update_checkbox = tk.Checkbutton(choco_update_frame, text="Choco Update All", variable=choco_update_var)
choco_update_checkbox.grid(row=0, column=0, sticky="w")

# Create a function to change the color of the choco update frame based on the value of the check button
def apply_choco_update_color():
    if choco_update_var.get() == 0:
        choco_update_frame.configure(highlightbackground="red", highlightthickness=1)
    else:
        choco_update_frame.configure(highlightbackground="green", highlightthickness=1)

apply_choco_update_color()  # Call the function to apply the initial color
choco_update_var.trace("w", lambda *args: apply_choco_update_color())  # Apply the function whenever the check button is clicked


##################### GUI for Windows Image #####################

# Create a frame for the Windows Image feature
windows_image_frame = tk.Frame(window, bd=2, relief=tk.GROOVE)
windows_image_frame.grid(row=7, column=0, columnspan=7, sticky="ew", padx=10)

# Create a label for the source column
source_label = tk.Label(windows_image_frame, text="Source Drives")
source_label.grid(row=1, column=0, sticky="w")

# Create a label for the destination column
destination_label = tk.Label(windows_image_frame, text="Destination Drive")
destination_label.grid(row=1, column=1, sticky="w")

# Create a dictionary to store the IntVar instances and the corresponding drive letters
source_drive_vars = {}
destination_drive_var = tk.StringVar(value="")  # Initialize to an empty string

# Create a function to disable the checkbox for the destination drive in the source column
def disable_source_drive(drive):
    for source_drive, source_var in source_drive_vars.items():
        if source_drive == drive:
            source_var.set(0)
            source_drive_vars[source_drive].set(0)

# Create a check button for each available drive letter in the source column and a radio button in the destination column
for i, letter in enumerate(string.ascii_uppercase, start=2):
    drive = f"{letter}:\\"
    if os.path.exists(drive):
        source_var = tk.IntVar()
        source_var.set(0)  # Set the initial value to 0
        source_checkbox = tk.Checkbutton(windows_image_frame, text=drive, variable=source_var)
        source_checkbox.grid(row=i, column=0, sticky="w")
        source_drive_vars[drive] = source_var  # Store the IntVar instance and the drive letter in the dictionary

        destination_radiobutton = tk.Radiobutton(windows_image_frame, text=drive, value=drive, variable=destination_drive_var, command=lambda drive=drive: disable_source_drive(drive))
        destination_radiobutton.grid(row=i, column=1, sticky="w")


# Create a check button for enabling the Windows Image feature
windows_image_var = tk.IntVar()
windows_image_var.set(0)  # Set the initial value to 0
windows_image_checkbox = tk.Checkbutton(windows_image_frame, text="Windows Image", variable=windows_image_var)
windows_image_checkbox.grid(row=0, column=0, sticky="w")

# Create a function to change the color of the windows image frame based on the value of the check button
def apply_windows_image_color():
    if windows_image_var.get() == 0:
        windows_image_frame.configure(highlightbackground="red", highlightthickness=1)
    else:
        windows_image_frame.configure(highlightbackground="green", highlightthickness=1)

apply_windows_image_color()  # Call the function to apply the initial color
windows_image_var.trace("w", lambda *args: apply_windows_image_color())  # Apply the function whenever the check button is clicked

# Create a dictionary to store the IntVar instances and the corresponding drive letters
drive_vars = {}

# Create a function to create a Windows image
def create_windows_image():
    if windows_image_var.get() == 1:
        for drive, var in drive_vars.items():
            if var.get() == 1:
                # Replace 'destination' with the destination for the Windows image
                subprocess.run(["wbAdmin", "start", "backup", "-backupTarget:\\destination", "-include:" + drive, "-allCritical", "-quiet"], check=True)


################### GUI for Update Windows ###################

# Create a frame for the Update Windows feature
update_windows_frame = tk.Frame(window, bd=2, relief=tk.GROOVE)
update_windows_frame.grid(row=9, column=0, columnspan=7, sticky="ew", padx=10)

# Create a check button for enabling the Update Windows feature
update_windows_var = tk.IntVar()
update_windows_var.set(0)  # Set the initial value to 0
update_windows_checkbox = tk.Checkbutton(update_windows_frame, text="Update Windows and Windows Defender", variable=update_windows_var)
update_windows_checkbox.grid(row=0, column=0, sticky="w")

# Create a function to change the color of the update windows frame based on the value of the check button
def apply_update_windows_color():
    if update_windows_var.get() == 0:
        update_windows_frame.configure(highlightbackground="red", highlightthickness=1)
    else:
        update_windows_frame.configure(highlightbackground="green", highlightthickness=1)

apply_update_windows_color()  # Call the function to apply the initial color
update_windows_var.trace("w", lambda *args: apply_update_windows_color())  # Apply the function whenever the check button is clicked


################### GUI for Full Windows Defender Scan ###################

# Create a frame for the Update Windows feature
defender_scan_frame = tk.Frame(window, bd=2, relief=tk.GROOVE)
defender_scan_frame.grid(row=11, column=0, columnspan=7, sticky="ew", padx=10)

# Create a check button for enabling the Update Windows feature
defender_scan_var = tk.IntVar()
defender_scan_var.set(0)  # Set the initial value to 0
defender_scan_checkbox = tk.Checkbutton(defender_scan_frame, text="Full Windows Defender Scan", variable=defender_scan_var)
defender_scan_checkbox.grid(row=0, column=0, sticky="w")

# Create a function to change the color of the update windows frame based on the value of the check button
def apply_defender_scan_color():
    if defender_scan_var.get() == 0:
        defender_scan_frame.configure(highlightbackground="red", highlightthickness=1)
    else:
        defender_scan_frame.configure(highlightbackground="green", highlightthickness=1)

apply_defender_scan_color()  # Call the function to apply the initial color
defender_scan_var.trace("w", lambda *args: apply_defender_scan_color())  # Apply the function whenever the check button is clicked

################### GUI for what to do after the backup ###################
# Create a frame for the "What to do after backup" feature
shutdown_frame = tk.Frame(window, bd=2, relief=tk.GROOVE)
shutdown_frame.grid(row=13, column=0, columnspan=7, sticky="ew", padx=10)
shutdown_label = tk.Label(shutdown_frame, text="What to do after backup")
shutdown_label.grid(row=0, column=0, sticky="w")

# Create radio buttons for "Nothing (default)", "Restart (recommended)", "Shutdown", and "Lock"
shutdown_option = tk.StringVar()
shutdown_option.set("Nothing (default)")

nothing_radio = tk.Radiobutton(shutdown_frame, text="Nothing (default)", variable=shutdown_option, value="Nothing (default)")
nothing_radio.grid(row=1, column=0, sticky="w")

restart_radio = tk.Radiobutton(shutdown_frame, text="Restart (recommended)", variable=shutdown_option, value="Restart (recommended)")
restart_radio.grid(row=2, column=0, sticky="w")

shutdown_radio = tk.Radiobutton(shutdown_frame, text="Shutdown", variable=shutdown_option, value="Shutdown")
shutdown_radio.grid(row=3, column=0, sticky="w")

lock_radio = tk.Radiobutton(shutdown_frame, text="Lock", variable=shutdown_option, value="Lock")
lock_radio.grid(row=4, column=0, sticky="w")


def perform_shutdown(): # The function checks the value of the `shutdown_option` variable and performs the corresponding action.
    selected_option = shutdown_option.get()

    if selected_option == "Nothing (default)":
        pass  # Do nothing

    elif selected_option == "Restart (recommended)":
        subprocess.run(["shutdown", "/r", "/t", "0"], shell=True)  # Restart the system

    elif selected_option == "Shutdown":
        subprocess.run(["shutdown", "/s", "/t", "0"], shell=True)  # Shutdown the system
        
    elif selected_option == "Lock":
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], shell=True)  # Lock the system

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

empty_label = tk.Label(window)
empty_label.grid(row=8)

empty_label = tk.Label(window)
empty_label.grid(row=10)

empty_label = tk.Label(window)
empty_label.grid(row=12)

empty_label = tk.Label(window)
empty_label.grid(row=14)

empty_label = tk.Label(window)
empty_label.grid(row=99)

robocopy_frame.grid(row=1, column=0, columnspan=7, sticky="ew", padx=10) # Add some horizontal padding to the robocopy frame
restore_point_frame.grid(row=3, column=0, columnspan=7, sticky="ew", padx=10) # Add some horizontal padding to the restore point frame

# start button
start_button = tk.Button(window, text="Start Backup", command=start_backup, fg="red")
start_button.grid(row=15, column=2, columnspan=3)

# Start the GUI event loop
window.mainloop()