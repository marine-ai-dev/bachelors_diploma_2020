"ПОДІЛ НА ТЕСТОВУ ТА НАВЧАЛЬНУ ВИБІРКИ 80% --- 20%"
import shutil
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # parameterized for portability (was a hardcoded Windows path)
path1=os.path.join(BASE_DIR, "..", "..", "data", "PlantVillage", "plantvillage-dataset", "segmented", "train")
path2=os.path.join(BASE_DIR, "..", "..", "data", "PlantVillage", "plantvillage-dataset", "segmented", "val")
percent=0.2 #процент зображень для тестової вибірки


all_folders = os.listdir(path1) #список всіх папок у директорії


for i in range(len(all_folders)): #проходимося по всім папкам
    os.mkdir(path2+"/"+all_folders[i]) #створюємо порожні папки для тестової вибірки із назвами, як у навчальній вибірці
    
    folder=os.listdir(path1+"/"+all_folders[i])
    size_of_folder=len(folder) #знаходимо розмір кожної папки із зображенням
    count_of_test_samples=int(size_of_folder*percent)
    for j in range(count_of_test_samples):
        src=path1+"/"+all_folders[i]+'/'+folder[j]
        dst=path2+"/"+all_folders[i]+'/'+folder[j]
        shutil.move(src, dst)
    
    
    
    