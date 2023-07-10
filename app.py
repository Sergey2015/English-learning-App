
# Импортируем необходимые библиотеки
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

random.seed(42)
# page_bg_img = '''
# <style>
# .stApp {
# background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
# background-size: cover;
# }
# </style>
# '''

# st.markdown(page_bg_img, unsafe_allow_html=True)

# Загружаем модель 
nlp = spacy.load("en_core_web_sm") 

nltk.download('punkt')



st.header('Генератор упражнений по английскому')
st.subheader('Вставьте текст для создания упражнения')

# Создаем экземпляр класса
create_exercise = Create_exercise()   

# Подгружаем текст в текстовое поле
text = st.text_area('Вы можете вставить сюда любой текст', create_exercise.get_text())

# Слздаем слайдер с выбором типа упражнения
exercise_type = st.sidebar.selectbox('Выберите тип упражнения:', ['', 'Выберите правильную форму глагола',
                                                                   'Выбор правильного прилагательного', 'Выберите правильный артикль', 'Расставьте в правильном порядке слова предложения'], format_func=lambda x: 'Ничего не выбрано' if x == '' else x)
# Проверка на то, выбран ли тип упражнения
if exercise_type:
    st.success(exercise_type)
else:
    st.warning('Для начала выберите в боковом меню тип упражнения')

# Добавляем ползунок, чтобы пользователь мог выбрать количество предложений в упражнении
num_of_sentenses = st.sidebar.slider('Количество предложений', 0, 20, 5)
st.write("В заданиях будет отображаться", num_of_sentenses, 'предложений')

# Метод очистки текста
text = create_exercise.clear_text(text)

# Создание датафрейма
df = create_exercise.create_df()

# Приводим короткие формы глаголов к полной
text = create_exercise.contracted_text(text)

# Токенизация по предложениям и создание ДФ
df_sentences = create_exercise.tokenization(text)    

# Обработка упражнения и вывод итогового ДФ
df = create_exercise.select_exercise(df_sentences, exercise_type)
 
# Делаем срез ДФ с заданным пользователем количество предложений 
df = df[0:num_of_sentenses]

# Выводим контент
for index, row in df.iterrows():
    counter = 0               
    col1, col2 = st.columns(2)
    with col1:
        st.write(str(row['sentence_hidden'])) 

    with col2:
        option = []
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
            
#st.write(df)