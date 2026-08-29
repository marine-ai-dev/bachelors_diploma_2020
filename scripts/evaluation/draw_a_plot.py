пimport os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rc('font', family='Times New Roman')
mpl.rc('font', size=16)


full = []

train = []
val = []




#name="20-04-2020"
#name="21-04-2020"
#name="24-04-2020"
name="25-04-2020"


#plot_type = "LOSS"
plot_type = "ACC"



ВІДКРИВАЄМО ПОТРІБНИЙ ФАЙЛ
text_file = open(name + "_" + plot_type + ".txt", "r")
for line in text_file:
    full.append(float(line))


#ДІЛИМО ДАНІ НА НАВЧАЛЬНІ РЕЗУЛЬТАТІ ТА ТЕСТОВІ
for i in range(len(full)):
    if (i % 2 == 0):
        train.append(full[i])
    else:
        val.append(full[i])



#ПОБУДОВА ГРАФІКІВ
fig = plt.figure()
plt.figure(figsize=(10, 4.5))
ax = plt.gca()
ax.set_xlabel('ЕПОХА', fontsize=18) #ОХ





if (plot_type == "LOSS"):
    ax.set_ylabel('ВИТРАТА', fontsize=18) #OY
    ax.set_ylim([0,1.5]) #межі по OY
    major_ticks_y = np.arange(0, 1.5, 0.1)
    minor_ticks_y = np.arange(0, 1.5, 0.05)
    
    if   (name == "20-04-2020"):
        model_id = '1'
    elif (name == "21-04-2020"):
        model_id = '2'
    elif (name == "24-04-2020"):
        model_id = '3'
    elif (name == "25-04-2020"):
        model_id = '4'
    title = 'ФУНКЦІЯ ВТРАТА' (loss function) МОДЕЛІ-' + model_id    


elif (plot_type == "ACC"):
    ax.set_ylabel('ТОЧНІСТЬ', fontsize=18) #OY
    ax.set_ylim([0,1.05]) #межі по OY
    major_ticks_y = np.arange(0, 1.05, 0.1)
    minor_ticks_y = np.arange(0, 1.05, 0.05)
    
    if   (name == "20-04-2020"):
        model_id = '1'
    elif (name == "21-04-2020"):
        model_id = '2'
    elif (name == "24-04-2020"):
        model_id = '3'
    elif (name == "25-04-2020"):
        model_id = '4'
    title = 'ТОЧНІСТЬ (accuracy) МОДЕЛІ-' + model_id   
        
ax.set_title(title, fontsize=20) #заголовок


if (model_id == '1' or model_id == '2'):
    epochs = 15
elif (model_id == '3'):
    epochs = 20
elif (model_id == '4'):
    epochs = 40   


#РОЗЛІНОВКА СІТКИ ГРАФІКУ ПО ОХ
major_ticks_x = np.arange(-1, epochs, 1)
minor_ticks_x = np.arange(-1, epochs, 0.5)


ax.set_xticks(major_ticks_x)
#ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)

ax.grid(which='both')


plt.xticks(rotation=90)


plt.plot(train, '-', color='black', linewidth=1) 
plt.plot(val, '-xk', color='black', linewidth=1) 
plt.legend(['навчальна вибірка', 'тестова вибірка'], prop={"size":14}) #легенда

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # parameterized for portability (was a hardcoded Windows path)
path = os.path.join(BASE_DIR, name + "_" + plot_type + ".png")
plt.savefig(path)

plt.show()