import streamlit as st
import numpy as np
import pandas as pd
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn.colors as snsc


st.set_page_config(layout="wide")

athletes = pd.read_csv("files/athletes.csv")
athletes2=athletes.copy()
final_df = pd.read_csv("files/final2_df.csv")
final2_df=final_df.copy()
final3_df=final_df.copy()
teams = pd.read_csv("files/teams.csv")
medals = pd.read_csv("files/medals.csv")
filtered_athletes= pd.read_csv("files/filtered_athlete.csv")



st.sidebar.title("Olympics 2024 Analysis")

gender=st.sidebar.radio("Select Gender",("Both","Male","Female"))
country_list=athletes['country'].unique().tolist()
country_list=sorted(country_list)
country_list.insert(0,"All")
country_selected=st.sidebar.selectbox("Select Country",country_list)
games_list= list(helper.all_games(athletes).keys())
games_list=sorted(games_list)
games_list.insert(0,"All")
# g=['3x3','BMX','Beach','Bike','Canoe','Freestyle','Sevens','Rugby','Water','Trampoline','Track']
# for i in g:
#     games_list.remove(i)

game_selected = st.sidebar.selectbox("Select Discipline",games_list)



athletes['disciplines'] = athletes['disciplines'].apply(lambda x: x.replace("[", '').replace("]", '').replace("'", ''))
athletes2['disciplines'] = athletes2['disciplines'].apply(lambda x: x.replace("[", '').replace("]", '').replace("'", ''))


athletes=preprocessor.athlete(athletes,gender,country_selected,game_selected)

color1=list(snsc.crayons.values())

st.title("General Features")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.header("Avg Weight")
    avg_w=helper.average_weight(athletes)
    if len(avg_w)==0:
        st.subheader("no data")
    else:
        st.subheader(f"{round(np.mean(avg_w),1)} kg")

with col2:
    st.header("Avg Height")
    avg_h = helper.average_height(athletes)
    if len(avg_h)==0:
        st.subheader("no data")
    else:
        st.subheader(f"{round(np.mean(avg_h),1)} cm")

with col3:
    st.header("no. athletes")
    a=helper.participate(athletes)
    if a==0:
        st.subheader("no participants")
    else:
        st.subheader(a)

with col4:
    st.header("Avg Age")
    a=helper.avg_age(athletes)
    if a == 0:
        st.subheader("no data")
    else:
        st.subheader(f"{round(a,1)} yrs")



#--------------------------------------Languages---------------------------------------------------#

col1, col2 = st.columns([0.8,0.2])

with (col2):
    if country_selected!="All":
        st.markdown("<br>",unsafe_allow_html=True)
        st.button("ⓘ",
                  help=f"""Description: Most common speaking language by athletes from {country_selected}""")
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("ⓘ",
                  help=f"""Description: Most common speaking language by athletes""")
with col1:
    st.title("Most Speaking Languages")
# st.markdown("<hr>",unsafe_allow_html=True)

col1, col2 = st.columns(2,gap="small")
# new_athletes = pd.read_csv("files/athletes.csv")
freq_lang, counter_lang = helper.lang(athletes)
with col1:

    color=sns.color_palette("Set2",freq_lang.shape[0])
    fig, ax = plt.subplots(figsize=(7,7))
    ax.pie(freq_lang[1], labels=freq_lang[0],autopct="%0.1f%%",startangle=140,explode=[0.01 for _ in range(freq_lang.shape[0])],colors=color1)
    st.pyplot(fig)

with col2:
    st.markdown("<b>",unsafe_allow_html=True)
    counter_lang.rename(columns={
        0:'Language',
        1:'Frequency'
    },inplace=True)
    a = pd.DataFrame(counter_lang)
    a.index += 1
    st.dataframe(a,width=2000)


#----------------------------------HOBBBIES----------------------------------------------------------#


col1, col2 = st.columns([0.8,0.2])

