import nltk
import streamlit as st
import pandas as pd
import spacy
import pyinflect
import random     
import numpy as np

from tqdm import tqdm

nlp = spacy.load("en_core_web_sm") 

class Get_exercise:
    def __init__(self, df, task='', answer='', exercise_type='Ничего не выбрано'):
        self.df = df
        #self.options=options
        self.task = task
        self.answer = answer
        self.exercise_type = exercise_type

    def select_exercise(self, df_sentences, options):

        for sentence in df_sentences.sentence:
            for token in nlp(str(sentence)):
                if token.pos_=='VERB' and self.exercise_type == 'Выберите правильную форму глагола':
                    self.answer = [token.text for token in nlp(str(sentence)) if token.pos_=='VERB']
                    options.append(list(set([token._.inflect('VB'), token._.inflect('VBN'), token._.inflect('VBP'), token._.inflect('VBZ'), token._.inflect('VBG'), token._.inflect('VBD')])))
                    self.task = token.pos_
                    write_it_df=1
                elif token.pos_=='ADJ'and self.exercise_type == 'Выбор правильного прилагательного':
                    self.answer = [token.text for token in nlp(str(sentence)) if token.pos_=='ADJ']
                    options.append([token.text, token._.inflect('JJS')])
                    self.task = token.pos_
                    write_it_df=1
            
                elif self.exercise_type ==  'Расставьте в правильном порядке слова предложения'  and len(nlp(str(sentence))) < 9:
                    options = [token.text for token in nlp(str(sentence))]
                    options = [options] * len(options)
                    self.answer = [token.text for token in nlp(str(sentence))]
                        
                    write_it_df=1
                    self.task = 'order_words'
                else: pass                

            if self.exercise_type == 'Выберите правильный артикль':
                self.task = 'articles'
                self.answer=[]
                split_string = sentence.split(" ")
                #st.write(test_string)
                #st.write(len(test_string))
                if len(split_string) in range (3, 20):
                    st.write(len(split_string))
                for i in split_string:
                    for j in ['a', 'the', 'an']:
                        if i==j:
                            self.answer.append(i)
                            options.append([' a ', ' the ', ' an '])
                            break  
                self.answer = list(map(lambda x: ' '+ x + ' ', self.answer))  
                write_it_df=1     

            if len(nlp(str(sentence))) in range(3, 20) and len(self.answer) > 0 and write_it_df==1:                    
                self.df.loc[len(self.df)]=[sentence, options, self.answer, self.task, []]  

            # сбрасываем переменные    
            options=[]  
            write_it_df=0    
            self.answer=[]        

        self.df["sentence_hidden"] = self.df["sentence"]
        for index, row in tqdm(self.df.iterrows()): 
            for i in row.answer:
                if self.exercise_type == 'Расставьте в правильном порядке слова предложения':
                    self.df["sentence_hidden"][index] = '__________________________'
                else: self.df["sentence_hidden"][index] = self.df["sentence_hidden"][index].replace(i, ' ___ ')
        return self.df
    
