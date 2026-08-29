'''---------------------- FLASK LIBRARIES --------------------- '''
import os
import datetime
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # parameterized for portability (was hardcoded Windows paths)
import flask
from flask import Flask, render_template, request, redirect, flash, url_for
print("• Flask Version: ",flask.__version__)

'''--------------------- PYTORCH LIBRARIES -------------------- '''
import torch
from torchvision import datasets, models, transforms
from PIL import Image
import os
import torch.nn.functional as nnf

'''---------------------- MYSQL LIBRARIES --------------------- '''
import mysql.connector
from mysql.connector import Error

'''---------------------- OTHER LIBRARIES --------------------- '''
from collections import Counter
import matplotlib.pyplot as plt

number_of_classes=38

'''---------------------- MYSQL FUNCTIONS --------------------- '''
# ІДКЛЮЧЕННЯ ДО MYSQL
def connect_to_mysql_database():
    try:
        connection = mysql.connector.connect(host='localhost', 
                                             database='mydb', 
                                             user='root', 
                                             password=os.environ.get("MYSQL_PASSWORD"), 
                                             use_pure=True)
        
        db_Info = connection.get_server_info()
        
        print("• Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("• You're connected to database: ", record)
        print("• DB connection = ", connection)
        print()
        return connection
        
    except Error as e:
        print("ERROR WHILE CONNECTING TO MySQL: ", e) 
        print()
        raise SystemExit()
        
      

'''--------------------- PYTORCH FUNCTIONS -------------------- '''
#?ЕРЕТВОРЕННЯ ЗОБРАЖЕННЯ НА НОРМАЛІЗОВАНЕЕ
transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize( 
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]  
                )])

#Список КЛАСІВ - із текстового файлу зчитування
def find_classes(directory): 
    f = open(directory, "r")
    classes = list(f)
    classes.sort()
    class_to_idx = {classes[i]: i for i in range(len(classes))}
    return classes, class_to_idx


#ªКЛАСИФІКАЦІЯ ЗОБРАЖЕННЯ
def image_classification(pth):
    img = Image.open(pth)
    img_t = transform(img) #трансформування зображеннэ
    img_t = img_t.unsqueze(0) #додаємо 4 вимір - розмір батчу
    #img.show()
    model_path = os.path.join(BASE_DIR, "..", "models", "alexnet__pytorch_new_last.pth")  # parameterized for portability (was a hardcoded Windows path)
    test_model = torch.load(model_path)
    test_model.eval()  
    
    #ВАРІАНТ КЛАСИФІКАЦІЇ A
    output=test_model(img_t)
    prob = nnf.softmax(output, dim=1)
    top_p, top_class = prob.topk(1, dim = 1)
    res_class = top_class.item()
    res_probability = round(top_p.item()*100,3)
    
    cl, dict_of_classes = (find_classes(os.path.join(BASE_DIR, "list_of_classes.txt")))
    class_name=(list(dict_of_classes.keys())[list(dict_of_classes.values()).index(res_class)])
    print()
    print(".")
    print("RESULT OUTPUT TO PYTHON COMMAND LINE: ")
    
    print("So, with the probability " + str(res_probability) + "% " + "the class number is = " + str(res_class) + ".")
    print("Moreover, the class name is " + str(class_name) + ".")
    print()
    
    return str(res_probability), str(res_class), str(class_name)
 

'''---------------------- OTHER FUNCTIONS --------------------- '''
#Сортування
def s(val):
     return val[-1]

'''--------------------------- CONFIG ------------------------- '''
app = Flask(__name__) #Створюємо додаток через Flask
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(24)) #Секретний ключ для додатку
image_path='' #Глобальна змінна, що зберігатиме шлях до оброблюваного зображення
my_date_time ='' #Глобальна змінна для зберігання часу та дати, коли було класифіковане зображення, для запису у історію БД
my_connection = connect_to_mysql_database() #підключаємося до MYSQL
   
'''---------------------- FLASK FUNCTIONS --------------------- '''
 
