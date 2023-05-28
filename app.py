import matplotlib.pyplot as plt
import streamlit as st
import preprocessor,helper
#to create the heatmap
import seaborn as sns
import pickle
#checking path
from pathlib import  Path
#lib to authenticate user
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
from PIL import Image
import json
import requests
from streamlit_lottie import st_lottie



#user auth

names = ["Rohit","Amar","Sachin","Shiva"]
usernames = ['Rohit','Amar','Sachin','Shiva']

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)


authenticator = stauth.Authenticate(names,usernames,hashed_passwords,"whatsapp_chat","abcdef",cookie_expiry_days=30)






name , authenticator_status , username = authenticator.login("Login Form","main")



st.markdown("The next word is <span style='color:red'>red</span>",unsafe_allow_html=True)


if authenticator_status == False:
    st.error("Username/password is incorrect")
if authenticator_status == None:
    st.warning("Please enter your username and passwords")
if authenticator_status :
    # navbar
    selected = option_menu(
        menu_title=None,
        options=['Home', 'Project', 'About', 'Contact'],
        icons = ['house','motherboard','file-person','envelope-check-fill'],
        menu_icon='cast',
        default_index=0,
        orientation='horizontal'
    )
    if selected == 'Home':

        with st.container():
            lottie_load = helper.load_lottiefile("welcome.json")
            lottie_analyse = helper.load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_vxtEG7.json")

            st_lottie(
                lottie_load,
                speed=1,
                reverse=False,
                loop=True,
                quality="medium",
                key=None,
            )

        st.sidebar.image("WCA-bg.png")
        st.sidebar.title(f"Welcome {name} ")
        authenticator.logout("Logout", "sidebar")

        st.sidebar.write(
            'Welcome to the homepage of our B.Tech final year project! We are thrilled to present an innovative and impactful project that showcases our expertise and dedication to the field of technology.')
        st.sidebar(st.markdown("The next word is <span style='color:red'>red</span>",unsafe_allow_html=True))
    if selected == 'Project':
        st.sidebar.image("WCA-bg.png")
        st.sidebar.title("Whatsapp Chat Analyzer")

        authenticator.logout("Logout", "sidebar")


        #lottie_load = load_lottiefile("analyse.json")
        #lottie_analyse = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_MZUZlbTZTG.json")

        # col1, col2, col3 = st.columns(3)
        # with col1:
        #     ""
        # with col2:
        #     st.image(img,
        #              width=200)
        # with col3:
        #     ""
        #st.subheader('Welcome to whatsapp chat analyzer')

        with st.container():
            lottie_load = helper.load_lottiefile("analyse.json")
            lottie_analyse = helper.load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_MZUZlbTZTG.json")

            st_lottie(
                lottie_load,
                speed=1,
                reverse=False,
                loop=True,
                height=400,
                width=600,
                key=None,
            )


        uploaded_file = st.sidebar.file_uploader("Choose a 'text' file")
        if uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()

            # converting byte stream into string
            data = bytes_data.decode("utf-8")
            # st.text(data)
            # getting the dataframe from preprocessor
            df = preprocessor.preprocess(data)

            # st.dataframe(df)

            # fetching unique users
            user_list = df['users'].unique().tolist()
            user_list.remove('group_notification')
            user_list.sort()
            user_list.insert(0, "Overall")
            # showing dropdown of user list
            selected_user = st.sidebar.selectbox("show analysis of", user_list)

            if st.sidebar.button("Show Analysis"):

                num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

                st.title('Top Statistics')
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.header("Total Messages  ")
                    st.title(num_messages)
                with col2:
                    st.header("Total Words  ")
                    st.title(words)
                with col3:
                    st.header("Media Shared  ")
                    st.title(num_media_messages)
                with col4:
                    st.header("Link Shared  ")
                    st.title(num_links)

                # monthly timeline
                st.title('Monthly Timeline')
                timeline = helper.monthly_timeline(selected_user, df)
                fig, ax = plt.subplots()
                ax.plot(timeline['time'], timeline['message'])
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

                # daily timeline
                st.title('Daily Timeline')
                daily_timeline = helper.daily_timeline(selected_user, df)
                fig, ax = plt.subplots()
                ax.plot(daily_timeline['daily_date'], daily_timeline['message'], color='black')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

                # activity map

                st.title('Activity Map')
                col1, col2 = st.columns(2)

                with col1:
                    st.header('Most busy day')
                    busy_day = helper.week_activity_map(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.bar(busy_day.index, busy_day.values)
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                with col2:
                    st.header('Most busy month')
                    busy_month = helper.month_activity_map(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.bar(busy_month.index, busy_month.values, color='orange')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                st.title("Weekly Activity Map")
                user_heatmap = helper.activity_heatmap(selected_user, df)
                fig, ax = plt.subplots()
                ax = sns.heatmap(user_heatmap)
                st.pyplot(fig)

                # finding the most busy user in group
                if selected_user == 'Overall':
                    st.title('Most busy users')
                    x, new_df = helper.fetch_busy_user(df)
                    fig, ax = plt.subplots()

                    col1, col2 = st.columns(2)

                    with col1:
                        ax.bar(x.index, x.values, color='green')
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)
                    with col2:
                        st.dataframe(new_df)

                # Wordcloud
                st.subheader('Word Cloud')
                df_wc = helper.create_wordcloud(selected_user, df)
                fig, ax = plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)

            # most common words

            most_common_df = helper.most_common_words(selected_user, df)
            st.dataframe(most_common_df)
            st.subheader("Most Common Words")
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1])
            st.pyplot(fig)

            # emoji
            emoji_df = helper.emoji_show(selected_user, df)
            st.title('Emoji')

            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[0].head(), labels=emoji_df[0].head())
                st.pyplot(fig)

    # if selected == 'Journal':
    #     st.title("")  # You Have slected Journal
    #     st.sidebar.title(f"Welcome {name} ")
    #     authenticator.logout("Logout", "sidebar")
    if selected == 'About':
        col1 , col2 ,col3 = st.columns(3)
        with col1:
            st.title(" ")
        with col2:
            st.title("About")
        with col3:
            st.title(" ")
        c1,c2 = st.columns(2)
        with c1:
            st._main.write(
                "The goal is to provide users with a comprehensive tool that can summarize lengthy conversations, extract key topics, and visualize the data in an easily understandable format. This analysis can help individuals, businesses, researchers, and organizations gain valuable insights from their WhatsApp chats, enabling them to make informed decisions, identify trends, and improve their communication strategies.Our college project is a culmination of our academic pursuits, practical skills, and passion for technology. With a focus on the main objective of our WhatsApp Chat Analyzer project is to develop a software solution that can analyze and extract valuable insights from WhatsApp chat conversations.")
        with c2:
            st.image("about.jpg",width=500)

        st.sidebar.image("WCA-bg.png")
        st.sidebar.title(f"Welcome {name} ")
        authenticator.logout("Logout", "sidebar")
    if selected == 'Contact':
        st.header(":mailbox: Get in Touch with Us")
        contact_form = """
            <form action="https://formsubmit.co/gugallbaba@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here"></textarea>
     <button type="submit">Send</button>
</form>
        """
        st.markdown(contact_form,unsafe_allow_html=True)
        helper.local_css("style.css")
        st.sidebar.image("WCA-bg.png")
        st.sidebar.title(f"Welcome {name} ")
        authenticator.logout("Logout", "sidebar")










