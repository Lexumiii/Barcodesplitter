
from datetime import datetime, date
import glob
from os.path import join, basename
import os
import shutil

class ColoredPrint:
    def __init__(self):
        self.PINK = '\u001b[35m'
        self.OKBLUE = '\u001b[34m'
        self.OKGREEN = '\u001b[32m'
        self.WARNING = '\u001b[33m'
        self.FAIL = '\u001b[31m'
        self.ENDC = '\u001b[0m'
        self.LOGF = 'logfile.log'
        self.msg = ''

    def disable(self):
        self.PINK = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

    def store(self):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.LOGF, mode='a') as file_:
            file_.write(f"{self.msg} -- {date}")
            file_.write("\n")

    def success(self, *args, **kwargs):
        self.msg = ' '.join(map(str, args))
        print(self.OKGREEN + self.msg + self.ENDC, **kwargs)
        return self

    def info(self, *args, **kwargs):
        self.msg = ' '.join(map(str, args))
        print(self.OKBLUE + self.msg + self.ENDC, **kwargs)
        return self

    def warn(self, *args, **kwargs):
        self.msg = ' '.join(map(str, args))
        print(self.WARNING + self.msg + self.ENDC, **kwargs)
        return self

    def err(self, *args, **kwargs):
        self.msg = ' '.join(map(str, args))
        print(self.FAIL + self.msg + self.ENDC, **kwargs)
        return self

    def pink(self, *args, **kwargs):
        self.msg = ' '.join(map(str, args))
        print(self.PINK + self.msg + self.ENDC, **kwargs)
        return self
    
    def write(self, *args):
        self.msg = ' '.join(map(str, args))
        return self
    
    def get_line(self, lookup):
        with open(self.LOGF) as myFile:
            for num, line in enumerate(myFile, 1):
                if str(lookup) in line:
                    print('found at line:', num)
        return self
class CalcTime:
    def __init__(self):
        self.msg = 'Create date'
        
    def calc_time(self):
        today = datetime.now()
        d = dict()
        current_date = today.strftime("%d/%m/%Y/%H/%M/%S")
        current_date = current_date.split('/')
        d['day'] = current_date[0]
        d['month'] = current_date[1]
        d['year'] = current_date[2]
        d['hour'] = current_date[3]
        d['minute'] = current_date[4]
        d['second'] = current_date[5]
        return d
    
class DirHandler:
    def __init__(self):
        self.image_folder = './img/'
        self.batch_folder = './input/'
        self.output_folder = './output/'
        self.archive_folder = './archiv/'
        self.mimetype_pdf = 'pdf'
        self.mimetype_img = 'img'

        
    def make_dir(self, dir_name):
        try:
            os.mkdir(dir_name)
        except FileExistsError:
            pass
        
    def remove_images(self):
        # remove images
        for f in os.listdir(self.image_folder):
            os.remove(os.path.join(self.image_folder, f))

    def remove_folder(self, folder):
        #remove image folder
        if os.path.exists(folder):
            # checking whether the folder is empty or not
            if len(os.listdir(folder)) == 0:
                # removing the file using the os.remove() method
                os.rmdir(folder)

    def move_old_pdf(self): 
        """move processed pdf to archive"""
        for pdf_file in glob.glob(join(self.batch_folder, '*.pdf')):
            shutil.move(pdf_file, self.archive_folder)
            
    def move_empty_pdf(self, filename):
        log = ColoredPrint()
        log.info('Move file %s with no barcode/qrcode to output folder' % (filename)).store()
        shutil.move(self.batch_folder + filename, self.output_folder)
        log.info('Finished moving %s to output folder' % (filename)).store()
        
        