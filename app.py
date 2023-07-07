


import nltk
import streamlit as st
import pandas as pd
import spacy
import pyinflect
import random     
import numpy as np
import contractions
from ast import literal_eval

from create_exercise import Create_exercise


# page_bg_img = '''
# <style>
# .stApp {
# background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
# background-size: cover;
# }
# </style>
# '''

# st.markdown(page_bg_img, unsafe_allow_html=True)

# st.markdown(
#     """
#     <style>
#     .reportview-container {
#         background: url("https://images.app.goo.gl/LFCobouKtT7oZ7Qv7")
#     }
#    .sidebar .sidebar-content {
#         background: url("https://images.app.goo.gl/LFCobouKtT7oZ7Qv7")
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )


nlp = spacy.load("en_core_web_sm") 

nltk.download('punkt')

random.seed(42)

st.header('Генератор упражнений по английскому')
st.subheader('Вставьте текст для создания упражнения')

create_exercise = Create_exercise()   

text = st.text_area('Текст', create_exercise.get_text())


exercise_type = st.sidebar.selectbox('Выберите тип упражнения:', ['', 'Выберите правильную форму глагола',
                                                                   'Выбор правильного прилагательного', 'Выберите правильный артикль', 'Расставьте в правильном порядке слова предложения'], format_func=lambda x: 'Ничего не выбрано' if x == '' else x)

if exercise_type:
    st.success(exercise_type)
else:
    st.warning('Для начала выберите в боковом меню тип упражнения')


num_of_sentenses = st.sidebar.slider('Количество предложений', 0, 20, 5)
st.write("В заданиях будет отображаться", num_of_sentenses, 'предложений')

text = create_exercise.clear_text(text)



df = create_exercise.create_df()


#@st.cache_data

text = create_exercise.contracted_text(text)

df_sentences = create_exercise.tokenization(text)    

df = create_exercise.select_exercise(df_sentences, exercise_type)
 


#key=0

df = df[0:num_of_sentenses]

for index, row in df.iterrows():
    counter = 0               
    col1, col2 = st.columns(2)
    with col1:
        st.write(str(row['sentence_hidden'])) 

    with col2:
        option = []
        #st.write(len(row['options']))
        #st.write(key+1)
        for i in range(len(row['options'])):
            #key+=1
            option = row['options'][i]
            random.shuffle(option)
            option = ['–––'] + option
            df['result'][index] =  st.selectbox('nolabel', option, label_visibility="hidden", key = str(random.random())) #str(key)

            if df['result'][index] == '–––':
                pass

            elif df['result'][index] == str(row['answer'][i]):
                st.success('Это правльный ответ', icon="✅")
                counter += 1
                if counter == len(row['options']):
                    st.success(df['sentence'][index])
            
            else:
                st.error('Попробуйте еще раз', icon="😟")
            
    st.write('----------------------')   

# df["result"] = np.nan
# for index, row in df.iterrows():
#     counter = 0               
#     col1, col2 = st.columns(2)
#     with col1:
#         st.write(str(row['sentence_hidden'])) 

#     with col2:
#         option = []
#         #st.write(len(row['options']))
#         #st.write(key+1)
#         for i in range(len(row['options'])):
#             st.write('длина row_options',len(row['options']))
#             #key+=1
#             option = row['options'][i]
#             st.write(option)
#             random.shuffle(option)
#             option = ['–––'] + option
#             st.write(option)
#             # Выбранный ответ пользователя
#             df['result'][index] =  st.selectbox('nolabel', option, label_visibility="hidden", key = str(random.random())) #str(key)

#             if df['result'][index] == '–––':
#                 pass

#             elif df['result'][index] == str(row['answer'][i]):
#                 st.write(df['result'][index])
#                 st.write(str(row['answer'][i]))
#                 st.success('Это правльный ответ', icon="✅")
#                 counter += 1
#                 if counter == len(row['options']):
#                     #st.success(df['sentence'][index])
#                     current_sent = df['sentence'][index]                    
#                     st.markdown(f':green[{current_sent}]', unsafe_allow_html=True)
            
#             else:
#                 st.error('Попробуйте еще раз', icon="😟")
#                 st.write(df['result'][index])
#                 st.write('row_answer[i]', row['answer'])
#                 st.write(str(row['answer'][index]))
#                 st.write(df['answer'][i])
            
#     st.write('----------------------')    
            
st.write(df)
    


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







        
       


    