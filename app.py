import shutil
import glob
import asyncio
import os
import cv2
import shutup
import warnings
from os.path import join, basename
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode
from PyPDF2 import PdfFileWriter, PdfFileReader
from datetime import date
from re import compile


# supress warnings
shutup.please()


# global declaration
batch_folder = './input/'
image_folder = './img/'
output_folder = './output/'
archive_folder = './archiv/'

async def create_page_image():
    """
    Convert pages to images and decode them, create new pdfs based on barcodes
    """
    try:
        # Create target Directory
        os.mkdir('img')
        os.mkdir('output')
    except FileExistsError:
        pass
    # loop over every pdf in folder
    for pdf_file in glob.glob(join(batch_folder, '*.pdf')):
        filename = basename(pdf_file)
        print('PDF found, processing: ' + filename)
        # create pdf reader
        input_pdf = PdfFileReader(batch_folder + filename)
        pagenum = 0
        pages = convert_from_path(batch_folder + filename, 500)
        # save pages as png
        for page in pages: 
            pagename = image_folder + filename.replace('.pdf', '') + '_' + str(pagenum) + '.png'
            pagenum += 1
            page.save(pagename, 'PNG')
            
        await check_code(input_pdf, filename)
        print('Finished processing: ' + filename)
    return True
           

async def check_code(input_pdf, filename):
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
    for image in glob.glob(join(image_folder, '*.png')):
        read_image = cv2.imread(image)
        regex = compile(r'%s_(\d+)\.png' % (pdf_name))
        # ignore warnings
        warnings.filterwarnings('ignore')
        decode_image = decode(read_image)
        if decode_image: #check if qrcode is found on each page
            if decode_image[0].type != "":
                if output:
                    found  = False
                    with open(output_folder + year + month + day + '_' + str(filename).replace('.pdf', '') + str(pdfnum) + '.pdf', 'wb') as output_stream:
                        output.write(output_stream)
                        pdfnum += 1
                output = PdfFileWriter()
                #create new pdf and add current file
                pagenum = regex.findall(basename(image))[0]
                found  = True 
                output.addPage(input_pdf.getPage(int(pagenum)))
        else: #if no barcode is found, add current page to previous created pdf                
            pagenum = int(pagenum)
            if found:
                pagenum += 1
                output.addPage(input_pdf.getPage(pagenum))
            else: 
                output.addPage(input_pdf.getPage(pagenum))
                pagenum += 1
    if output:
        with open(output_folder + year + month + day + '_' + str(filename).replace('.pdf', '') + str(pdfnum) + '.pdf', 'wb') as output_stream:
            output.write(output_stream)
            pdfnum += 1
 
    # remove images
    for f in os.listdir(image_folder):
        os.remove(os.path.join(image_folder, f))
    
    #remove image folder
    if os.path.exists('img'):
        # checking whether the folder is empty or not
        if len(os.listdir('img')) == 0:
            # removing the file using the os.remove() method
            os.rmdir('img')
    return True

async def move_old_pdf(): 
    """move processed pdf to archive"""
    for pdf_file in glob.glob(join(batch_folder, '*.pdf')):
        shutil.move(pdf_file, archive_folder)
    
    
def main():
    try:
        # Create target Directory
        os.mkdir('input')
        os.mkdir('archiv')
    except FileExistsError:
        pass

    while len(os.listdir(batch_folder)) == 0:
        pass
    else:
        asyncio.run(create_page_image())
        asyncio.run(move_old_pdf())
        main()
        
if __name__ == '__main__':
    main()
    