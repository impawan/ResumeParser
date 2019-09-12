# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 10:51:12 2019

@author: paprasad
"""


from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage,PDFTextExtractionNotAllowed
import io
#import nltk
import spacy
from spacy.matcher import Matcher

nlp = spacy.load('en')

matcher = Matcher(nlp.vocab)

def extract_name(resume_text):
    nlp_text = nlp(resume_text)
    
    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    
    matcher.add('NAME', None, pattern)
    
    matches = matcher(nlp_text)
    for match_id, start, end in matches:
        span = nlp_text[start:end]
    return span.text

        
def extract_text(pdfFile):
	fp = open(pdfFile, 'rb')
	filhandler = io.StringIO()
	laparams = LAParams() 
	resManger = PDFResourceManager()
	device = TextConverter(resManger,filhandler,codec ='utf-8',laparams = laparams )
	interpreter = PDFPageInterpreter(resManger,device)
	
	for page in PDFPage.get_pages(fp,caching=True):
		interpreter.process_page(page)
	fp.close()
	device.close()
	text = filhandler.getvalue()
	filhandler.close()
	return text
            
        
def text_cleaning(text):
    text = text.replace("\n"," ")
    return text 
    
        
        
        


