import os

# Tentukan path folder dataset Anda
folder_path = './DatasetHotel'

# Berjalan menelusuri semua folder dan sub-folder (dari terdalam ke terluar)
for root, dirs, files in os.walk(folder_path, topdown=False):
    
    # 1. Ubah nama file yang mengandung '&'
    for file_name in files:
        if '&' in file_name:
            # Mengganti '&' dengan kata 'dan'
            new_name = file_name.replace('&', 'dan') 
            old_file_path = os.path.join(root, file_name)
            new_file_path = os.path.join(root, new_name)
            
            os.rename(old_file_path, new_file_path)
            print(f"Sukses mengubah file: {file_name} -> {new_name}")

    # 2. Ubah nama folder (berjaga-jaga jika ada nama folder yang pakai '&')
    for dir_name in dirs:
        if '&' in dir_name:
            # Mengganti '&' dengan kata 'dan'
            new_name = dir_name.replace('&', 'dan')
            old_dir_path = os.path.join(root, dir_name)
            new_dir_path = os.path.join(root, new_name)
            
            os.rename(old_dir_path, new_dir_path)
            print(f"Sukses mengubah folder: {dir_name} -> {new_name}")

print("Proses pergantian nama dengan kata 'dan' selesai!")