######################## 
ГОЛОВНА СТОРІНКА ######################## 
@app.route("/")
def Home():
    return render_template('HomePage.html')

@app.route("/HomePage.html")
def Home2():
    return render_template('HomePage.html')

############################### MAIN-1 ############################ 
@app.route("/Main1Page.html")
def Main1Page():
    return render_template('Main1Page.html') 

#UPLOAD AN IMAGE
@app.route("/Main1Page.html", methods = ["POST"])
def upload_image():
    if request.method == "POST":
        file = request.files["file"]
        if (file.filename != ''):
            #Куди будемо зберігати завантажене зображення
            my_path=os.path.join(BASE_DIR, "static", "uploaded_images")
            
            #Змінюємо назву зображення на таку, яка мене влаштовує, а не така, яка вона була з початку
            old_name = file.filename
            name, ext = old_name.rsplit('.', 1) #Розбиваємо назву зображення на власне назву і розширення зображення з кінця і тільки один раз (тобто назва.розширення)
            
            #назва зображення складаться із дати і часу, коли воно було завантажене
            my_date=str(datetime.datetime.now().date())
            my_time=str(datetime.datetime.now().time())
            
            #також зберігаємо повне значення часу та дати, для подальшого запису у історію БД
            global my_date_time
            my_date_time = my_date +" "+ my_time 
                        
            #робимо потрібне форматування для того, щоб із дати та часу створити нову назву завантаженого зображеннэ
            my_time = my_time.replace(":", "-") #замінюємо непотрібні символи на бажані
            my_time = my_time.replace(".", "-") #замінюємо непотрібні символи на бажані
            result = my_date + "___" + my_time #створюємо бажану назву зображеннэ
            
            #утворюємо нову назву + додаємо розширеннэ зображеннэ
            new_name = result + "." + ext
            
            #зберігаємо нову назву зображеннэ
            file.filename = new_name
            
            #Зберігаємо зображення 
            global image_path
            image_path = os.path.join(my_path, file.filename)
            file.save(image_path)
            return redirect('/Main2Page.html') #після завантаженнэ фото перейти до його обробки та класифікації
        else:
            flash('no image selected for uploading. please, choose an image!', "warning")
            return redirect(request.url) 

