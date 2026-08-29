import torch
from torchvision import datasets, models, transforms
from PIL import Image
import os
import torch.nn.functional as nnf

'''----------------- PATH TO THE TESTING IMAGE ---------------- '''
list_of_classes="../datasets/PlantVillage/plantvillage-dataset/segmented"


#ТЕСТУВАННЯ-1 - СЕГМЕНТОВАНА ВИБІРКА

data_dir = "../datasets/PlantVillage/plantvillage-dataset/segmented"
type_of_data="train"
image_folder="Tomato___healthy"
image_name="3a1c6737-c9ff-44dc-9014-954753732160___GH_HL Leaf 406.1_final_masked.JPG"


#ТЕСТУВАННЯ-2 - МОЇ СТВОРЕНІ ТЕСТУВАЛЬНІ ПРИКЛАДИ --> НА ДЕЯКИХ ТРЕБА ВИДАЛЯТИ ФОН
'''
data_dir="../datasets"
type_of_data="my_test"
image_folder=""
#image_name="healthy_my_on_color_1.JPG"
image_name="photo_2020-04-10_18-45-43.JPG"
#image_name="photo_2020-04-10_18-35-05.JPG"
'''

#ТЕСТУВАННЯ-3 - АУГМЕНТОВАНА СЕГМЕНТОВАНА (КУКУРУДЗА) ТЕСТОВА ВИБІРКА
'''
data_dir="../datasets/PlantVillage/new-plant-diseases-dataset/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)"
type_of_data="valid"
image_folder="Corn_(maize)___Common_rust_"
image_name="RS_Rust 1647_flipLR.JPG"
'''


#ТЕСТУВАННЯ-4 - КОЛЬОРОВИЙ НЕПОФІЛЕНИЙ НА TRAIN/VAL ДАТАСЕТ --> МОЖНА ВИДАЛИТИ ФОН
'''
data_dir = "../datasets/PlantVillage/plantvillage-dataset/color"
type_of_data=""
image_folder="Strawberry___healthy"
image_name="00e9a277-ca5e-4350-95ce-8b2918b69fb9___RS_HL 4667.JPG"
'''




'''-------------------- TRANSFORM THE IMAGE ------------------- '''
#ПЕРЕТВОРЕННЯ ЗОБРАЖЕННЯ НА НОРМАЛІЗОВАНЕ
transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize( 
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]  
                )])


'''----------------------- OPEN THE IMAGE --------------------- '''
#PIL
img = Image.open(data_dir+"/"+type_of_data+"/"+image_folder+"/"+image_name)
#img.show()



#ВИДАЛЕННЯ ЧОРНОГО ФОНУ (ПІДКЗ РІЗІВМИ)
'''
#Варіант-1
threshold = 128  
img_temp = img #копія зображення
img = img.point(lambda p: p <= threshold and 255) #заміна пікселів на чорний і на інший
#img.show()
black = (0,0,0)
width, height = img.size
for x in range(width):
   for y in range(height):
       if  img.getpixel( (x,y) ) != black: #якщо піксель не чорний
           pixel_tmp = img_temp.getpixel((x,y)) #замінити його на оригінальний піксель із оригінального фото
           img.putpixel( (x,y), pixel_tmp)

'''

'''
#Варіант-2
brightness=150
black = (0,0,0)
width, height = img.size
for x in range(width):
   for y in range(height):
       pixel=img.getpixel((x,y))
       R,G,B=pixel
       current_brightness = sum([R,G,B])/3
       if(current_brightness >= brightness):
           img.putpixel( (x,y), black)
'''

'''

'''
        
#img.show()
img_t = transform(img) #трансформуваннэ зображеннэ
img_t = img_t.unsqueze(0) #додаємо 4 вимір - розмір батчу


'''----------------------- OPEN THE MODEL --------------------- '''
test_model = torch.load('../input/25-04-2020/40e_128bs_feF/py_torch_1/alexnet__pytorch_new_last.pth')
test_model.eval()
#print(test_model)

'''
#�рнВЅТРИ МОДЕЛІ
for param in test_model.parameters():
    print(param.data)
'''
 

'''----------------------- CLASSIFICATION --------------------- '''
#СПИСОК КЛАСІВ
def find_classes(directory): 
    classes = os.listdir(directory)
    classes.sort()
    class_to_idx = {classes[i]: i for i in range(len(classes))}
    return classes, class_to_idx

cl, dict_of_classes = find_classes(list_of_classes+"/"+"train") 

#ВАРІАНТ КЛАСИФІКАЦІЧ A
output=test_model(img_t)
prob = nnf.softmax(output, dim=1)
top_p, top_class = prob.topk(1, dim = 1)

res_class = top_class.item()
res_probability = round(top_p.item()*100,3) 

print("So, with the probability " + str(res_probability) + "% " + "the class number is = " + str(res_class) + ".")
print("Moreover, the class name is " +  (list(dict_of_classes.keys())[list(dict_of_classes.values()).index(res_class)]) + ".")



'''
#�АРАМЕТРИ КЛАСИФІКАЦІЇ B
output = test_model.forward(img_t) #відправка зображення на модель
output = torch.exp(output) 
probs, classes = output.topk(1, dim=1) #ймоверність і номер класу
#print(probs.item())
print("B) The class number is = " + str(classes.item()))
print("The class name is " + (list(dict_of_classes.keys())[list(dict_of_classes.values()).index(classes.item())]))    
print()
'''
'''
#ВАРІАНТ КЛАСИФІКАЦІЇ C
output = test_model(img_t)
prediction = int(torch.max(output.data, 1)[1].numpy())
print("C) The class number is = "+ str(prediction))
print("The class name is " + (list(dict_of_classes.keys())[list(dict_of_classes.values()).index(prediction)]))    
'''


