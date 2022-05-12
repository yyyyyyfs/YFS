import json
import os
from collections import Counter
from unicodedata import name
import matplotlib.pyplot as plt



file_path = os.path.join('data','Analyse_data','1号_coco','training','data2coco_all.json')

#读出目标json文件的信息
def open_file(file_path):
    area = []
    category = []
    categories = ['person','head','helmet','clothes','uniform','helmet_unknown','uniform_unknown']
    num_per_category = [0 for j in range(len(categories))]
    #打开json文件
    with open(file_path,'r') as f:
        data = json.load(f)
        #读出所有的框的面积信息
        for i in data['annotations']:
            area.append(i['area'])
            area.sort()#决定是否排序
            #####用Counter方法
            # category.append(i['category_id'])#将category_id都取到category列表中
            # num_per_category = Counter(category)#计算每一个category_id出现的次数，返回一个Counter字典
            # num_per_category = dict(num_per_category)#转换成普通字典
            # #然后遍历字典，读取所有category出现的次数
            
        #得到所有的category_id，然后统计每一个类别id出现的次数，即每一个类的数量，然后返回
            category = i['category_id'] #得到所有的category_id
            num_per_category[category-1] +=1 #统计每个category_id出现的次数
        return area, num_per_category
    #统计框的面积分布
def data_statistical(area):
    tiny_area = 0
    medium_area = 0
    large_area = 0
    for i in area:
        if i < 0 :
            print('area_error')
        elif i <= 100000:
            tiny_area +=1
        elif i > 100000 and i <= 300000:
            medium_area +=1
        elif i >300000:
            large_area +=1
    return tiny_area, medium_area, large_area

def data_plot(area,num_per_category):
    #区分小框、中框、大框面积的数量
    fig1 = plt.figure()#创建图形对象
    tiny_area,medium_area,large_area = data_statistical(area)
    name  = ['tiny_area','medium_area','large_area']
    num1 = [tiny_area,medium_area,large_area]
    plt.bar(name,num1)
    print(num1)
    plt.savefig('/home/guest/data_Deal/data_sta_plot/fihure1')
    #画出每一类的个数
    fig2 = plt.figure()
    catgories = ['person','head','helmet','clothes','uniform','helmet_unknown','uniform_unknown'] 
    num2 = [i for i in num_per_category ]
    plt.bar(catgories,num2)
    plt.savefig('/home/guest/data_Deal/data_sta_plot/figure2')
    print(num2)
area, num_per_category= open_file(file_path)
plot = data_plot(area,num_per_category)

# area_distribution = data_statistical(area)


