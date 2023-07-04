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
    def __init__(self, df):
        self.df = df

    def select_exercise(self, df_sentences, options, task, answer, exercise_type):
        
        for sentence in df_sentences.sentence:
            for token in nlp(str(sentence)):
                if token.pos_=='VERB' and exercise_type == 'Выберите правильную форму глагола':
                    answer = [token.text for token in nlp(str(sentence)) if token.pos_=='VERB']
                    options.append(list(set([token._.inflect('VB'), token._.inflect('VBN'), token._.inflect('VBP'), token._.inflect('VBZ'), token._.inflect('VBG'), token._.inflect('VBD')])))
                    task = token.pos_
                    write_it_df=1
                elif token.pos_=='ADJ'and exercise_type == 'Выбор правильного прилагательного':
                    answer = [token.text for token in nlp(str(sentence)) if token.pos_=='ADJ']
                    options.append([token.text, token._.inflect('JJS')])
                    task = token.pos_
                    write_it_df=1
            
                elif exercise_type ==  'Расставьте в правильном порядке слова предложения'  and len(nlp(str(sentence))) < 9:
                    options = [token.text for token in nlp(str(sentence))]
                    options = [options] * len(options)
                    answer = [token.text for token in nlp(str(sentence))]
                        
                    write_it_df=1
                    task = 'order_words'
                else: pass                

            if exercise_type == 'Выберите правильный артикль':
                task = 'articles'
                answer=[]
                split_string = sentence.split(" ")
                #st.write(test_string)
                #st.write(len(test_string))
                if len(split_string) in range (3, 20):
                    st.write(len(split_string))
                for i in split_string:
                    for j in ['a', 'the', 'an']:
                        if i==j:
                            answer.append(i)
                            options.append([' a ', ' the ', ' an '])
                            break  
                answer = list(map(lambda x: ' '+ x + ' ', answer))  
                write_it_df=1     

            if len(nlp(str(sentence))) in range(3, 20) and len(answer) > 0 and write_it_df==1:                    
                self.df.loc[len(self.df)]=[sentence, options, answer, task, []]  

            # сбрасываем переменные    
            options=[]  
            write_it_df=0    
            answer=[]        

        self.df["sentence_hidden"] = self.df["sentence"]
        for index, row in tqdm(self.df.iterrows()): 
            for i in row.answer:
                if exercise_type == 'Расставьте в правильном порядке слова предложения':
                    self.df["sentence_hidden"][index] = '__________________________'
                else: self.df["sentence_hidden"][index] = self.df["sentence_hidden"][index].replace(i, ' ___ ')
    
