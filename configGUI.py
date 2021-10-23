import tkinter as tk
import configparser
import sys
from googletrans import Translator
from utility import ColoredPrint
from errorHandler import CreateMessage
from subprocess import call
from tkinter import messagebox, Button
from tkinter import ttk



# initialize root object
root = tk.Tk()


class CreateGui:
    def __init__(self):

        #  initialize config
        self.config = configparser.ConfigParser()
        self.config.read('./config.ini')

        # initialize translator
        self.translator = Translator()
        self.language = self.config.get('Options', 'language')

        # initialize colorprinter
        self.log = ColoredPrint()
        self.title = 'Fehler'

        # initialize error handler
        self.errorHandler = CreateMessage()

        # main programm
        self.pyprog = self.config.get('Options', 'mainprogram')

        try:
            # set translated title
            title = self.translator.translate('Optionen', dest=self.language)
            self.title = title
        except ValueError:
            # handle error when wrong language was given
            self.log.err(self.errorHandler.create('invalid_lang'))
            sys.exit()
        except Exception as e:
            # handle error on connection error
            self.log.err(self.errorHandler.create('connection_translator'))

    def check_if_string_in_file(self, file_name, string_to_search):
        """Search for the given string in file and return lines containing that string,
        along with line numbers"""
        line_number = 0
        list_of_results = []

        # open file
        with open(file_name, 'r') as read_obj:
            # read each lines
            for line in read_obj:
                # check if line contains the string
                line_number += 1
                if string_to_search in line:
                    # add line number & line as a tuple in list
                    list_of_results.append((line_number, line.rstrip()))
        # Return list of tuples containing line numbers and lines where string is found
        return list_of_results

    def changeConfig(self, option):
        """Not implemented yet"""
        # find string in config file
        containArr = self.check_if_string_in_file('config.ini', str(option))

        if (containArr):
            print('Yes, string found in file', containArr)
        else:
            print('String not found in file')
        msgText = (self.translator.translate(
            'Änderungen wurden gespeichert', dest=self.language)).text
        messagebox.showinfo('Message', msgText)

    # call main function
    def callpy(self): call(['python', '-i', self.pyprog])

    def create(self):
        # create canvas
        root.title = self.title
        tabControl = ttk.Notebook(root)

        # create tabs
        mainTab = ttk.Frame(tabControl)
        configTab = ttk.Frame(tabControl)

        try:
            # add main tab
            tabControl.add(mainTab, text=(
                self.translator.translate('Barcodesplitter', dest=self.language)).text)

            # add option tab
            tabControl.add(configTab, text=(self.translator.translate(
                'Konfiguration', dest=self.language)).text)
            tabControl.pack(expand=1, fill='both')

            # add elements
            startProgramText = str(self.translator.translate(
                'Program starten', dest=self.language).text)
            startProgram = Button(mainTab, text=startProgramText,
                                command=self.callpy)
            startProgram.grid(column=2, row=1)
            
            root.mainloop()
        except ValueError:
            self.log.err(self.errorHandler.create('invalid_lang'))


if __name__ == '__main__':
    gui = CreateGui()
    gui.create()
