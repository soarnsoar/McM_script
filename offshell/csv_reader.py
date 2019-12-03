import os
import csv

KEY='1bAdzoB9bg6nbyxCOBsTAWSSJy6FHNfmkrIDqY-Nmdi0'
sheet="Sheet1"
cell_range="A2:M2"
download_url='"https://docs.google.com/spreadsheets/d/'+KEY+'/gviz/tq?tqx=out:csv&sheet='+sheet+'&range='+cell_range+'"'
filename='temp.txt'
os.system('wget -q -O '+filename+" "+download_url)

with open('temp.txt') as f:
#f=open('temp.txt')
    reader = csv.reader(f)
    for row in reader:
        for element in row:
            print element
    
    f.close()
