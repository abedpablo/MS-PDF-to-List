# -*- coding: utf-8 -*-
import PyPDF2
import os
import re
import pandas as pd

# Set working directory
directory = 'C:\\INPUT_FOLDER'

#Create Lists for dataframe
s_lens = []
mass = []
names = []
CEs = []

for file in os.listdir(directory):
    if not file.endswith(".pdf"): 
        continue
    with open(os.path.join(directory,file), 'rb') as pdfFileObj:
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        page = pdfReader.getPage(0)
        page_content = page.extractText().encode('utf-8') #Convert text to numerical values
        page_lines = re.split(r'\d{2}:\d{2}:\d{2}:', page_content)
        text = "\n".join(page_lines)

        s_lens.append(re.findall(r'New Setting = (\w+.{3}[0-9])', text)) #search for s-lens values and make list(the output will be blank if no new setting was obtained)
        mass.append(re.findall(r'New Parent Mass: (\w+.{3}[0-9])', text)) #search and get new Parent mass to 3 decimal places and make list
        names.append(file) #Get compound names in list (This is provided by the user when they save the file on the mass spectrometer)
        rest = text.split('(v)', 1)[1].split('Finish', 1)[0].split() #Isolate the product m/z and collision energies
        df_CE = pd.DataFrame([rest], columns = ['Mass1', 'CE1', 'Mass2', 'CE2', 'Mass3', 'CE3', 'Mass4', 'CE4', 'Mass5', 'CE5', 'Mass6', 'CE6', 'Mass7', 'CE7', 'Mass8', 'CE8']) #convert to dataframe
        CEs.append(df_CE)

#Create Products and collision energy, RF lens, Parent m/z, and filename dataframe
df_CE = pd.concat(CEs)
df = pd.DataFrame({'RF':s_lens, 'Parent m/z':mass, 'Filename':names})
df['Parent m/z'] = df['Parent m/z'].map(lambda x: str(x)[:-2]).map(lambda x: str(x)[2:])
df['RF'] = df['RF'].map(lambda x: str(x)[:-2]).map(lambda x: str(x)[2:])
df1 = pd.concat([df.reset_index(drop=True), df_CE.reset_index(drop=True)], axis=1)

df1.to_csv('C:\\OUTPUTFILE\\Infusion.csv')