############################### MAIN-2 ############################
@app.route("/Main2Page.html") 
def Main2Page():
    #ймовірність, номер класу та назва класу після класифікації зображеннэ
    prob, class_num, class_name = image_classification(image_path)
    
    #обрізка шляху до папки "static"
    cropped_path=image_path[image_path.find("static") : ]
    cropped_path=cropped_path.replace("\\", "/")
    print(cropped_path)
    

       
    '''--------------------------- QUERY -------------------------- '''
    #ЗАПИТ ДО MYSQL: повертає інформацію про хворобу (якщо така є) за номером класу
    if (my_connection): #якщо існує з'єднання, то робимо запит
        #print("MEOW")
        my_select = "SELECT CLASS.class_id, DISEASE.* " 
        my_from =   "FROM DISEASE, CLASS "
        my_where =  "WHERE (DISEASE.disease_id = CLASS.DISEASE_disease_id) and (CLASS.class_id='"+str(class_num)+"')"
        my_query = my_select + my_from + my_where
        cursor = my_connection.cursor()
        cursor.execute(my_query)
        records = cursor.fetchall()
        print("Total number of rows is: ", cursor.rowcount) #Має бути один рядок 

        
        if (cursor.rowcount>0): #Якщо існує запис
            is_disease=True
            print("_______is_disease_______ = ", is_disease)
            my_class_id = records[0][0]
            my_disease_id = records[0][1]
            my_disease_name = records[0][2]
            my_pathogen = records[0][3]
            my_disease_description = records[0][4]
            print("• Class id = ", my_class_id)
            print("• Disease id = ", my_disease_id)
            print("• Disease name = ", my_disease_name)
            print("• Pathogen = ", my_pathogen)
            print("• Disease description = ", my_disease_description)
            print()
            
            #ЗАПИТ: якщо у базі відсутня інформація про лікування — для моделі результат
            my_select = "SELECT DRUG.drug_name, DRUG.pharma_company_name, DRUG.drug_description, DRUG_and_DISEASE.instruction_description "
            my_from =   "FROM DRUG, DRUG_and_DISEASE, DISEASE "
            my_where =  "WHERE DISEASE.disease_id = '" + str(my_disease_id) + "' and DISEASE.disease_id = DRUG_and_DISEASE.DISEASE_disease_id and DRUG_and_DISEASE.DRUG_drug_id = DRUG.drug_id "
            my_query = my_select + my_from + my_where
            cursor = my_connection.cursor()
            cursor.execute(my_query)
            my_records = cursor.fetchall()
            print("Total number of rows is: ", cursor.rowcount)
            #for row in my_records:
                #print (♦ ",row)
            print()
            
            #ЗАПИТ: робимо запис у історію БД
            my_insert = "INSERT INTO CASE_OF_THE_DISEASE (case_date_time, probability, CLASS_class_id)"
            my_values = "VALUES ('"+str(my_date_time)+"',"+str(prob)+", "+str(my_class_id)+");"
            my_query = my_insert + my_values
            cursor = my_connection.cursor()
            cursor.execute(my_query)
            my_connection.commit() #ОБОВ'ЯЗКОВО!! Інакше зміни не будуть виконані
            
            
            return render_template('Main2Page.html', 
                                    prob=prob, 
                                    disease_name=my_disease_name, 
                                    pathogen=my_pathogen, 
                                    disease_description=my_disease_description,
                                    records = my_records,
                                    is_disease=is_disease,
                                    src1=cropped_path)
        
        
        else: #ЗАПИТ: якщо запис у БД відсутній, тобто рослина здорова
            is_disease=False
            print("_______is_disease_______ = ", is_disease)
            #Тому вибираємо назву класу просто і повертаємо результат
            my_select = "SELECT class_id, alias_class_name " 
            my_from =   "FROM CLASS "
            my_where =  "WHERE class_id = '"+class_num+"'"
            my_query = my_select + my_from + my_where
            cursor = my_connection.cursor()
            cursor.execute(my_query)
            records = cursor.fetchall()
            print("Total number of rows is: ", cursor.rowcount) #Має бути один запис
            my_class_id = records[0][0]
            my_class_alias_name = records[0][1]
            print("• Class id = ", my_class_id)
            print("• CLass alias name = ", my_class_alias_name)
            
            #ЗАПИТ: робимо запис у історію БД
            my_insert = "INSERT INTO CASE_OF_THE_DISEASE (case_date_time, probability, CLASS_class_id)"
            my_values = "VALUES ('"+str(my_date_time)+"',"+str(prob)+", "+str(my_class_id)+");"
            my_query = my_insert + my_values
            cursor = my_connection.cursor()
            cursor.execute(my_query)
            my_connection.commit() #ОБОВ'ЯЗКОВО!! Інакше зміни не будуть виконані    
            
            return render_template('Main2Page.html', 
                                    prob=prob,
                                    class_alias_name = my_class_alias_name,
                                    is_disease=is_disease,
                                    src1=cropped_path)
        
        
    '''------------------------------------------------------------ '''
    
############################## HISTORY ############################ 
@app.route("/HistoryPage.html")
def HistoryPage():
    #ЗАПИТ ДО MYSQL: ПОВЕРТАЄ ВСІ ЗАПИСИ ПРО ВИПАДКИ КЛАСИФІКАЦІЇ ЗАХВОРЮВАННЯ І ЗДОРОВИХ РОСЛИН
    if (my_connection): #якщо існує з'єднання, то робимо запит
        
        #²иводимо всю БД із історією
        my_select = "SELECT CASE_OF_THE_DISEASE.case_id, CASE_OF_THE_DISEASE.case_date_time, CASE_OF_THE_DISEASE.probability, CLASS.alias_class_name "
        my_from =   "FROM CASE_OF_THE_DISEASE, CLASS "
        my_where =  "WHERE CASE_OF_THE_DISEASE.CLASS_class_id = CLASS.class_id "
        my_query = my_select + my_from + my_where
        cursor = my_connection.cursor()
        cursor.execute(my_query)
        my_records = cursor.fetchall()
        print("Total number of rows is: ", cursor.rowcount)
        #for row in my_records:
            #print (row)
       
    return render_template('HistoryPage.html', records = my_records)    