with (col2):
    if country_selected!="All":
        st.markdown("<br>",unsafe_allow_html=True)
        st.button("ⓘ",
                  help=f"""Description: Most common hobbies of athletes from {country_selected}""",key=2)
    else:
        st.markdown("<br>",unsafe_allow_html=True)
        st.button("ⓘ",
                  help=f"""Description: Most common hobbies of athletes""",key=2)
with col1:
    st.title("Most common hobbies")



col1, col2 = st.columns(2, gap="small")

with col1:
    threshold = 50
    if country_selected != "All":
        threshold = 1
        if game_selected != "All":
            threshold = 6
    if game_selected != "All":
        threshold = 12

    user_text = st.number_input(label="Threshold: ", min_value=1, max_value=200, step=1, value=threshold)
    hobbies, bar_df = helper.hobbies(athletes,user_text)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(hobbies[0],hobbies[1])
    plt.xticks(rotation=90)
    st.pyplot(fig)

with col2:
    # bar_df.reset_index(drop=True)
    bar_df=pd.DataFrame(bar_df)
    bar_df.index+=1
    bar_df.rename(columns={
        0:"Hobbies",
        1:"Frequency"
    },inplace=True)
    st.table(bar_df)


# --------------------------------------------Medals--------------------------------------------------

col1, col2 = st.columns([0.8,0.2])

with (col2):
    if country_selected=="All":
        st.markdown("<br>",unsafe_allow_html=True)
        st.button("ⓘ",
                  help=f"""Description: Medals won by every country""",key=3)
    else:
        st.markdown("<br>",unsafe_allow_html=True)
        st.button("ⓘ",
                  help=f"""Description: Medals won by {country_selected}""")
with col1:
    st.title("Medal Tally")


col1, col2 = st.columns(2, gap="small")
df=helper.medalss(final_df,country_selected,gender,game_selected)
df1=df.copy()

with col1:
    if df.empty:
        st.subheader("No Data")
        st.dataframe(df)
    else:
        fig, ax= plt.subplots(figsize=(7,7))
        if country_selected == "All":
            threshold=round(df['Medal Counts'].mean()) + 10
            if (gender != "Both") | (game_selected != "All"):
                threshold=round(df['Medal Counts'].mean()) + 2
                if df['Medal Counts'].mean() < 3.5:
                    threshold = 2

            df['Country'] = df.apply(lambda x: "Other" if x['Medal Counts'] < threshold else x['Country'], axis=1)
            df=df.groupby("Country").sum().reset_index()
            ax.pie(df['Medal Counts'],labels=df['Country'],autopct="%0.1f%%",startangle=140,explode=[0.01 for _ in range(df.shape[0])],colors=color1)
            st.pyplot(fig)

        else:

            if (df['Counts']==0).all():
                st.subheader("No Wins")
            else:
                ax.pie(df['Counts'], labels=df['Medal'], autopct="%0.1f%%", startangle=140,
                       explode=[0.01 for _ in range(df.shape[0])], colors=color)
                st.pyplot(fig)

with col2:
    if df1.empty:
        st.subheader("No Data")
    else:
        if country_selected == "All":
            df1=df1.sort_values("Medal Counts",ascending=False).reset_index(drop=True)
            df1.index+=1
            st.dataframe(df1,width=450)

        else:
            if (df['Counts']==0).all():
                st.table(df)
            else:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.table(df)

st.title("Athletes")

col1, col2 = st.columns(2, gap="small")

if country_selected == "All":
    if game_selected != "All":
        # new_df = helper.athlete_discipline(filtered_athletes, gender,game_selected)
        new_df = helper.athlete_country(athletes2, final2_df, gender, game_selected)

    else:
        new_df=helper.athlete_country(athletes2,final2_df,gender,False)
    new_df2 = new_df.copy()
else:
    if game_selected == "All":
        new_df=helper.abc(athletes,final_df,country_selected)
        new_df2=new_df.copy()
    else:
        new_df2=helper.medalist_list(final3_df,country_selected, game_selected, gender)
        new_df=new_df2['name'].value_counts().reset_index()


