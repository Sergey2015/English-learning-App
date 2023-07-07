import nltk
import streamlit as st
import pandas as pd
import spacy
import pyinflect
import random     
import numpy as np
import contractions
from ast import literal_eval

nlp = spacy.load("en_core_web_sm") 

# Главный класс приложения
class Create_exercise:
    def __init__(self, task='', answer=''):
        #self.df = df
        #self.options=options
        self.task = task
        self.answer = answer
        #self.exercise_type = exercise_type
        

 # Загрузка текста 
    #@st.cache_data
    def get_text(self):
        with open('Little_Red_Cap_ Jacob_and_Wilhelm_Grimm.txt') as f:
            self.text = f.read()
            self.text = self.text.replace('\n','')
            return self.text
        
# Приводим короткие формы глаголов к полной
    def contracted_text(self, text): 
        expanded_words = []   
        for word in text.split():
            expanded_words.append(contractions.fix(word))  
        expanded_text = ' '.join(expanded_words)    
        return expanded_text
        
# Очистка текста        
   # @st.cache_data
    def clear_text(self, text):
        self.text = self.text.lower()
        self.text = self.text.replace('"', '')
        self.text = self.text.replace(',', '')
        self.text = self.text.replace(':', '')
        self.text = self.text.replace('-"', '')
        return self.text

    #st.cache_data
    def create_df(self):
        self.df = pd.DataFrame(columns=['sentence', 'options', 'answer', 'task', 'result'])
        # self.text = text
        # tokens_sens = nltk.tokenize.sent_tokenize(self.text, language='english')
        # df_sentences = pd.DataFrame({'sentence': tokens_sens})
        # df_sentences["sentence"]= df_sentences.apply(lambda x: x['sentence'].replace('.', ''), axis=1)
        return self.df

# Токенизация по предложениям и создание ДФ
    #@st.cache_data
    def tokenization(self, text):
        self.text=text
        self.tokens_sens = nltk.tokenize.sent_tokenize(self.text, language='english')
        self.df_sentences = pd.DataFrame({'sentence': self.tokens_sens})
        self.df_sentences["sentence"]= self.df_sentences.apply(lambda x: x['sentence'].replace('.', ''), axis=1)    
        return self.df_sentences

# Обработка упражнения и вывод итогового ДФ
    #@st.cache_data
    def select_exercise(self, df_sentences, exercise_type):
        options = []
        try:
            if exercise_type == 'Выберите правильную форму глагола':
                self.df = pd.read_csv('df_VERB.csv', converters={'options': literal_eval, 'answer': literal_eval})
            elif exercise_type == 'Выбор правильного прилагательного':
                self.df = pd.read_csv('df_ADJ.csv', converters={'options': literal_eval, 'answer': literal_eval})
            elif exercise_type == 'Расставьте в правильном порядке слова предложения':
                self.df = pd.read_csv('df_ORDER.csv', converters={'options': literal_eval, 'answer': literal_eval})   
            elif exercise_type == 'Выберите правильный артикль':
                self.df = pd.read_csv('df_ARTICLES.csv', converters={'options': literal_eval, 'answer': literal_eval})      
            # self.df.drop(columns=['result'], axis=1, inplace=True)
            # self.df.options = self.df.options.astype(list)
            st.write('Загружен датасет')
            return self.df
        except:
            st.write('Создан датасет')
            for sentence in df_sentences.sentence:
                for token in nlp(str(sentence)):
                    if token.pos_=='VERB' and exercise_type == 'Выберите правильную форму глагола':  
                        dataset = 'df_VERB.csv'                  
                        self.answer = [token.text for token in nlp(str(sentence)) if token.pos_=='VERB']
                        options.append(list(set([token._.inflect('VB'), token._.inflect('VBN'), token._.inflect('VBP'), token._.inflect('VBZ'), token._.inflect('VBG'), token._.inflect('VBD')])))
                        self.task = token.pos_
                        write_it_df=1
                    elif token.pos_=='ADJ'and exercise_type == 'Выбор правильного прилагательного':
                        dataset = 'df_ADJ.csv'  
                        self.answer = [token.text for token in nlp(str(sentence)) if token.pos_=='ADJ']
                        options.append([token.text, token._.inflect('JJS')])
                        self.task = token.pos_
                        write_it_df=1
                
                    elif exercise_type ==  'Расставьте в правильном порядке слова предложения'  and len(nlp(str(sentence))) < 9:
                        dataset = 'df_ORDER.csv'  
                        options = [token.text for token in nlp(str(sentence))]
                        options = [options] * len(options)
                        self.answer = [token.text for token in nlp(str(sentence))]
                            
                        write_it_df=1
                        self.task = 'order_words'
                    else: pass                

                if exercise_type == 'Выберите правильный артикль':
                    dataset = 'df_ARTICLES.csv'  
                    self.task = 'articles'
                    self.answer=[]
                    split_string = sentence.split(" ")
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
            for index, row in self.df.iterrows(): 
                for i in row.answer:
                    if exercise_type == 'Расставьте в правильном порядке слова предложения':
                        self.df["sentence_hidden"][index] =  '__ ' * len(row.answer)
                    else: self.df["sentence_hidden"][index] = self.df["sentence_hidden"][index].replace(i, ' ___ ')
            #filename = f'df_{self.task}.csv'
            self.df.to_csv(dataset, index=False)        
                        
            return self.df
    
    
