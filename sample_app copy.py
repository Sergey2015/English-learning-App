
import nltk
import streamlit as st
import pandas as pd
import spacy
import pyinflect
import random     

from nltk.corpus import stopwords


nltk.download('punkt')




st.header('Генератор упражнений по английскому')
st.subheader('Вставьте текст для создания упражнения')

text2 = st.text_area('nolabel', label_visibility="hidden")













exercise_type = st.sidebar.selectbox('Выберите тип упражнения:', ['', 'Выберите правильную форму глагола',
                                                                   'Выбор правильного прилагательного', 'Выберите правильный артикль', 'Выберите слово', 'Заполните пропуск'], format_func=lambda x: 'Ничего не выбрано' if x == '' else x)

if exercise_type:
    st.success('Ура! Вы выбрали тип упражнения 🎉')
    st.write("Вы выбрали упражнение: ", exercise_type)
else:
    st.warning('Ничего не выбрано')



import streamlit as st
text2 = st.text_area('Text to analyze', '''
Little Red Cap

Jacob and Wilhelm Grimm

Once upon a time there was a sweet little girl. Everyone who saw her liked her, but most of all her grandmother, who did not know what to give the child next. Once she gave her a little cap made of red velvet. Because it suited her so well, and she wanted to wear it all the time, she came to be known as Little Red Cap.
One day her mother said to her, "Come Little Red Cap. Here is a piece of cake and a bottle of wine. Take them to your grandmother. She is sick and weak, and they will do her well. Mind your manners and give her my greetings. Behave yourself on the way, and do not leave the path, or you might fall down and break the glass, and then there will be nothing for your sick grandmother."

Little Red Cap promised to obey her mother. The grandmother lived out in the woods, a half hour from the village. When Little Red Cap entered the woods a wolf came up to her. She did not know what a wicked animal he was, and was not afraid of him.

"Good day to you, Little Red Cap."

"Thank you, wolf."

"Where are you going so early, Little Red Cap?"

"To grandmother's."

    ''')




tokens_sens = nltk.tokenize.sent_tokenize(text2, language='english')

#Создаем датафрейм
df_sentences = pd.DataFrame({'sentence': tokens_sens})
#st.write(df_sentences)


word_forms = []
task = ''
answer = ''
df = pd.DataFrame({'sentence':'', 'word_forms': word_forms, 'answer':answer, 'task':task, 'result':[]})
nlp = spacy.load("en_core_web_sm") # изменение формы глагола с помощью pyinflect
for sentence in df_sentences.sentence:
        #st.write(sentence)
    for token in nlp(str(sentence)):
        #st.write(token)
        if token.pos_=='VERB' and exercise_type == 'Выберите правильную форму глагола':
            word_forms = [token._.inflect('VB'), token._.inflect('VBN'), token._.inflect('VBP'), token._.inflect('VBZ'), token._.inflect('VBG'), token._.inflect('VBD')]
            answer = token
            task = token.pos_
        elif token.pos_=='ADJ'and exercise_type == 'Выбор правильного прилагательного':
            word_forms = [token.text, token._.inflect('JJS')]
            answer = token.text
            #st.write(word_forms)
            task = token.pos_
            #st.write('правильно')
        # elif str(token) == 'a' and exercise_type == 'Выберите правильный артикль':
        #     word_forms = ['a', 'the', 'an']
        #     answer = token
        #     #task ='article'
        else: pass
# # отобрать предложения, где есть глагол или прилагательное
         
    if len(nlp(str(sentence))) > 3:            
        df.loc[len(df)]=[sentence, word_forms, answer, task, []]    
    



if exercise_type == 'Заполните пропуск':

    st.subheader('Выберите правильные варианты пропущенных слов:')

df["sentence_hidden"]= df.apply(lambda x: x['sentence'].replace(str(x['answer']), ' ___ '), axis=1)




for index, row in df.iterrows():
    #st.write(row['sentence'], row['answer'])
    col1, col2 = st.columns(2)
    with col1:
        st.write('')
        st.write(str(row['sentence_hidden'])) 
    with col2:
        #st.write('Тут список ответов')
        #st.write(index)
        option = []
        for i in range(len(row['word_forms'])):
            #st.write(i)
            
            option.append(row['word_forms'][i])
            #st.write(i, option)
            #df['result'][index] = i
        #option = sorted(option, key=lambda k: random.random())
        option = ['–––'] + option
        #option = random.sample(option, len(option))
        df['result'][index] =  st.selectbox('nolabel', option, label_visibility="hidden", key =str(index) )
        #st.write('1111', df['origin_sentences'].astype('unicode').values)
        #st.write(df['result'][index])
        if df['result'][index] == '–––':
            pass
        
            
        #elif df['result'][index] == df['answer'][index]:
        elif df['result'][index] == str(df['answer'][index]):
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







        
       


    