import os
import subprocess
import shutil
import tkinter as tk
from tkinter import messagebox

def create_restore_point():
    subprocess.run(['wmic', 'shadowcopy', 'call', 'create'])

def run_choco_upgrade():
    subprocess.run(['choco', 'upgrade', 'all', '-y'])

def check_install_windows_backups():
    # Add your code here to check and install Windows backups
    pass

def make_windows_image():
    subprocess.run(['wbadmin', 'start', 'backup', '-allCritical', '-quiet'])

def delete_old_windows_images():
    subprocess.run(['wbadmin', 'delete', 'backup', '-keepVersions:5'])

def make_hard_file_copies():
    # Add your code here to make hard file copies
    pass

def check_disk_space(target_disk, required_space):
    total, used, free = shutil.disk_usage(target_disk)
    if free > required_space:
        return True
    else:
        return False

def run_windows_defender_scan():
    subprocess.run(['mpcmdrun', '-scan', '-scantype', '3'])

def perform_backup():
    # Get user-selected options from GUI settings
    restore_point_enabled = restore_point_var.get()
    choco_upgrade_enabled = choco_upgrade_var.get()
    windows_backups_enabled = windows_backups_var.get()
    windows_image_enabled = windows_image_var.get()
    hard_file_copies_enabled = hard_file_copies_var.get()
    defender_scan_enabled = defender_scan_var.get()

    # Perform backup tasks based on user-selected options
    if restore_point_enabled:
        create_restore_point()
    if choco_upgrade_enabled:
        run_choco_upgrade()
    if windows_backups_enabled:
        check_install_windows_backups()
    if windows_image_enabled:
        make_windows_image()
        delete_old_windows_images()
    if hard_file_copies_enabled:
        make_hard_file_copies()
    if defender_scan_enabled:
        if check_disk_space(target_disk, required_space):
            run_windows_defender_scan()
        else:
            messagebox.showwarning("Insufficient Disk Space", "Not enough space on the target disk to perform backup.")

# Create the GUI
window = tk.Tk()
window.title("Backup Program")
window.geometry("400x300")

# GUI settings
restore_point_var = tk.BooleanVar()
choco_upgrade_var = tk.BooleanVar()
windows_backups_var = tk.BooleanVar()
windows_image_var = tk.BooleanVar()
hard_file_copies_var = tk.BooleanVar()
defender_scan_var = tk.BooleanVar()

# GUI checkboxes
restore_point_checkbox = tk.Checkbutton(window, text="Create Windows Restore Point", variable=restore_point_var)
choco_upgrade_checkbox = tk.Checkbutton(window, text="Run 'choco upgrade all -y' command", variable=choco_upgrade_var)
windows_backups_checkbox = tk.Checkbutton(window, text="Check and Install Windows Backups", variable=windows_backups_var)
windows_image_checkbox = tk.Checkbutton(window, text="Make Windows Image and Delete Old Images", variable=windows_image_var)
hard_file_copies_checkbox = tk.Checkbutton(window, text="Make Hard File Copies", variable=hard_file_copies_var)
defender_scan_checkbox = tk.Checkbutton(window, text="Perform Full Windows Defender Scan", variable=defender_scan_var)

# GUI button
backup_button = tk.Button(window, text="Perform Backup", command=perform_backup)

# GUI layout
restore_point_checkbox.pack()
choco_upgrade_checkbox.pack()
windows_backups_checkbox.pack()
windows_image_checkbox.pack()
hard_file_copies_checkbox.pack()
defender_scan_checkbox.pack()
backup_button.pack()

# Start the GUI event loop
window.mainloop()
