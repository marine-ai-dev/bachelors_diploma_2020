'''----------------------- LIBRARIES -------------------------- '''
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.scrollview import ScrollView


print("Kivy Version: ",kivy.__version__)
print()


'''--------------------- *.KV-CLASSES ------------------------- '''
#ПІДКЛЮЧЕННЯ СТОРІНОК *.KV 
class Main1PageScreen(Screen):  #Main-1
    pass

class HistoryPageScreen(Screen):  #History
    pass

class AboutPageScreen(Screen):  #About
    pass


#СТВОРЕННЯ ГОЛОВНОГО КЛАСУ
class PlantDiseaseAIApp(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition()) #створюємо менеджер екрану
        sm.add_widget(Main1PageScreen(name='main1page'))
        sm.add_widget(HistoryPageScreen(name='historypage'))
        sm.add_widget(AboutPageScreen(name='aboutpage'))
        
        
        if(sm):
            print("\n\n\n ---------- TRUE ---------- \n\n\n")
        else:
            print("\n\n\n ---------- FALSE --------- \n\n\n")
        return sm
 
  

     
'''------------------------ FUNCTIONS ------------------------- '''  
#ПЕРЕЗАВАНТАЖЕННЯ ПЕРЕД КОЖНИМ ЗАПУСКОМ ПРОГРАМИ ВІКНА ПРОГРАМИ
def reset(): 
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}
   
   
'''-------------------------- MAIN ---------------------------- ''' 


if __name__ == '__main__':
    reset()
    PlantDiseaseAIApp().run()
    #print("MEOW")