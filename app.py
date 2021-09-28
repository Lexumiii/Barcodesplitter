import glob
import asyncio
import os
import cv2
import warnings
import configparser
from os.path import join, basename
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode    
from PyPDF2 import PdfFileWriter, PdfFileReader
from re import compile
from utility import ColoredPrint, CalcTime, DirHandler
from configGUI import CreateGui

# install colored logging
log = ColoredPrint()


# load config
config = configparser.ConfigParser()
config.read("./config.ini")


# global declaration
batch_folder = config.get('Folders', 'batch_folder')
image_folder = config.get('Folders', 'image_folder')
output_folder = config.get('Folders', 'output_folder')
archive_folder = config.get('Folders', 'archive_folder')
mimetype_pdf = config.get('Folders', 'mimetype_pdf')
mimetype_img = config.get('Folders', 'mimetype_img')

# get current date(day, month, year)
time = CalcTime()
time = time.calc_time()

# dir handler
dir = DirHandler()

async def create_page_image():
    """Convert pages to images and decode them, create new pdfs based on barcodes"""
    # loop over every pdf in folder
    for pdf_file in glob.glob(join(batch_folder, '*.pdf')):
        filename = basename(pdf_file)
        log.success('PDF found, processing: ' + filename).store()

        # create pdf reader
        input_pdf = PdfFileReader(batch_folder + filename)
        pagenum = 0
        pages = convert_from_path(batch_folder + filename, 500)
        # save pages as png
        for page in pages: 
            pagename = image_folder + filename.replace(mimetype_pdf, '') + '_' + str(pagenum) + mimetype_img
            pagenum += 1
            page.save(pagename, 'PNG')
            
        check = await check_code(input_pdf, filename)
        if check: 
            log.success('Finished processing: ' + filename).store()
        else: 
            log.warn('There was no Barcode/Qrcode in the Pdf: ' + filename)
            dir.move_empty_pdf(filename)
    return True
           

async def check_code(input_pdf, filename):
    pagenum = 0
    pdfnum = 0
    output = ""
    code_check = False
    found = False
    create = True
    # get name of pdf
    pdf_name = str(basename(filename)).replace(mimetype_pdf, '')
    
    # decode images and create new pdfs
    for image in glob.glob(join(image_folder, '*.png')):
        
        create_message = 'Created file: ' + time['year'] + time['month'] + time['day'] + '_' + str(filename).replace(mimetype_pdf, '') + str(pdfnum) + mimetype_pdf + ' -- ' + time['year'] + '-' + time['month'] + '-' + time['day'] + ' ' + time['hour'] + ':' + time['minute'] + ':' + time['second']
        read_image = cv2.imread(image)
        regex = compile(r'%s_(\d+)\.png' % (pdf_name))
        # ignore warnings
        warnings.filterwarnings('ignore')

        decode_image = decode(read_image)
        # check if qrcode is found on each page
        if decode_image: 
            if decode_image[0].type != "":
                code_check = True
                create = False
                if output:
                    found  = False
                    with open(output_folder + time['year'] + time['month'] + time['day'] + '_' + str(filename).replace(mimetype_pdf, '') + "_" + str(pdfnum) + mimetype_pdf, 'wb') as output_stream:
                        output.write(output_stream)
                        log.write(create_message).store()
                        pdfnum += 1
                output = PdfFileWriter()
                # create new pdf and add current file
                pagenum = regex.findall(basename(image))[0]
                found  = True 
                output.addPage(input_pdf.getPage(int(pagenum)))
        else:
            # if no barcode is found, add current page to previous created pdf       
            if create:
                # remove images
                dir.remove_images()
                return code_check    
            pagenum = int(pagenum)
            if found:
                pagenum += 1
                output.addPage(input_pdf.getPage(pagenum))
            else: 
                output.addPage(input_pdf.getPage(pagenum))
                pagenum += 1
    if output:
        with open(output_folder + time['year'] + time['month'] + time['day'] + '_' + str(filename).replace(mimetype_pdf, '') + str(pdfnum) + mimetype_pdf, 'wb') as output_stream:
            output.write(output_stream)
            log.write(create_message).store()
            pdfnum += 1
 
    # remove images
    dir.remove_images()
    
    # remove image folder
    dir.remove_folder('img')
    return code_check


def main():
    # Create target Directory
    dir.make_dir('input')
    dir.make_dir('archiv')
    dir.make_dir('img')
    dir.make_dir('output')
    while len(os.listdir(batch_folder)) == 0:
        pass
    else:
        asyncio.run(create_page_image())
        dir.move_old_pdf()
        main()
        
if __name__ == '__main__':
    main()
    