with col1:

    if country_selected == "All":
        if game_selected!='All':
            st.button("ⓘ", help=f"""Description: Bigger circle is the % of athletes participated from each countries in {game_selected}
                                                  and Small Circle is % of medalist from each countries in {game_selected}""")
        else:
            st.button("ⓘ",
                      help="""Description: Bigger circle is the % of athletes participated from each countries in 
                                                              and Small Circle is % of medalist from each countries""")
        if new_df.empty:
            st.write('No Data Available for that players')
        else:

            fig, ax = plt.subplots(figsize=(7, 7))
            ax.pie(new_df['Participants'].head(8),autopct="%0.1f%%",labels=new_df['Country'].head(8),startangle=140,explode=[0.01 for _ in range(new_df.head(8).shape[0])],colors=color1,radius=1.4,labeldistance=1.1,pctdistance=0.8)
            ax.pie([1,1],colors=["white","white"],radius=0.92)
            ax.pie(new_df['Medalists'].head(8), autopct="%0.1f%%", startangle=140,
                   explode=[0.01 for _ in range(8)], colors=color1, radius=0.9,pctdistance=0.6)
            plt.legend(loc="upper right",fontsize=14,title='top 10 countries',bbox_to_anchor=(0.1,0.3))
            st.pyplot(fig)
    else:
        if game_selected=="All":
            st.button("ⓘ", help=f"""Description: Bigger circle is the total % of athletes participated in each sports from {country_selected}
                                          and Small Circle is % of medalist in each sports from {country_selected}""")
            fig, ax = plt.subplots(figsize=(7, 7))
            new_df.dropna(subset=['Medalists'],inplace=True)
            if new_df.shape[0] < 8:
                ax.pie(new_df['Participants'], autopct="%0.1f%%", startangle=140,labels=new_df['Disciplines'],
                       explode=[0.01 for _ in range(new_df.shape[0])], colors=color1, radius=1.4, labeldistance=1.1,
                       pctdistance=0.8)
                ax.pie([1, 1], colors=["white", "white"],
                       radius=0.92)
                ax.pie(new_df['Medalists'], autopct="%0.1f%%", startangle=140,
                       explode=[0.01 for _ in range(new_df.shape[0])], colors=color1, radius=0.9, pctdistance=0.6)
            else:
                ax.pie(new_df['Participants'].head(8), autopct="%0.1f%%", startangle=140, labels=new_df['Disciplines'].head(8),
                       explode=[0.01 for _ in range(new_df.head(8).shape[0])], colors=color1, radius=1.4, labeldistance=1.1,
                       pctdistance=0.8)
                ax.pie([1, 1], colors=["white", "white"],radius=0.92)
                ax.pie(new_df['Medalists'].head(8), autopct="%0.1f%%", startangle=140,
                       explode=[0.01 for _ in range(new_df.head(8).shape[0])], colors=color1, radius=0.9, pctdistance=0.6)
            plt.legend(loc="upper right", fontsize=14, title='countries participants in discipline', bbox_to_anchor=(0.1, 0.3))
            st.pyplot(fig)
        else:
            st.button("ⓘ", help="""Description: Top athletes names""")
            if new_df.empty:
                st.subheader("No Data")
            else:
                fig, ax = plt.subplots(figsize=(7, 7))
                ax.pie(new_df['count'].head(8), autopct="%0.1f%%", startangle=140,
                       labels=new_df['name'].head(8),
                       explode=[0.01 for _ in range(new_df.head(8).shape[0])], colors=color1, radius=1.4,
                       labeldistance=1.1,
                       pctdistance=0.8)
                plt.legend(loc="upper right", fontsize=14, title='Top Medalists',
                           bbox_to_anchor=(0.1, 0.3))
                st.pyplot(fig)





with col2:
    if new_df2.empty:
        st.subheader("No Athletes")
    else:

        new_df = new_df.reset_index(drop=True)
        st.dataframe(new_df2,width=450)