############################# TREATMENT ########################### 
@app.route("/Treatment1Page.html")
def Treatment1Page():
    #ЗАПИТ: на отримання інформації для вибору у випадаючому списку
    if (my_connection): #Якщо існує з'єднання, то робимо запит
        
        #ЗАПИТ: ЛИШЕ ВИПАДКИ, ПОВ'ЯЗАНІ ІЗ ЗАХВОРЮВАННЯМ
        my_select = "SELECT CASE_OF_THE_DISEASE.case_id, CASE_OF_THE_DISEASE.case_date_time,CASE_OF_THE_DISEASE.probability, CLASS.alias_class_name, CLASS.DISEASE_disease_id "
        my_from =   "FROM CASE_OF_THE_DISEASE, CLASS "
        my_where =  "WHERE CASE_OF_THE_DISEASE.CLASS_class_id = CLASS.class_id and (CLASS.DISEASE_disease_id IS NOT NULL) "
        my_order =  "ORDER BY CASE_OF_THE_DISEASE.case_id ASC "
        my_query = my_select + my_from + my_where + my_order
        cursor = my_connection.cursor()
        cursor.execute(my_query)
        my_records_1 = cursor.fetchall()
        print("Total number of rows is: ", cursor.rowcount)
        #for row in my_records_1:
            #print (row)
        
        #ЗАПИТ: ВСІ МОЖЛИВІ ПРЕПАРАТИ
        my_select = "SELECT DRUG.drug_id, DRUG.drug_name, DRUG.pharma_company_name "
        my_from =   "FROM DRUG "
        my_query = my_select + my_from
        cursor = my_connection.cursor()
        cursor.execute(my_query)
        my_records_2 = cursor.fetchall()
        print("Total number of rows is: ", cursor.rowcount)
        #for row in my_records_2:
            #print (row)        
    return render_template('Treatment1Page.html', records_1 = my_records_1, records_2 = my_records_2)       

