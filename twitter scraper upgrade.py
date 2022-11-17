import streamlit as st
from streamlit_option_menu import option_menu
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import datetime
import time
import json

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Features", "Project", "About Me"],
        icons=["house", "binoculars", "app-indicator", "person-video3"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":
    st.image("data:image/png;base64,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")
    st.header("Welcome to  Tweet scrapping App ")
    st.subheader("Let's start scrape data from twitter:sunglasess:")
    st.write("See main menu for more options")

    st.subheader("Why?")
    st.write("Scraping Twitter can yield many insights into sentiments, opinions and social media trends.")
    st.write(
        "Analysing tweets, shares, likes, URLs and interests is a powerful way to derive insight into public conversations.")

    st.subheader("5 Ways To Use Twitter Data For Businesses")
    with st.expander("1.Understanding Customers"):
        st.write(
            "Twitter is a deep resource of customer insights. By surveying brand or product mentions, businesses can analyse the conversations surrounding their brands or products. Twitter today is widely used for customer service, and many people tag brands when they need assistance. This data can be mined and analysed for common issues or complaints. This also extends to positive customer experiences or discussions. ")
    with st.expander("2.Influencer Marketing"):
        st.write(
            "Scraping Twitter data can help locate potential influencers. For example, industry-specific keywords and tags can reveal top posters. This provides opportunities to reach out to influencers via Twitter or another platform. Moreover, Twitter data helps you find what hashtags influencers are using so you can copy these to get noticed in similar hashtag streams. ")
    with st.expander("3.Brand and Reputation Monitoring"):
        st.write(
            "Brand reputations are particularly important on Twitter. Negative stories have been proven to travel faster on Twitter than positive ones. Monitoring brand mentions and reputational comments allows businesses to quickly stub out any false negative stories, or respond to true negative stories promptly to mitigate reputational damage. Brand and product monitoring also help businesses improve services and products and provide on-hand advice to common issues. ")
    with st.expander("4.Sentiment Analysis"):
        st.write(
            "Sentiment analysis targets the semantic meaning of tweets and content, i.e. their emotions. For example, if customers report positive sentiments around a brand or products using words such as ‘super, excellent, happy, content,’ etc, this is a positive sign. Conversely, if customers report negative sentiments such as ‘unhappy, annoyed, frustrated,’ etc, then this is a sign that the brand should intervene. Sentiments can help design customer service and even shape product and service improvements.")
    with st.expander("5.Competitor Monitoring"):
        st.write(
            "All of these techniques can be applied to competitors. It’s possible to analyse sentiments surrounding competitor products or services, or discover what competitors are doing well (or badly), so you can respond strategically. Monitoring competitors’ campaigns and Twitter strategies also reveal insights into how your brand can match or beat their winning tactics. ")

if selected == "Features":
    st.write("Data can be scrape from Twitter :bird: easily")
    st.write(":star:. Easily downloaded as csv")
    st.write(":star: Easily downloaded to json format")
    st.write(":star: Easily uploaded into your's favorite cloud database or local host")


if selected == "Project":
    st.image("data:image/png;base64,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")
    st.header("Tweet scrapping App ")
    st.subheader("WELCOMES'S YOU :heart::smile:")
    st.write("Let's start scarpe data from twitter")

    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)

    with st.form("my form"):
        keyword = st.text_input("Enter your Keyword or Hashtag to be searched : ",
                                placeholder="#Data_Scientist or #viratkohli")
        starting_date = st.date_input("Starting Date                          : ", value=datetime.date(2022, 1, 1),
                                      min_value=datetime.date(2017, 1, 1))
        ending_date = st.date_input("End Date                                 : ", max_value=datetime.date.today())
        no_of_tweets = st.slider("No of Tweets needed                         : ", 50, 500, step=50)
        submit = st.form_submit_button("Search")

    try:

        t = f"{keyword} since:{starting_date} until:{ending_date}"
        tweets_list1 = []
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(t).get_items()):
            if i > no_of_tweets:
                break
            tweets_list1.append([tweet.date, tweet.id, tweet.url, tweet.content, tweet.username])
        tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Tweet url', 'Text', 'Username'])

        try:
            st.dataframe(tweets_df1, width=900)
        except:
            st.error('There is no data available for your input', icon="🚨")

        st.download_button("Download as CSV", tweets_df1.to_csv(), file_name=f'{keyword}.csv', mime='text/csv')

        try:
            def convert_df(tweets_df1):
                return tweets_df1.to_csv(index=False).encode('utf-8')


            csv = convert_df(tweets_df1)
            st.download_button("Download JSON File", csv, f'{keyword}.json', key='download-json')

        except:
            st.error('json not working', icon="🚨")

        g = tweets_df1.to_dict("r")

        if st.button("Upload into MongoDB"):
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            my_db = client["scrapped_database"]
            my_col = my_db["twitter"]
            my_col.insert_many(g)
            st.success("Uploaded successfully")
            with st.expander("To view MangoDB file"):
                st.write(g)

    except:
        st.error('Enter the Data and Search again ', icon="🚨")

if selected == "About Me":
    st.header("Hi, I am R.sarath kumar:wave:")
    st.subheader("A Newbie Data Scientist From Bsc Biotech Background")
    st.write("I am passionate about learning python to be more efficient and effective in **AI and ML Projects**")
    st.write("Check out my other projects in [GitHub]")


