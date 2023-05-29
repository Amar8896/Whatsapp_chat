import pandas as pd
from collections import Counter
from urlextract import URLExtract
from wordcloud import WordCloud
import emoji
import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie



extract = URLExtract()



def fetch_stats(selected_user,df):
    if(selected_user == 'Overall'):
        #No of messages
        num_messages = df.shape[0]
        #Shared Media
        num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
        #Total Links
        links = []
        for message in df['message']:
            links.extend(extract.find_urls(message))

        #No of words
        words = []
        for message in df['message']:
            words.extend(message.split())

        return num_messages,len(words),num_media_messages,len(links)
    else:
        new_df = df[df['users'] == selected_user]
        num_message = new_df.shape[0]
        num_media_message = new_df[new_df['message'] == '<Media omitted>\n'].shape[0]
        links = []
        for message in new_df['message']:
            links.extend(extract.find_urls(message))

        words = []
        for message in new_df['message']:
            words.extend(message.split())

        return num_message,len(words),num_media_message,len(links)

def fetch_busy_user(df):
    x = df['users'].value_counts().head()
    #calculating the most active users
    df = round((df['users'].value_counts() / df.shape[0]) * 100 , 2).reset_index().rename(columns={'count':'percent','users':'name'})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

#most common words

def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

        # remove group messages
        # remove media omitted message
        # remove stop words

        temp = df[df['users'] != 'group_notification']
        temp = temp[temp['message'] != '<Media omitted>\n']

        words = []

        for message in temp['message']:
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)

        most_common_df = pd.DataFrame(Counter(words).most_common(20))
        return most_common_df


def emoji_show(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

        emojis = []
        for message in df['message']:
            emojis.extend([c for c in message if c in emoji.EMOJI_DATA.keys()])

        emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
        return emoji_df

#monthly timeline
def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['Year','month_num','Month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))
    timeline['time'] = time
    return timeline

#daily timeline
def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    daily_timeline = df.groupby('daily_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    return df['Month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    #creating pivot table
    user_heatmap = df.pivot_table(index='day_name',columns='period', values='message',aggfunc='count').fillna(0)

    return user_heatmap


def load_lottiefile(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)