#GET DATA FROM FORM IN TREATMENT-1
@app.route("/Treatment1Page.html", methods=['GET', 'POST'])
def get_form_data():
    if request.method == "POST":
        #Отримуємо результат вибору із випадаючого списку (вибір випадку захворювання)
        get_selected_case = str(request.form.get("select_1")) 
        #Отримуємо результат вибору із випадаючого списку (отримуємо обраний препарат)

        get_selected_drug = str(request.form.get("select_2"))
        #тримуємо опису про treatment result
        get_selected_treatment_result = str(request.form.get("text_area"))
        
        #Якщо всі поля заповнені (непорожні)
        if(get_selected_case!='' and get_selected_drug!='' and get_selected_treatment_result!=''):
            print("----------------------------------------------------")
            get_selected_case = get_selected_case.split("/") #розбиваємо запис на окремі складові
            get_selected_drug = get_selected_drug.split("/") #розбиваємо запис на окремі складові
            
            my_selected_case_id = get_selected_case[0]  
            my_selected_disease_id_1 = get_selected_case[-1] 
            print(my_selected_disease_id_1)
            print(type(my_selected_disease_id_1))
            
            my_selected_drug_id = get_selected_drug[0] 
            
            #ШУКАЄМО ЗА ВІДПОВІДНИМ ПРЕПАРАТОМ СПИСОК ВСІХ ХВОРОБ, ЯКІ ВІН ЛІКУЄ

            if (my_connection): #якщо існує з'єднання, то робимо запит
                my_select = "SELECT DRUG_and_DISEASE.DISEASE_disease_id "
                my_from =   "FROM DRUG, DRUG_and_DISEASE "
                my_where =  "WHERE DRUG.drug_id = '"+str(my_selected_drug_id)+"' and DRUG.drug_id=DRUG_and_DISEASE.DRUG_drug_id "
                my_query = my_select + my_from + my_where
                cursor = my_connection.cursor()
                cursor.execute(my_query)
                my_records_3 = cursor.fetchall()
                print("Total number of rows is: ", cursor.rowcount)
                for i in range(len(my_records_3)):
                    my_records_3[i] = my_records_3[i][0]
                print(my_records_3)
                
                #Якщо ІД хвороби випадку не існує у списку всіх хвороб, що може лікувати даний препарат
                if (int(my_selected_disease_id_1) not in my_records_3): 
                    flash("this drug is not suitable for this disease. choose another one. try again", "warning")
                    return redirect(request.url)   
                
                else:
                    print(get_selected_case)
                    print(get_selected_drug)
                    print(get_selected_treatment_result)
                    
                    
                    current_date=str(datetime.datetime.now().date())
                    current_time=str(datetime.datetime.now().time())
                    
                    #днато вдегригатний для додальшого запису у сіторіючж БД
                    current_date_time=current_date +" "+current_time
                    print("current_date_time = ", current_date_time)
                    print("----------------------------------------------------")
                
                    #ЗАПИТ: запис даних до БД
                    my_insert = "INSERT INTO TREATMENT_HISTORY (treatment_date_time, CASE_OF_THE_DISEASE_case_id, DRUG_drug_id, treatment_result) "
                    my_values = "VALUES('"+str(current_date_time)+"',"+str(my_selected_case_id)+","+str(my_selected_drug_id)+",'"+str(get_selected_treatment_result)+"'); "
                    my_query = my_insert + my_values
                    cursor = my_connection.cursor()
                    cursor.execute(my_query)
                    my_connection.commit() #ОБОВ'ЯЗКОВО!! Інакше зміни не будуть виконані
                    
                    #Повідомляємо користувачу, що запис відбувся
                    flash("a reccord was successfully added to treatment history", "success")
                    return redirect("/Treatment1Page.html")
        else:
            flash("not all not all items are filled / selected. try again", "warning")
            return redirect(request.url)           

@app.route("/Treatment2Page.html")
def Treatment2Page():
    if (my_connection): #якщо існує з'єднання, то робимо запит
        my_select = "SELECT 	TREATMENT_HISTORY.treatment_id, \
                        		TREATMENT_HISTORY.treatment_date_time, \
                                TREATMENT_HISTORY.CASE_OF_THE_DISEASE_case_id,  \
                                CASE_OF_THE_DISEASE.case_date_time, \
                                CASE_OF_THE_DISEASE.probability, \
                                CLASS.alias_class_name, \
                                DRUG.drug_name, \
                                DRUG.pharma_company_name, \
                                TREATMENT_HISTORY.treatment_result "
        my_from =   "FROM TREATMENT_HISTORY, CASE_OF_THE_DISEASE, CLASS, DRUG "
        my_where =  "WHERE TREATMENT_HISTORY.CASE_OF_THE_DISEASE_case_id = CASE_OF_THE_DISEASE.case_id and \
                           CASE_OF_THE_DISEASE.CLASS_class_id = CLASS.class_id and \
                           TREATMENT_HISTORY.DRUG_drug_id = DRUG.drug_id "
        my_query = my_select + my_from + my_where       
        cursor = my_connection.cursor()
        cursor.execute(my_query)
        my_records = cursor.fetchall()
        print("Total number of rows is: ", cursor.rowcount)
        #for row in my_records:
            #print (row)
            
    return render_template('Treatment2Page.html', records = my_records)    

