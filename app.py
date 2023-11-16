import streamlit as st
import pickle
import string
import nltk
import time
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def changetext(text):
    text = str(text).lower()
    text = nltk.word_tokenize(text)
    x=[]
    for i in text:
        if i.isalnum():
            x.append(i)
    text=x[:]
    x.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            x.append(i)
    text=x[:]
    x.clear()
    for i in text:
        x.append(ps.stem(i))
    return " ".join(x)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


tfidf=pickle.load(open('vectorizer.pkl','rb'))
model=pickle.load(open('model.pkl','rb'))
st.title("Email/SMS Spam Detector")
input_sms=st.text_area("Enter the message")
if st.button('Predict'):
    if not input_sms:
        st.warning('ㅤPlease input a message.', icon="⚠️")

    if input_sms:
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()
        changedsms=changetext(input_sms)
        vector_input=tfidf.transform([changedsms])
        result=model.predict(vector_input)[0]
        if result==1:
            st.error('ㅤSpam!', icon="🚨")
        if result==0:
            st.success('ㅤNot Spam!', icon="✅")