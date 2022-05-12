import os
import shutil

file_dir = '/home/guest/data/Analyse_data/1号阀室平台'
file_list = os.listdir(file_dir)
# print(file_list)


for image in file_list:
    
    
    if image[-3:] == 'jpg':

        if os.path.exists(os.path.join('/home/guest/data/Analyse_data/1号_coco/training','images')):
            shutil.copy(os.path.join(file_dir,image),os.path.join('/home/guest/data/Analyse_data/1号_coco/training','images'))
        else:
            os.mkdir(os.path.join('/home/guest/data/Analyse_data/1号_coco/training','images'))
            shutil.copy(os.path.join(file_dir,image),os.path.join('/home/guest/data/Analyse_data/1号_coco/training','images'))