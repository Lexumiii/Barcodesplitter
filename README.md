# Barcodescanner

The barcodescanner is working automatic once activated. start the programm with the command "python app.py" a new folder with the name "input" will apear, in which you can put a pdf that has a barcode.
The Programm will split the pdf on each barcode to create new splitted PDF's. This can be used for invoices that have been marked with barcodes to be scanned with a scanner.
Atm Warnings can happen from zbar, these can be ignored for now.


pip install shutup pyzbar.pyzbar PyPDF2 opencv-python