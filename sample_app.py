import streamlit as st
import pandas as pd
import spacy
import pyinflect
import random     

tasks = [ 
    {'sentence': 'THE BUZZ IN THE STREET _____ like the humming of flies.',
     'options' : [['was', 'is']], 
     'answers' : ['was'],
     'result'  : [''],
     'total'   : 0
    },
    
    {'sentence': 'Photographers _____ massed behind barriers patrolled by police, their long-snouted cameras poised, their breath rising like steam.',
     'options' : [['stood', 'were standing']], 
     'answers' : ['were standing'],
     'result'  : [''],
     'total'   : 0
    },
    
    {'sentence': 'Snow _____ steadily on to hats and shoulders; gloved fingers _____ lenses clear.',
     'options' : [['fell', 'had fallen'], ['wiped','were wiping']], 
     'answers' : ['fell', 'were wiping'],
     'result'  : ['', ''],
     'total'   : 0
    },
    
    {'sentence': 'From time to time there _____ outbreaks of desultory clicking, as the watchers _____ the waiting time by snapping the white canvas tent in the middle of the road, the entrance to the tall red-brick apartment block behind it, and the balcony on the top floor from which the body _____.',
     'options' : [['came', 'come'], ['filled', 'had filled'], ['had fallen', 'was falling']],
     'answers' : ['came', 'filled', 'had fallen'],
     'result'  : ['', '', ''],
     'total'   : 0
    }
]



st.header('Генератор упражнений по английскому')
st.subheader('Вставьте текст для создания упражнения')

text = st.text_area('nolabel', label_visibility="hidden")

'---'










# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

col1, col2 = st.columns(2)

with col1:
    st.checkbox("Disable selectbox widget", key="disabled")
    st.radio(
        "Set selectbox label visibility 👉",
        key="visibility",
        options=["visible", "hidden", "collapsed"],
    )

with col2:
    option = st.selectbox(
        "How would you like to be contacted?",
        ("Email", "Home phone", "Mobile phone"),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )







# exercise_type = st.sidebar.selectbox( 
#     'Выберите тип упражнения',
#     ('Выберите слово', 'Заполните пропуск')
# )

exercise_type = st.sidebar.selectbox('Выберите тип упражнения:', ['', 'Выберите правильную форму глагола', 'Выберите слово', 'Заполните пропуск'], format_func=lambda x: 'Ничего не выбрано' if x == '' else x)

if exercise_type:
    st.success('Ура! Вы выбрали тип упражнения 🎉')
    st.write("Вы выбрали упражнение: ", exercise_type)
else:
    st.warning('Ничего не выбрано')

# def get_exercise_type(name):
#     data = None
#     if name == 'Выберите слово':
#         st.write(name)
#     elif name == 'Заполните пропуск':
#         st.write(name)





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

"And what are you carrying under your apron?"

"Grandmother is sick and weak, and I am taking her some cake and wine. We baked yesterday, and they should give her strength."

"Little Red Cap, just where does your grandmother live?"

"Her house is a good quarter hour from here in the woods, under the three large oak trees. There's a hedge of hazel bushes there. You must know the place," said Little Red Cap.

The wolf thought to himself, "Now there is a tasty bite for me. Just how are you going to catch her?" Then he said, "Listen, Little Red Cap, haven't you seen the beautiful flowers that are blossoming in the woods? Why don't you go and take a look? And I don't believe you can hear how beautifully the birds are singing. You are walking along as though you were on your way to school in the village. It is very beautiful in the woods."

Little Red Cap opened her eyes and saw the sunlight breaking through the trees and how the ground was covered with beautiful flowers. She thought, "If a take a bouquet to grandmother, she will be very pleased. Anyway, it is still early, and I'll be home on time." And she ran off into the woods looking for flowers. Each time she picked one she thought that she could see an even more beautiful one a little way off, and she ran after it, going further and further into the woods. But the wolf ran straight to the grandmother's house and knocked on the door.

