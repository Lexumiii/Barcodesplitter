import time
import glob
import os
import cv2
import PyPDF2
from os.path import join, basename
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode
from PyPDF2 import PdfFileWriter, PdfFileReader
from re import compile

#declaration
batch_folder = './pdf/'
image_folder = './img/'

#body
def create_page_image():
    try:
        # Create target Directory
        os.mkdir('img')
    except FileExistsError:
        pass
    
    for Pdf_file in glob.glob(join(batch_folder, '*.pdf')):
        filename = basename(Pdf_file)
        input_pdf = PdfFileReader('./pdf/' + filename)
        pagenum = 0
        pages = convert_from_path(batch_folder + filename, 500)
        
        for page in pages: 
            pagename = image_folder + filename.replace('.pdf', '') + '_' + str(pagenum) + '.png'
            pagenum += 1
            page.save(pagename, 'PNG')
            
        check_code(input_pdf, filename)
           

def check_code(input_pdf, filename):
    pagenum = 0
    found  = False
    output = PdfFileWriter()
    pdf_name = str(basename(filename)).replace('.pdf', '')
    for image in glob.glob(join(image_folder, '*.png')):
        read_image = cv2.imread(image)
        regex = compile(r'%s_(\d+)\.png' % (pdf_name))
        decode_image = decode(read_image)
        pdf = PdfFileReader(open('./pdf/' + filename,'rb'))
        pages = pdf.getNumPages()
        if(int(pagenum) <= pages):
            if decode_image: #check if qrcode is found on each page
                if decode_image[0].type == 'QRCODE' or decode_image[0].type == 'BARCODE':
                    #create new pdf and add current file
                    pagenum = regex.findall(basename(image))[0]
                    found  = True
                    print('found: ' + str(pagenum))
                    output.addPage(input_pdf.getPage(int(pagenum)))
                    with open('splitpdf' + str(pagenum) + '.pdf', 'wb') as outputStream:
                        output.write(outputStream)
            else: #if no barcode is found, add current page to previous created pdf
                pagenum = int(pagenum)
                if found:
                    pagenum += 1
                    output.addPage(input_pdf.getPage(pagenum))
                    found  = False
                    print("none: " + basename(image))
                else: 
                    output.addPage(input_pdf.getPage(pagenum))
                    pagenum += 1
 
    for f in os.listdir(image_folder):
        os.remove(os.path.join(image_folder, f))
    
        
if __name__ == '__main__':
    create_page_image()
    
    