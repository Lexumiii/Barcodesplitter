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
batchFolder = './pdf/'
imageFolder = './img/'


#body

def createPageImage():
    try:
        # Create target Directory
        os.mkdir('img')
    except FileExistsError:
        pass
    
    for PDFfile in glob.glob(join(batchFolder, '*.pdf')):
        filename = basename(PDFfile)
        inputPDF = PdfFileReader('./pdf/' + filename)
        pagenum = 0
        pages = convert_from_path(batchFolder + filename, 500)
        
        for page in pages: 
            pagename = imageFolder + filename.replace('.pdf', '') + '_' + str(pagenum) + '.png'
            pagenum += 1
            page.save(pagename, 'PNG')
            
        checkCode(inputPDF, filename)
    return True
           

def checkCode(inputPDF, filename):
    pagenum = 0
    test = False
    output = PdfFileWriter()
    for image in glob.glob(join(imageFolder, '*.png')):
        readImage = cv2.imread(image)
        regex = compile(r'X_(\d+)\.png')
        decodeImage = decode(readImage)
        pdf = PdfFileReader(open('./pdf/' + filename,'rb'))
        pages = pdf.getNumPages()
        if(int(pagenum) <= pages):
            if decodeImage:
                if decodeImage[0].type == 'QRCODE':
                    #create new pdf and add current file
                    pagenum = regex.findall(basename(image))[0]
                    test = True
                    print('found: ' + str(pagenum))
                    #create
                    output.addPage(inputPDF.getPage(int(pagenum)))
                    with open('splitpdf' + str(pagenum) + '.pdf', 'wb') as outputStream:
                        output.write(outputStream)
            else:
                #add page to pdf
                pagenum = int(pagenum)
                if test == False:
                    output.addPage(inputPDF.getPage(pagenum))
                    pagenum += 1
                if test: 
                    pagenum += 1
                    output.addPage(inputPDF.getPage(pagenum))
                    test = False
                    print("none: " + basename(image))
 
    for f in os.listdir(imageFolder):
        os.remove(os.path.join(imageFolder, f))
    

            
if __name__ == '__main__':
    finished = False
    finished = createPageImage()
    while finished != True:
        time.sleep(1)
    
    