import shutil
import os
import csv
import tkinter.filedialog
import patoolib

# Show message dialog for choosing files
submission_file = tkinter.filedialog.askopenfilename(title="Pilih file submission (.zip)")
grader_file     = tkinter.filedialog.askopenfilename(title="Pilih file grader")
extract_dir     = tkinter.filedialog.askdirectory(title="Pilih folder untuk extract")
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
    reader = csv.reader(fp)
    next(reader, None)  # skip the headers
    student_list = [row for row in reader]

# Add NRP & grader to folder name
for student in student_list:
    nrp, name, kelas, grader = student

    old_name = name
    old_path = os.path.join(extract_dir, old_name)
    new_name = kelas + "_" + grader + "_" + nrp[-3:] + "_" + name 
    new_path = os.path.join(extract_dir, new_name)
    os.rename(old_path, new_path)

# Extract file in each folder
folders = os.listdir(extract_dir)
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
            patoolib.extract_archive(file_path, program="unrarw64.exe" ,outdir=folder_path)
            os.remove(file_path)