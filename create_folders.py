import os

main_folder = "imgs-ex"
main_path = os.path.join(os.getcwd(), main_folder)


if not os.path.exists(main_path):
    os.mkdir(main_path)
    print(f"Pasta {main_folder} criada com sucesso!")
    
subfolders = ["inputs", "labels", "tiffs"]

for subfolder in subfolders:
    subfolder_path = os.path.join(main_path, subfolder)
    if not os.path.exists(subfolder_path):
        os.mkdir(subfolder_path)
        print(f"Pasta {subfolder} criada com sucesso!")
    else:
        print(f"Pasta {subfolder} já existe!")