############################# STATISTICS ########################### 
@app.route("/Statistics1Page.html")
def Statistics1Page():
        if (my_connection): #якщо існує з'єднання, то робимо запит
            #ЗАПИТ: ВСІ МОЖЛИВІ ЗАПИСИ ІЗ КЛАСИФІКАЦІЄЮ ЗАХВОРЮВАННЯ
            my_select = "SELECT * "
            my_from =   "FROM CASE_OF_THE_DISEASE "
            my_query = my_select + my_from
            cursor = my_connection.cursor()
            cursor.execute(my_query)
            my_records_1 = cursor.fetchall()
            print("Total number of rows is: ", cursor.rowcount)
            #for row in my_records_1:
                #print (row)  
             
            #ВИЗНАЧАЄМО ЧАСТОТУ КОЖНОГО КЛАСУ
            class_id = [class_id[-1] for class_id in my_records_1] #виписуємо всі останні значення рядочка (номер класу)
            c = Counter(class_id) #Отримуємо частотний словник 
            #print("c = ", c) 
            
            c = dict(c) #конвертуємо у словник
            
            #Додаємо ті класи, які іще не зустрічалися у ВИПАДКАХ ЗАХВОРЮВАННЯ (частота = 0)
            for i in range(number_of_classes):
                if i not in c.keys():
                        c_new={i:0}
                        dict.update(c,c_new)
                    
            #print ("c_new = ", c)    
            
            c = list(sorted(c.items(), reverse=False)) #сортуємо у порядку зростання
            #print (c)
            
            my_classes=[] #список класів
            my_frequencies=[] #список відповідних частот
            
            #±творюємо два масиви- клас/частота
            for i in range(len(c)): 
                my_classes.append(c[i][0])
                my_frequencies.append(c[i][1])
            
            
            #ЗАПИТ: знаходимо назви класів
            my_select = "SELECT CLASS.class_id, CLASS.alias_class_name "
            my_from =   "FROM CLASS "
            my_query = my_select + my_from
            cursor = my_connection.cursor()
            cursor.execute(my_query)
            my_records_2 = cursor.fetchall()
            #for row in my_records_2:
                #print (row) 
            '''
            #Замінюємо номери класів на назви класів
            for i in range(len(my_classes)):
                my_classes[i]=my_records_2[i][1]
            '''
            print(my_classes)
            print(my_frequencies)
            
            plt.figure(figsize=(16, 9))
            ax = plt.gca()
            ax.set_title('CLASSES FREQUENCY IN CASES', fontsize=30, fontname="Times New Roman")
            ax.set_xlabel('class', fontsize=30, fontname="Times New Roman")
            ax.set_ylabel('frequency', fontsize=30, fontname="Times New Roman")
            
            x=range(len(my_frequencies))
            
            ax.bar(x, my_frequencies, align='center', width=1, color='green', edgecolor='black')
            ax.set_xticks(x)
            labels = [labels[-1] for labels in my_records_2]
            ax.set_xticklabels(my_classes, rotation='vertical')

            #plt.grid()
            path1 = os.path.join(BASE_DIR, "static", "images", "classes_histogram.png")
            path2 ='/static/images/classes_histogram.png'
            plt.savefig(path1, transparent=True)
            #plt.show()   
            
        return render_template('Statistics1Page.html', path=path2, records=my_records_2)

#BUILD A HISTOGRAM 
@app.route("/Statistics1Page.html", methods=['GET', 'POST'])
def BuildHistogram():
        #if request.method == "POST":
    return redirect("/Statistics1Page.html")

                        
############################### ABOUT ############################# 
@app.route("/AboutPage.html")
def AboutPage():
    return render_template('AboutPage.html')    

########################### PRIVACY POLICY ######################### 
@app.route("/PrivacyPolicyPage.html")
def PrivacyPolicyPage():
    return render_template('PrivacyPolicyPage.html')    


  

    
'''----------------------------- MAIN ------------------------- '''
if __name__ == "__main__":
    app.run(host='0.0.0.0')

    
    
    
    