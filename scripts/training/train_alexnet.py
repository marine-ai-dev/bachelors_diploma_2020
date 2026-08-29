def run(): #Виносимо весь код в одну єдину функцію, щоб потім її запустити
    
    '''------------------------ LIBRARIES -------------------------- '''
    import torch
    import torch.nn as nn
    import torch.optim as optim
    import numpy as np
    import torchvision
    from torchvision import datasets, models, transforms
    import matplotlib.pyplot as plt
    import time
    import os
    import copy
    import datetime
    
    
    print("PyTorch Version: ",torch.__version__)
    print("Torchvision Version: ",torchvision.__version__)
    print()
    
    
    '''-------------- LOADING ALEXNET FROM PYTORCH ---------------- '''
    #alexnet_model = models.alexnet(pretrained=True) #завантажуємо модель
    #print(alexnet_model) #виведення всіх параметрів моделі
    #torch.save(alexnet_model, '../input/py_torch/alexnet_original_pytorch.pth') #зберігаємо оригінальну модель
    
    
    '''------------------- PARAMETERS FOR ALEXNET ------------------ '''
    data_dir = "../datasets/PlantVillage/plantvillage-dataset/segmented" #тут зберігаються фото для навчання і тестування
    model_name = "alexnet" #назва моделі, що буде використовуватися
    num_classes=38 
    batch_size = 64 #розмір партії зображени batch_size*iterations --> 1 epoch
    num_epochs = 13 #кількість епох для тренування
    feature_extract = True # False->Finetuting, True->Feature extraction
    
    if(feature_extract==True): #це для назви файлу збереженної моделі
        type_of_training="feature_extract"
    else:
        type_of_training="finetuting"
    
    '''--------------------- HELPER FUNCTIONS --------------------- '''
    #НАВЧаННЯ І ТЕСТУВАННЯ МОДЕЛІ
    #model - PyTorch модель (у нашому випадку Алекснет)
    #dataloaders - словники інструментів для завантаження даних
    #criterion - функція втрат 
    #optimizer - оптимізатор
    #num_epochs - кысть епох для навчання та тестування
    #is_inseption - чи єдана модель моделлю inception, у якої трохи інші там параметри 
    #після кожної епохи відбуваться повний валідаційний етап
    def train_model(model, dataloaders, criterion, optimizer, num_epochs=25, is_inception=False):
        since = time.time()
        val_acc_history = []
        best_model_wts = copy.deepcopy(model.state_dict())
        best_acc = 0.0
    
        for epoch in range(num_epochs):
            print('Epoch {}/{}'.format(epoch, num_epochs - 1))
            print('-' * 10)
    
            # Кожна епоха має фазу навчання і валідації
            for phase in ['train', 'val']:
                if phase == 'train':
                    model.train()  # Відправляємо модель на тренерування
                else:
                    model.eval()   # Відправляємо модель на її оцінівання
    
                running_loss = 0.0
                running_corrects = 0
    
                # Перебір даних 
                for inputs, labels in dataloaders[phase]:
                    inputs = inputs.to(device)
                    labels = labels.to(device)
    
                    # обнулюення параметрів градієнта
                    optimizer.zero_grad()
    
                    # вперед
                    # слідкувати за історією, якщо відбуваться навчання
                    with torch.set_grad_enabled(phase == 'train'):
                        # Отримуємо вихідні дані моделі і обчислюємо втрати
                        # Особливий випадок для inception, тому що при навчанні вона маєдопоміжний вихід 
                        
                        # У режимі навчання ми обраховуємо втрату сумючи кінцевий та додатковий виходи
                        # Але у режиі тестування ми використовуємо лише фінальний вихід
                        if is_inception and phase == 'train': 
                            # Взято із https://discuss.pytorch.org/t/how-to-optimize-inception-model-with-auxiliary-classifiers/7958
                            outputs, aux_outputs = model(inputs)
                            loss1 = criterion(outputs, labels)
                            loss2 = criterion(aux_outputs, labels)
                            loss = loss1 + 0.4*loss2
                        else:
                            outputs = model(inputs)
                            loss = criterion(outputs, labels)
    
                        _, preds = torch.max(outputs, 1) 
    
                        # назад + оптимізуємо, якщо лише знаходимося на етапі тренування 
                        if phase == 'train':
                            loss.backward()
                            optimizer.step()
    
                    # статистика
                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)
    
                epoch_loss = running_loss / len(dataloaders[phase].dataset)
                epoch_acc = running_corrects.double() / len(dataloaders[phase].dataset)
    
                print('{} Loss: {}:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))
    
                # deep copy моделі
                if phase == 'val' and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    best_model_wts = copy.deepcopy(model.state_dict())
                if phase == 'val':
                    val_acc_history.append(epoch_acc)
                    
            '''------------------- ЗБЕРІГАЄМО ОТРИМАНУ МОДЕЛЬ У КОЖНІЙ ЕПОСІ -------------------'''
            path_to_save_each_epoch='../input/py_torch/alexnet_' + str(type_of_training) + '_pytorch_new_'+str(epoch)+'.pth'
            torch.save(model, path_to_save_each_epoch) 
            
            
            '''-------------------- ЗБЕРІГАЄМО ЧЕКПОІНТ МОДЕЛІ У КОЖНІЙ ЕПОСІ ------------------'''
            path_to_save_each_epoch_checkpoint='../input/py_torch/alexnet_' + str(type_of_training) + '_pytorch_new'+'_CHECKPOINT_'+str(epoch)+'.pth'
            torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': loss,
            }, path_to_save_each_epoch_checkpoint)
            
    
            #виводимо поточний системний час
            currentDT = datetime.datetime.now() 
            print (str(currentDT))
            print()
    
        time_elapsed = time.time() - since
        print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
        print('Best val Acc: {:4f}'.format(best_acc))
    
        # Завантаження найкращих ваг моделі
        model.load_state_dict(best_model_wts)
        
        return model, val_acc_history
    
    
    '''------------------ SET MODEL PARAMETERS’ ------------------- '''
    def set_parameter_requires_grad(model, feature_extracting):
        if feature_extracting: #якщо виконується feature extracting
            for param in model.parameters():
                param.requires_grad = False #ставить ці всі параметри моделі у False
    
    #За замовчуваням, коли завантажується pretrained модель, 
    #всі її параметри мають .requires_grad=True, що є добрим лише у випадку, коли
    #ми навчаємо модель з нуля (training from scratch) чи робимо finetuning.
    #Однак, коли ми виконуємо feature extracting і лише хочемо обчислити градієнт для 
    #щойно ініціалізованого нового шару, тоді ми хочемо,
    #щоб інші параметри не вимагали градієнтів
    
    
    '''----------- INITIALIZE AND RESHAPE THE NETWORK  ------------ '''
    #Необхідно перевизначити к-сть виходів моделі для нашої задачі,
    #адже кожна pretrained модель була навчена на датасеті Imagenet, тому має 1000 виходів
    #Ціль цього блоку кода - reshape останній шар ШНМ під к-сть класів для нашої задачі
    
    #!!! РІЗНИЦЯ МІЖ FINETUNING ТА FEATURE-EXTRACTION
    #--- Коли виконується feature extracting, ми хочемо лише оновити параметри останнього шару,
    #тобто, ми хочемо лише но на дйеннс вер моделр грабалчуващіP
    

    #AlexNet потребуєть на вході розмір зображення 224*224
    
    def initialize_model(model_name, num_classes, feature_extract, use_pretrained=True):
        model_ft = None
        input_size = 0
    
        if model_name == "alexnet":
            model_ft = models.alexnet(pretrained=use_pretrained) #використовуємо pretrained модель
            set_parameter_requires_grad(model_ft, feature_extract)
            num_ftrs = model_ft.classifier[6].in_features
            model_ft.classifier[6] = nn.Linear(num_ftrs,num_classes) #задаємо к-сть класів
            input_size = 224
        else:
            print("Invalid model name, exiting...")
            exit()
    
        return model_ft, input_size
    
    #ІНІЦІАЛІЗУЄМО МОДЕЛЬ ДЛЯ ЗАПУСКУ
    model_ft, input_size = initialize_model(model_name, num_classes, feature_extract, use_pretrained=True)
    #Виводимо модель, яку ми тільки що створили на екран
    print(model_ft)
    print()
    
    '''------------------------ LOAD DATA ------------------------- '''
    #Моделі, що були pretrained від PyTorch, були жорстоко закодовані під певні значення нормалізації!
    #Описано тут: https://pytorch.org/docs/master/torchvision/models.html
    
    # Аугментація даних та їх нормалізація для навчання
    # Просто нормалізація для перевірки
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(input_size),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize(input_size),
            transforms.CenterCrop(input_size),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }
    
    print("Initializing Datasets and Dataloaders...")
    print()
    
    # Створюємо датасети для навчання та валідації
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x]) for x in ['train', 'val']}
    # Створюємо завантажувачі даних для навчання та валідації
    dataloaders_dict = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=batch_size, shuffle=True, num_workers=4) for x in ['train', 'val']}
        
    # Визначаємо, чи є доступний GPU / CPU
    #device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    device="cpu" #відправляємо на CPU
    print("Device: ", device)
    print()
    
    '''------------------- CREATE THE OPTIMIZER ------------------- '''
    #Створення оптимізатора, що буде оновлювати бажані параметри
    #Тепер, всі параметри, що мають .requires_grad=True, мають бути оптимізовані
    #Тому, створюємо список параметрів та передаємо їх в алгоритм SGD
    
    # Відправляємо модель на GPU / CPU
    model_ft = model_ft.to(device)
    
    # Збираємо параметри, які будуть оптимізовані/оновлені у цьому запуску.
    #  Якщо ми finetuning, то ми оновлюємо всі параметри. Однак, якщо 
    #  ми використовуємо метод feature extract, ми лише оновлюємо параметри, що
    #  ми щойно ініціалізували, тобто, параметри із requires_grad, що рівні True
    params_to_update = model_ft.parameters()
    print("Params to learn:")
    if feature_extract:
        params_to_update = []
        for name,param in model_ft.named_parameters():
            if param.requires_grad == True:
                params_to_update.append(param)
                print("\t",name)
    else:
        for name,param in model_ft.named_parameters():
            if param.requires_grad == True:
                print("\t",name)
    print()
    
    # Observe that all parameters are being optimized
    optimizer_ft = optim.SGD(params_to_update, lr=0.001, momentum=0.9)
    
    
    '''------------- RUN TRAINING AND VALIDATION STEP ------------- '''
    #learning rate не єоптимальним ля всіх pretrained моделей, тому його треба підбирати
    # Здаємо loss fxn
    criterion = nn.CrossEntropyLoss()
    
    #Тренування та оцінювання моделі
    model_ft, hist = train_model(model_ft, dataloaders_dict, criterion, optimizer_ft, num_epochs=num_epochs, is_inception=False)
    
    #!!! 
    torch.save(model_ft, '../input/py_torch/alexnet_'+'_pytorch_new_last.pth')
    
    ohist = []
    ohist = [h.cpu().numpy() for h in hist]
    plt.title("Validation Accuracy vs. Number of Training Epochs")
    plt.xlabel("Training Epochs")
    plt.ylabel("Validation Accuracy")
    plt.plot(range(1,num_epochs+1),ohist,label="Pretrained")
    plt.ylim((0,1.))
    plt.xticks(np.arange(1, num_epochs+1, 1.0))
    plt.legend()
    plt.show()
    

'''------------- LAUNCHING A PROGRAM ------------- '''
if __name__ == '__main__':
    import datetime
    current_DT = datetime.datetime.now()
    print (str(current_DT))
    print()
    
    run()
