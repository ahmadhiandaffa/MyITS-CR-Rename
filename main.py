import os
import sys
import csv
import tkinter.filedialog
import shutil
import tkinter.messagebox
from rarfile import RarFile

# Set correct path for WinRAR
if not shutil.which("unrar.exe"):
    winrarpath = os.path.join(os.environ.get("ProgramFiles",""),"WinRAR")
    unrarpath  = os.path.join(winrarpath,"UnRAR.exe")
    if os.path.isdir(winrarpath) and os.path.exists(unrarpath):
        os.environ['PATH'] = os.environ.get('PATH','') + os.pathsep + winrarpath
    else:
        tkinter.messagebox.showerror(
            title="Error", 
            message="WinRAR belum terinstal. Download dan install WinRAR " + 
                    "https://www.win-rar.com/download.html?&L=0")
        sys.exit()

# Show message dialog for choosing files
submission_file = tkinter.filedialog.askopenfilename(title="Pilih file submission (.zip)")
if submission_file == "":
    sys.exit()
grader_file     = tkinter.filedialog.askopenfilename(title="Pilih file grader (.csv)")
if grader_file == "":
    sys.exit()
extract_dir     = tkinter.filedialog.askdirectory(title="Pilih folder untuk extract")
if extract_dir == "":
    sys.exit()

# Make sure the extract folder is empty to prevent modifying existing file 
if os.listdir(extract_dir):
    extract_dir = os.path.join(extract_dir, "Extract")

# Unzip submission file
shutil.unpack_archive(submission_file, extract_dir)

# Remove unnecessary folder name part
folders = os.listdir(extract_dir)
for folder in folders:
    old_name = folder
    old_path = os.path.join(extract_dir, old_name)
    new_name = folder.split("_")[0]
    new_path = os.path.join(extract_dir, new_name)
    os.rename(old_path, new_path)

# Read grader file
with open(grader_file) as fp:
    reader = csv.reader(fp, delimiter=",") 
    header = next(reader, None)  # skip the headers
    if len(header) == 1: # Wrong delimiter
        reader = csv.reader(fp, delimiter=";")
    student_list = [row for row in reader]

# Add NRP & grader to folder name
for student in student_list:
    nrp, name, kelas, grader = student

    old_name = name
    old_path = os.path.join(extract_dir, old_name)
    new_name = kelas + "_" + grader + "_" + nrp[-3:] + "_" + name 
    new_path = os.path.join(extract_dir, new_name)
    if os.path.exists(old_path):
        os.rename(old_path, new_path)

# Extract file in each folder
folders = os.listdir(extract_dir)
fail_list = []
for folder in folders:
    folder_path = os.path.join(extract_dir, folder)
    files = os.listdir(folder_path)
    for file in files:
        file_path = os.path.join(folder_path, file)
        _, extension = os.path.splitext(file)
        if extension == ".zip":
            shutil.unpack_archive(file_path, format="zip", extract_dir=folder_path)
            os.remove(file_path)
        elif extension == ".rar":
            try:
                RarFile(file_path).extractall(path=folder_path)
                os.remove(file_path)
            except:
                fail_list.append(file)
                continue

fail_list = ", ".join(fail_list)

tkinter.messagebox.showwarning(title="Warning", message=f"File {fail_list} gagal untuk diextract secara otomatis oleh program")
tkinter.messagebox.showinfo(title="Success", message="Proses extract dan rename berhasil dilakukan")