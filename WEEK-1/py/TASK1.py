import os # file or folder manage 
import shutil # file copy,delete, and view

folder = "."   # current my  folder name INTERSHIP/WEEK-1

for file in os.listdir(folder):
    path = os.path.join(folder, file)

    if os.path.isfile(path):
        ext = file.split(".")[-1]

        # folder name = extension (jpg, pdf, etc.   )
        new_folder = os.path.join(folder, ext)

        if not os.path.exists(new_folder):
            os.mkdir(new_folder)

        new_path = os.path.join(new_folder, file)

        # simple duplicate handling
        if os.path.exists(new_path):
            name, ext2 = os.path.splitext(file)
            new_path = os.path.join(new_folder, name + "_1" + ext2)

        shutil.move(path, new_path)

print("Done all files to move in accurate folder by extensions")