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
import nltk
import spacy
import re
from spacy.matcher import Matcher
import pandas as pd
import numpy as np

nlp = spacy.load('en')

matcher = Matcher(nlp.vocab)

skills = pd.read_csv("one_word_skill.csv")

sklills_list = skills.skill.tolist()
def extract_email(text):
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", text)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None


def extract_phone_number(text):
    phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), text)
    
    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return '+' + number
        else:
            return number

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
    
        
        
        

def extrract_skill(text):
    for words in text.split():
        if words in sklills_list:
            print(words)
    
