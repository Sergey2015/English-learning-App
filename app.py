
import nltk
import streamlit as st
import pandas as pd
import spacy
import pyinflect
import random     
import numpy as np

from nltk.corpus import stopwords


nltk.download('punkt')


random.seed(4)

st.header('Генератор упражнений по английскому')
st.subheader('Вставьте текст для создания упражнения')

#text = st.text_area('nolabel', label_visibility="hidden")


with open('Little_Red_Cap_ Jacob_and_Wilhelm_Grimm.txt') as f:
    text = f.read()

text = text.replace('\n','')


text = st.text_area('Текст', text)






exercise_type = st.sidebar.selectbox('Выберите тип упражнения:', ['', 'Выберите правильную форму глагола',
                                                                   'Выбор правильного прилагательного', 'Выберите правильный артикль', 'Расставьте в правильном порядке слова предложения', 'Заполните пропуск'], format_func=lambda x: 'Ничего не выбрано' if x == '' else x)

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
nlp = spacy.load("en_core_web_sm") # изменение формы глагола с помощью pyinflect
for sentence in df_sentences.sentence:
        #st.write(sentence)
    for token in nlp(str(sentence)):
        #st.write(token)
        if token.pos_=='VERB' and exercise_type == 'Выберите правильную форму глагола':
            answer = [token.text for token in nlp(str(sentence)) if token.pos_=='VERB']
            options.append(list(set([token._.inflect('VB'), token._.inflect('VBN'), token._.inflect('VBP'), token._.inflect('VBZ'), token._.inflect('VBG'), token._.inflect('VBD')])))
            task = token.pos_
            write_it_df=1

        elif token.pos_=='ADJ'and exercise_type == 'Выбор правильного прилагательного':
            answer = [token.text for token in nlp(str(sentence)) if token.pos_=='ADJ']
            options.append([token.text, token._.inflect('JJS')])
            #st.write(options)
            task = token.pos_
            write_it_df=1
            #st.write('правильно')
        # elif str(token) == 'a' and exercise_type == 'Выберите правильный артикль':
        #     options = ['a', 'the', 'an']
        #     answer = token
        #     #task ='article'
        elif exercise_type ==  'Расставьте в правильном порядке слова предложения'  and len(nlp(str(sentence))) < 9:
            
            options = [token.text for token in nlp(str(sentence))]
            #options = random.sample(options, len(options))
            options = [options] * len(options)
            answer = [token.text for token in nlp(str(sentence))]
            
            write_it_df=1
            task = 'order_words'

        else: pass

    if exercise_type == 'Выберите правильный артикль':
        task = 'articles'
        answer=[]
        test_string = sentence.split(" ")
        #st.write(test_string)
        for i in test_string:
            for j in ['a', 'the', 'an']:
                if i==j:
                    answer.append(i)
                    options.append([' a ', ' the ', ' an '])
                    break  
        answer = list(map(lambda x: ' '+ x + ' ', answer))  
        write_it_df=1      
        #st.write(answer)
# # отобрать предложения, где есть глагол или прилагательное
        #st.write(options)


    if len(nlp(str(sentence))) in range(3, 20) and len(answer) > 0 and write_it_df==1:    
              
        df.loc[len(df)]=[sentence, options, answer, task, []]  
    options=[]  
    write_it_df=0    
    answer=[]
        #answer=[]
    



if exercise_type == 'Заполните пропуск':

    st.subheader('Выберите правильные варианты пропущенных слов:')

df["sentence_hidden"] = df["sentence"]
for index, row in df.iterrows(): 
    for i in row.answer:
        if exercise_type == 'Расставьте в правильном порядке слова предложения':
            df["sentence_hidden"][index] = '__________________________'
        else: df["sentence_hidden"][index] = df["sentence_hidden"][index].replace(i, ' ___ ')
#df["sentence_hidden"]= df.apply(lambda x: x['sentence'].replace(str(x['answer']), ' ___ '), axis=1)
#df["sentence_hidden"]= df.apply(lambda x: x['sentence'].replace(str(any(['Little', 'Cap'])), ' ___ '), axis=1)


key=0

for index, row in df.iterrows():
    col1, col2 = st.columns(2)
    with col1:
        st.write('')
        st.write(str(row['sentence_hidden'])) 
    with col2:
        option = []
        for i in range(len(row['options'])):
            key+=1
            option = row['options'][i]

            #option = random.sample(option, len(option))
            #np.random.shuffle(option)
            random.shuffle(option)
            # for i in range(len(option)):
            option = ['–––'] + option
            #st.write(len(option))
            #st.write(option)
            #     print(i)
            #     option[i] = ['–––'] + i

            option = ['–––'] + option
        #option = random.sample(option, len(option))
            df['result'][index] =  st.selectbox('nolabel', option, label_visibility="hidden", key =str(key) )
            st.write(df['result'][index])

            if df['result'][index] == '–––':
                pass

            elif df['result'][index] == str(row['answer'][i]):
                st.success('Это правльный ответ', icon="✅")
            
            else:
                st.error('Попробуйте еще раз', icon="😟")
    



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







        
       


    