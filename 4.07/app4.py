
import nltk
import streamlit as st
import pandas as pd
import spacy
import pyinflect
import random     
import numpy as np

from tqdm import tqdm

from get_exercise import Get_exercise

#from googletrans import Translator


#from nltk.corpus import stopwords


nltk.download('punkt')

random.seed(42)

st.header('Генератор упражнений по английскому')
st.subheader('Вставьте текст для создания упражнения')

#text = st.text_area('nolabel', label_visibility="hidden")


with open('Little_Red_Cap_ Jacob_and_Wilhelm_Grimm.txt') as f:
    text = f.read()

text = text.replace('\n','')


text = st.text_area('Текст', text)






exercise_type = st.sidebar.selectbox('Выберите тип упражнения:', ['', 'Выберите правильную форму глагола',
                                                                   'Выбор правильного прилагательного', 'Выберите правильный артикль', 'Расставьте в правильном порядке слова предложения'], format_func=lambda x: 'Ничего не выбрано' if x == '' else x)

if exercise_type:
    st.success(exercise_type)
else:
    st.warning('Для начала выберите в боковом меню тип упражнения')







text = text.replace('"', '')
text = text.replace(',', '')
text = text.replace(':', '')
text = text.replace('-"', '')

tokens_sens = nltk.tokenize.sent_tokenize(text, language='english')

#Создаем датафрейм
df_sentences = pd.DataFrame({'sentence': tokens_sens})
df_sentences["sentence"]= df_sentences.apply(lambda x: x['sentence'].replace('.', ''), axis=1)
#st.write(df_sentences)


options = []
task = ''
answer = ''
df = pd.DataFrame({'sentence':'', 'options': options, 'answer':answer, 'task':task, 'result':[]})
nlp = spacy.load("en_core_web_sm") 

#@st.cache_data


    
get_ex = Get_exercise(df=df)

get_ex.select_exercise(df_sentences, options, task, answer, exercise_type)
 


key=0


for index, row in tqdm(df.iterrows()):
    col1, col2 = st.columns(2)
    with col1:
        st.write(str(row['sentence_hidden'])) 

    with col2:
        option = []
        for i in range(len(row['options'])):
            key+=1
            option = row['options'][i]
            random.shuffle(option)
            option = ['–––'] + option
            df['result'][index] =  st.selectbox('nolabel', option, label_visibility="hidden", key =str(key) )

            if df['result'][index] == '–––':
                pass

            elif df['result'][index] == str(row['answer'][i]):
                st.success('Это правльный ответ', icon="✅")
            
            else:
                st.error('Попробуйте еще раз', icon="😟")
    

#st.write('part 1', time.time()-start, 'seconds.')

# total_sum = sum(df['total'] for row in df.iterrows())

# if total_sum == len(df.iterrows()):
#     st.success('Успех!')
#     st.balloons()

st.write(df)    


# import streamlit as st

# tasks = [ 
#     {'sentence': 'THE BUZZ IN THE STREET _____ like the humming of flies.',
#      'options' : [['was', 'is']], 
#      'answers' : ['was'],
#      'result'  : [''],
#      'total'   : 0
#     },
    
#     {'sentence': 'Photographers _____ massed behind barriers patrolled by police, their long-snouted cameras poised, their breath rising like steam.',
#      'options' : [['stood', 'were standing']], 
#      'answers' : ['were standing'],
#      'result'  : [''],
#      'total'   : 0
#     },
    
#     {'sentence': 'Snow _____ steadily on to hats and shoulders; gloved fingers _____ lenses clear.',
#      'options' : [['fell', 'had fallen'], ['wiped','were wiping']], 
#      'answers' : ['fell', 'were wiping'],
#      'result'  : ['', ''],
#      'total'   : 0
#     },
    
#     {'sentence': 'From time to time there _____ outbreaks of desultory clicking, as the watchers _____ the waiting time by snapping the white canvas tent in the middle of the road, the entrance to the tall red-brick apartment block behind it, and the balcony on the top floor from which the body _____.',
#      'options' : [['came', 'come'], ['filled', 'had filled'], ['had fallen', 'was falling']],
#      'answers' : ['came', 'filled', 'had fallen'],
#      'result'  : ['', '', ''],
#      'total'   : 0
#     }
# ]
    
# st.header('Генератор упражнений по английскому')
# st.subheader('Вставьте текст для создания упражнения')

# st.text_area('nolabel', label_visibility="hidden")

# '---'

# st.subheader('Выберите правильные варианты пропущенных слов:')

# for task in tasks:
#     col1, col2 = st.columns(2)
#     with col1:
#         st.write('')
#         st.write(str(task['sentence']))
        
#     with col2:
#         for i in range(len(task['options'])):
#             option = task['options'][i]
#             task['result'][i] = st.selectbox('nolabel', 
#                                              ['–––'] + option, 
#                                              label_visibility="hidden")
#             if task['result'][i] == '–––':
#                 pass
#             elif task['result'][i] == task['answers'][i]:
#                 st.success('', icon="✅")
#             else:
#                 st.error('', icon="😟")
#     task['total'] = task['result'] == task['answers']    
#     '---'        

# total_sum = sum(task['total'] for task in tasks)

# if total_sum == len(tasks):
#     st.success('Успех!')
#     st.balloons()







        
       


    