"Who's there?"
    ''')

# df = pd.read_csv(txt, lineterminator = '\n', header=None, sep="\t", names=['origin_sentences'])
# df.head(5)








import nltk
from nltk.corpus import stopwords
tokens_sens = nltk.tokenize.sent_tokenize(text2, language='english')
#Создаем датафрейм
df_sentences = pd.DataFrame({'sentence': tokens_sens})
#st.write(df_sentences)



if exercise_type == 'Выберите правильную форму глагола': #Если упражнение - выбор формы глагола
    verb_forms = []
    answer = ''
    df = pd.DataFrame({'sentence':'', 'verb_forms': verb_forms, 'answer':answer, 'result':[]})
    nlp = spacy.load("en_core_web_sm") # изменение формы глагола с помощью pyinflect
    for sentence in df_sentences.sentence:
        #st.write(sentence)
        for token in nlp(str(sentence)):
            if token.pos_=='VERB':
                verb_forms = [token._.inflect('VBP'), token._.inflect('VBZ'), token._.inflect('VBG'), token._.inflect('VBD')]
                answer = token
            
                
        df.loc[len(df)]=[sentence, verb_forms, answer, []]                 
    st.write(df)

 

    # for token in nlp(str(df_sentences.sentence)):
    #     if token.pos_=='VERB':
    #         verb_forms = [token._.inflect('VBP'), token._.inflect('VBZ'), token._.inflect('VBG'), token._.inflect('VBD')]
    #         answer = token
    #     df_sentences['answers'] = df_sentences.apply(lambda x: token, axis=1)



# if exercise_type == 'Выберите правильную форму глагола': #Если упражнение - выбор формы глагола
#     nlp = spacy.load("en_core_web_sm") # изменение формы глагола с помощью pyinflect
#     for token in nlp(str(df_sentences.sentence)):
#         if token.pos_=='VERB':
#             verb_forms = [token._.inflect('VBP'), token._.inflect('VBZ'), token._.inflect('VBG'), token._.inflect('VBD')]
#             answer = token
#         df_sentences['answers'] = df_sentences.apply(lambda x: token, axis=1)


            # df["final_ride_cost"] = df.apply(lambda x: int(x["ride_cost"] * 0.95)
            #                      if x["rating"] > 6 and x["speed_max"] < 120
            #                      else int(x["ride_cost"] * 1.05),
            #                      axis=1)
            
            #st.write(verb_forms)
#st.write(df_sentences)      
#st.write(verb_forms, '---------\n')


if exercise_type == 'Заполните пропуск':

    st.subheader('Выберите правильные варианты пропущенных слов:')


for index, row in df.iterrows():
    #st.write(row['sentence'], row['answer'])
    col1, col2 = st.columns(2)
    with col1:
        st.write('')
        st.write(str(row['sentence']))
    with col2:
        #st.write('Тут список ответов')
        #st.write(index)
        option = []
        for i in range(len(row['verb_forms'])):
            #st.write(i)
            
            option.append(row['verb_forms'][i])
            #st.write(i, option)
            #df['result'][index] = i
        df['result'][index] =  st.selectbox('nolabel', ['–––'] + option, label_visibility="hidden",  key = str(random.random()))
        if df['result'][index] == '–––':
            pass
            #st.write('pass')
        #elif df['result'][index] == df['answer'][index]:
        elif df['result'][index] == str(df['answer'][index]):
            st.write('Правильно')
            #st.success('Это правльный ответ', icon="✅")
            
        else:
            #st.error('Попробуйте еще раз', icon="😟")
            st.write('Неправильно')


st.write(df)



# for sentence in df:
#     #st.write(task)
#     col1, col2 = st.columns(2)
#     with col1:
#         st.write('')
#         st.write(str(df.sentence))
#     with col2:
#          #for i in range(len(task['options'])):
#          st.write('Тут список ответов')








        
       

for task in tasks:
    col1, col2 = st.columns(2)
    with col1:
        st.write('')
        st.write(str(task['sentence']))
        
    with col2:
        for i in range(len(task['options'])):
            option = task['options'][i]
            task['result'][i] = st.selectbox('nolabel', 
                                             ['–––'] + option, 
                                             label_visibility="hidden", key = str(random.random()))
            if task['result'][i] == '–––':
                pass
            elif task['result'][i] == task['answers'][i]:
                st.success('', icon="✅")
            else:
                st.error('', icon="😟")
    task['total'] = task['result'] == task['answers']    
    '---'        

total_sum = sum(task['total'] for task in tasks)

if total_sum == len(tasks):
    st.success('Успех!')
    st.balloons()
    