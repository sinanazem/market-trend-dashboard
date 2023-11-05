import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import datetime
import json
import pandas as pd
st.header("NLP Finance News Dashboard")

# Get the current date and time
now = datetime.datetime.now()
st.write(now.strftime("%a, %B %d"))


#Layout
# st.set_page_config(
#     page_title="Finance Dashboard",
#     layout="wide",
#     initial_sidebar_state="expanded")

#Data Pull and Functions
st.markdown("""
<style>
.big-font {
    font-size:80px !important;
}
</style>
""", unsafe_allow_html=True)
@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath,"r") as f:
        return json.load(f)

#Options Menu
with st.sidebar:

    selected = option_menu('ASAMA', ["Intro", 'Search','About'], 
        icons=['play-btn','search','info-circle'],menu_icon='intersect', default_index=0)
    lottie = load_lottiefile("/mnt/c/Users/user/OneDrive/Desktop/market-trend-dashboard/src/app/animation_loip14bs.json")
    st_lottie(lottie,key='loc', height=250, width=250)



with st.container():
    col1,col2=st.columns(2)
    with col2:
        st.markdown('**What We Offer:**')
        st.markdown(
            """
            - **Real-time Insights:** Gain a real-time understanding of market sentiment and emerging trends from the latest financial news.
            - **Advanced Analysis:** Harness the capabilities of NER, sentiment analysis, word cloud visualization, and more to uncover hidden opportunities and risks.
            - **Efficient Summaries:** Save time with automated article summarization, allowing you to digest critical information in seconds.
            """
            )
    with col1:
        lottie2 = load_lottiefile("/mnt/c/Users/user/OneDrive/Desktop/market-trend-dashboard/src/app/animation_loicsmnc.json")
        st_lottie(lottie2,key='loc2')
st.divider()
st.markdown("#### Create Dashboard!")

col1, col2, col3 = st.columns(3)
with col1:
    today = datetime.datetime.now()
    next_year = today.year
    jan_1 = datetime.date(next_year, 1, 1)
    dec_31 = datetime.date(next_year, 12, 31)

    d = st.date_input(
        "**Date**",
        (jan_1, datetime.date(next_year, 1, 7)),
        jan_1,
        dec_31,
    )

with col2:
    st.selectbox("**Sector**",
                        ("Finance", "Health", "All"))



with col3:
    bmi = st.text_input("**Ticker**")


options = st.multiselect(
    '**What do you need to analyze your text?**',
    ["WordCloud", "NER", "Most Common Words", "Topic Modeling"],
    ["NER", "WordCloud"])

st.markdown(" ")
if st.button('Generate'):
    pass
else:
    pass
st.write(options)

if "WordCloud" in options:
    pass
    