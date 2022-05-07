from os import path
from random import randint
import json
import shutil
import glob
import asyncio
import os
import cv2
import warnings
from os.path import join, basename
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode
from PyPDF2 import PdfFileWriter, PdfFileReader
from datetime import date
from re import compile
from progress.bar import Bar
from PIL import Image
from pyzbar.pyzbar import ZBarSymbol

class FileListener():
    def __init__(self):

        # read config json file
        with open('./config.json', 'r') as f:
            self.data = json.load(f)

        # global declaration
        self.base_path = self.data["folderPath"]
        print(self.base_path)
        self.batch_folder = './input/'
        self.image_folder = './img/'
        self.output_folder = './output/'
        self.archive_folder = './archiv/'

    async def create_page_image(self):
        """
        Convert pages to images and decode them, create new pdfs based on barcodes
        """
        
        # loop over every pdf in folder
        for pdf_file in glob.glob(join(self.batch_folder, '*.pdf')):
            
            try:
            # Create target Directory
                os.mkdir('img')
                os.mkdir('output')
            except FileExistsError:
                pass
            
            filename = basename(pdf_file)
            # create pdf reader
            input_pdf = PdfFileReader(self.batch_folder + filename)
            print(f'Started Processing: {filename}')
            pagenum = 0
            pages = convert_from_path(self.batch_folder + filename, 500)
            # save pages as png
            for page in pages:
                pagename = self.image_folder + \
                    filename.replace('.pdf', '') + '_' + str(pagenum) + '.png'
                pagenum += 1
                page.save(pagename, 'PNG')

            await self.check_code(input_pdf, filename)
            print(f'Finished processing: {filename}')
        return True

    async def check_code(self, input_pdf, filename):
        pagenum = 0
        pdfnum = 0
        output = ""
        # get name of pdf
        pdf_name = str(basename(filename)).replace('.pdf', '')

        # get current date(day, month, year)
        today = date.today()
        current_date = today.strftime("%d/%m/%Y")
        current_date = current_date.split('/')
        day = current_date[0]
        month = current_date[1]
        year = current_date[2]

        # decode images and create new pdfs
        for image in glob.glob(join(self.image_folder, '*.png')):
            read_image = cv2.imread(image)
            regex = compile(r'%s_(\d+)\.png' % (pdf_name))
            # ignore warnings
            warnings.filterwarnings('ignore')
            decode_image = decode(Image.open(image), symbols=[ZBarSymbol.QRCODE])
            if decode_image:  # check if qrcode is found on each page
                if decode_image[0].type != "":
                    if output:
                        found = False
                        with open(self.output_folder + year + month + day + '_' + str(filename).replace('.pdf', '') + str(pdfnum) + '.pdf', 'wb') as output_stream:
                            output.write(output_stream)
                            pdfnum += 1
                    output = PdfFileWriter()
                    # create new pdf and add current file
                    pagenum = regex.findall(basename(image))[0]
                    found = True
                    output.addPage(input_pdf.getPage(int(pagenum)))
            else:  # if no barcode is found, add current page to previous created pdf
                pagenum = int(pagenum)
                if found:
                    pagenum += 1
                    output.addPage(input_pdf.getPage(pagenum))
                else:
                    output.addPage(input_pdf.getPage(pagenum))
                    pagenum += 1
        if output:
            with open(self.output_folder + year + month + day + '_' + str(filename).replace('.pdf', '') + str(pdfnum) + '.pdf', 'wb') as output_stream:
                output.write(output_stream)
                pdfnum += 1

        # remove images
        for f in os.listdir(self.image_folder):
            os.remove(os.path.join(self.image_folder, f))

        # remove image folder
        if os.path.exists('img'):
            # checking whether the folder is empty or not
            if len(os.listdir('img')) == 0:
                # removing the file using the os.remove() method
                os.rmdir('img')
        return True

    async def move_old_pdf(self):
        """move processed pdf to archive"""
        for pdf_file in glob.glob(join(self.batch_folder, '*.pdf')):
            shutil.move(pdf_file, self.archive_folder)

    async def rename_pdf(self):
         # loop over every pdf in folder
        for pdf_file in glob.glob(join(self.batch_folder, '*.pdf')):
            
            # get filename
            filename = self.batch_folder + basename(pdf_file)
            
            # check if filename contains space
            if filename.endswith('.pdf') and " " in filename:
                # replace space with _
                os.rename(filename, filename.replace(" ", "_"))
            pass
        
    def start(self):
        try:
            # Create target Directory
            os.mkdir('input')
            os.mkdir('archiv')
        except FileExistsError:
            pass

        while len(os.listdir(self.batch_folder)) == 0:
            pass
        else:
            asyncio.run(self.rename_pdf())
            asyncio.run(self.create_page_image())
            asyncio.run(self.move_old_pdf())
            self.start()


if __name__ == '__main__':
    fl = FileListener()
    fl.start()
