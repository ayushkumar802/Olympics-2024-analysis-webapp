from datetime import datetime
from collections import Counter
import pandas as pd
def average_weight(athletes):
    athletes = athletes[athletes['weight'] != 0.0]
    athletes.dropna(subset=['weight'], inplace=True)
    athletes['weight'] = athletes['weight'].astype(int)

    return athletes['weight'].tolist()

def average_height(athletes):
    athletes = athletes[athletes['height'] != 0.0]
    athletes.dropna(subset=['height'], inplace=True)
    athletes['height'] = athletes['height'].astype(int)

    return athletes['height'].tolist()

def participate(athletes):
    return len(athletes['code'].unique())

def avg_age(athletes):
    athletes.dropna(subset=['birth_date'],inplace=True)
    if athletes.shape[0]==0:
        return 0
    athletes['birth_date']=athletes['birth_date'].astype('datetime64[ns]')
    athletes['age'] = athletes.apply(lambda x: datetime.now().year - x["birth_date"].year, axis=1)
    return athletes['age'].mean()


def lang(athletes):
    a = str(athletes['lang'].tolist()).replace("'", "").replace(", nan", "").replace("[", "").replace("]", "").replace(
        ".", "").replace("/", ",").replace(" ", "").split(",")
    b = Counter(a)
    return pd.DataFrame(b.most_common(5)), pd.DataFrame([b.keys(), b.values()]).T.sort_values(1, ascending=False)


def hobbies(df,user_text):

    df.dropna(subset=['hobbies'], inplace=True)
    string = " ".join(df['hobbies'].tolist()).lower()
    sli = string.split(",")
    a = [i.strip() for i in sli]
    d = pd.DataFrame(Counter(a).items())
    d[0] = d.apply(lambda x: 'other' if x[1] < user_text else x[0], axis=1)
    d[0] = d.apply(lambda x: 'music' if x[0] == "listening to music" else x[0], axis=1)
    d[0] = d[0].apply(lambda x: x[:30])
    d=d[d[0]!='other']
    d=d.groupby(0, as_index=False).sum()
    d=d.sort_values(1,ascending=False)
    return d,Counter(a).most_common(8)


def athlete_country(athletes,final_df,gender,game_selected):
    if gender != "Both":
        athletes=athletes[athletes['gender']==gender]
        final_df = final_df[final_df['gender']==gender]
    if game_selected:
        athletes = athletes[athletes['disciplines'] == game_selected]
        final_df = final_df[final_df['discipline'] == game_selected]

    df = athletes['country'].value_counts().reset_index()
    df.rename(columns={
        "country": "Country",
        "count": "Participants"
    }, inplace=True)
    df1 = final_df['country_x'].value_counts().reset_index()
    df1.rename(columns={
        "country_x": "Country",
        "count": "Medalists"
    }, inplace=True)
    new_df = pd.merge(df, df1, on="Country", how="left")
    new_df["Medalists"]=new_df["Medalists"].fillna(0)
    new_df["Winning Rate"] = round(new_df["Medalists"] / new_df["Participants"], 3)
    new_df=new_df.sort_values("Medalists", ascending=False)

    return new_df

def athlete_discipline(athletes,gender,game_selected):
    if gender != "Both":
        athletes=athletes[athletes['gender']==gender]
    df=athletes.groupby(["events", "disciplines"], as_index=False).count()
    df.drop(columns=['Unnamed: 0', 'gender', 'country'], inplace=True)
    df.rename(columns={
        "name": "Participants",
        "disciplines": "Disciplines",
        "events": "Events"
    }, inplace=True)
    a = df.pop("Disciplines")
    df.insert(0, 'Disciplines', a)
    if game_selected != "All":
        df = df[df['Disciplines'] == game_selected]
    return df



def medalss(medals,country_selected,gender,game_selected):
    medals.drop_duplicates(subset=["team_code", "discipline", 'event', 'medal_type', 'country_x'], inplace=True)
    if gender != "Both":
        medals=medals[medals['gender']==gender]
    if game_selected != "All":
        medals=medals[medals['discipline']==game_selected]

    if country_selected == "All":
        df1 = medals['country_x'].value_counts().reset_index()
        df1.rename(columns={
            "country_x": "Country",
            "count": "Medal Counts"
        },inplace=True)
        return df1

    else:
        df2 = medals[medals["country_x"] == country_selected]
        b = df2['medal_type'].tolist()
        g = 0
        bz = 0
        s = 0
        for i in b:
            if i == "Gold Medal":
                g += 1
            elif i == "Silver Medal":
                s += 1
            elif i == "Bronze Medal":
                bz += 1
        df = pd.DataFrame([g, s, bz], ["Gold Medal", "Silver Medal", "Bronze Medal"]).reset_index()
        df.rename(columns={
            "index": "Medal",
            0: "Counts"
        }, inplace=True)
        df.index += 1
        return df

def all_games(athletes):
    athletes.rename(columns={
        "discipline": "disciplines"
    }, inplace=True)
    athletes['disciplines'] = athletes['disciplines'].apply(lambda x: x.replace("[", '').replace("]", '').replace("'", ''))
    new_list = []
    for i in str(list(athletes['disciplines'])).replace("[", '').replace("]", '').replace("'", '').split(","):
        i = i.strip()
        new_list.append(i)
    return Counter(new_list)

def abc(athletes,final_df,country_selected):
    athletes = athletes[athletes['country']==country_selected]
    final_df = final_df[final_df['country_x']==country_selected]
    df1=pd.DataFrame(all_games(athletes).items())
    df1.rename(columns={
        0 :"Disciplines",
        1 :"Participants"
    },inplace=True)
    df2=pd.DataFrame(all_games(final_df).items())
    df2.rename(columns={
        0 :"Disciplines",
        1 :"Medalists"
    },inplace=True)
    df=pd.merge(df1,df2,on="Disciplines",how="left")
    df=df.sort_values("Participants",ascending=False)
    return df

def medalist_list(athletes,country,discipline,gender):
    athletes=athletes[athletes['country_x']==country]
    athletes=athletes[athletes['discipline']==discipline]
    if gender != "Both":
        athletes = athletes[athletes['gender'] == gender]
    athletes.drop(columns=['Unnamed: 0', 'code', 'country_x',"discipline","team_code","num_athletes"],inplace=True)
    athletes['name']=athletes['name'].apply(lambda x: x.title())
    return athletes