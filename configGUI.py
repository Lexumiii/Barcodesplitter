from tkinter import ttk
import tkinter as tk
from tkinter import *
import configparser
from googletrans import Translator, constants
from pprint import pprint
from utility import ColoredPrint
import httpcore   
from errorHandler import CreateMessage
root = tk.Tk()  

class CreateGui:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('./config.ini')
        self.translator = Translator()
        language = self.config.get("Options", "language")
        self.log = ColoredPrint()
        self.title = 'Fehler'
        self.errorHandler = CreateMessage()
        try: 
            title = self.translator.translate("Optionen", dest=language)
            self.title = title
        except Exception as e:
            if str(e).replace(' ', '') == "Thereadoperationtimedout" or str(e).replace(' ', '') == "timedout":
                self.log.err(self.errorHandler.create("Connection_translator"))
            else: 
                print(e)
            self.titel = "Error"

        
    def create(self):
        root.title = self.title
        tabControl = ttk.Notebook(root)  
        # create tabs
        optionTab = ttk.Frame(tabControl)
        configTab = ttk.Frame(tabControl)
              
        tabControl.add(optionTab, text ='Optionen')
        tabControl.add(configTab, text ='Konfiguration')
        tabControl.pack(expand = 1, fill ="both")
        
        # set label
        ttk.Label(optionTab, 
            text ="Wählen Sie Ihre Optionen").grid(column = 0, 
                               row = 0,
                               padx = 30,
                               pady = 30)  
        ttk.Label(configTab,
            text ="Wählen Sie Ihre Konfigurationen").grid(column = 0,
                                    row = 0, 
                                    padx = 30,
                                    pady = 30)
        root.mainloop()
        
    def changeConfig(option, value, newValue): 
        print("Not implemented yet")
    

class translateValue: 
    def __init__(self):
        self.text = ''
        self.config = configparser.ConfigParser()
        self.config.read('./config.ini')
                self.langTo = self.config.get()
        

if __name__ == "__main__":
    gui = CreateGui()
    gui.create()