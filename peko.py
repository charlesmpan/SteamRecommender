#Imports
import streamlit as st
import csv
import numpy as np
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer
import ast
from PIL import Image as pimp

#Opening the file
steam = pd.read_csv('./data/SteamFinal.csv')
steam['ReviewRange'] = steam['ReviewRange'].apply(lambda x: ast.literal_eval(x))
steam['SentimentRange'] = steam['SentimentRange'].apply(lambda x: ast.literal_eval(x))
steam['Labels'] = steam['Labels'].apply(lambda x: ast.literal_eval(x))
steam['Tags'] = steam['Tags'].apply(lambda x: ast.literal_eval(x))
steam['Categories'] = steam['Categories'].apply(lambda x: ast.literal_eval(x))
steam['Genres'] = steam['Genres'].apply(lambda x: ast.literal_eval(x))
steam = steam.set_index('AppID')
steamy = steam
steamy = steamy.sort_values('Total_Reviews', ascending=False)
steamgamelist = list(steamy.Name.values)
#Turning these categories into lists with ast.literal_eval

def create_mlb_df(df, columns):
    '''
    Uses MultiLabelBinarizer to transform specified columns and return a dataframe of encoded values
    
    Arguments:
        df: dataframe 
        columns: list of column names to encode
    
    Returns:
        new dataframe consisting of MultiLabelBinarizer transformed values
    '''
    #create a new empty dataframe with the same index as df
    new_df = pd.DataFrame(index=df.index)
    for column in columns:
        #instantiate a new MultiLabelBinarizer object
        mlb = MultiLabelBinarizer()
        mlb_array = mlb.fit_transform(df[column])
        mlb_df = pd.DataFrame(mlb_array, df.index, mlb.classes_)
        #concatenate each dataframe of encoded values by column
        new_df = pd.concat([new_df, mlb_df], axis=1)
    return new_df
mlb_df = create_mlb_df(steam, ['Labels'])
#An amalgamation of everything above

#Putting multiple games into one to see if we can handle multiple game recs at once
def SteamRecommendMeMany(game,game2,game3,game4,recs):
    if game != "":
        #This limits the game and finds the index at which it is aka the APPID, this will refer back to the actual dataframe not the mlb one later
        game = steam.index[steam.Name == game]
        # Pulling out an individual row indexed by steam app ID
        y = np.array(mlb_df.loc[game])
        # Need to reshape so it can be passed into cosine_sim function
        y = y.reshape(1, -1)
        # Utilize cosine_similarity from sklearn to return similarity scores based on cosine distance
        cos_sim = cosine_similarity(mlb_df, y)
        cos_sim = pd.DataFrame(data=cos_sim, index=mlb_df.index)
        cos_tot = cos_sim
        numct = 1
    if game2 != "":
        #This limits the game and finds the index at which it is aka the APPID, this will refer back to the actual dataframe not the mlb one later
        game2 = steam.index[steam.Name == game2]
        # Pulling out an individual row indexed by steam app ID
        y2 = np.array(mlb_df.loc[game2])
        # Need to reshape so it can be passed into cosine_sim function
        y2 = y2.reshape(1, -1)
        # Utilize cosine_similarity from sklearn to return similarity scores based on cosine distance
        cos_sim2 = cosine_similarity(mlb_df, y2)
        cos_sim2 = pd.DataFrame(data=cos_sim2, index=mlb_df.index)
        cos_tot = cos_tot + cos_sim2
        numct = numct + 1
    if game3 != "":
        #This limits the game and finds the index at which it is aka the APPID, this will refer back to the actual dataframe not the mlb one later
        game3 = steam.index[steam.Name == game3]
        # Pulling out an individual row indexed by steam app ID
        y3 = np.array(mlb_df.loc[game3])
        # Need to reshape so it can be passed into cosine_sim function
        y3 = y3.reshape(1, -1)
        # Utilize cosine_similarity from sklearn to return similarity scores based on cosine distance
        cos_sim3 = cosine_similarity(mlb_df, y3)
        cos_sim3 = pd.DataFrame(data=cos_sim3, index=mlb_df.index)
        cos_tot = cos_tot + cos_sim3
        numct = numct + 1
    if game4 != "":
        #This limits the game and finds the index at which it is aka the APPID, this will refer back to the actual dataframe not the mlb one later
        game4 = steam.index[steam.Name == game4]
        # Pulling out an individual row indexed by steam app ID
        y4 = np.array(mlb_df.loc[game4])
        # Need to reshape so it can be passed into cosine_sim function
        y4 = y4.reshape(1, -1)
        # Utilize cosine_similarity from sklearn to return similarity scores based on cosine distance
        cos_sim4 = cosine_similarity(mlb_df, y4)
        cos_sim4 = pd.DataFrame(data=cos_sim4, index=mlb_df.index)
        cos_tot = cos_tot + cos_sim4
        numct = numct + 1
    cos_tot.sort_values(cos_tot.columns[0], ascending = False).head(int(recs)+numct)
    results = cos_tot.sort_values(cos_tot.columns[0], ascending = False).head(int(recs)+numct).index
    # Using returned results variable I can index the original meta data frame to return appropriate information for each book
    steamresults = steam.loc[results]
    steamresults.reset_index(inplace=True)
    pd.options.display.float_format = '{:.2f}'.format
    recommendations = steamresults[['AppID', 'Name','Publisher','Developer','Release_Date','Price','Categories','Genres', 'Tags', 'Total_Reviews'
            ,'Sentiment']].iloc[numct: , :]
    for appid in list(results)[numct:]:
        with st.container():
            image_column, text_column = st.columns((6,4))
            with image_column:
                st.image(pimp.open(requests.get("https://cdn.akamai.steamstatic.com/steam/apps/"+str(appid)+"/header.jpg", stream=True).raw))
                st.markdown('[Steam Website URL](https://store.steampowered.com/app/'+str(appid)+')')
                st.subheader(""+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Name.values)))
                st.write("Costs $"+ "".join(map(str,steamresults.loc[steamresults.AppID == appid].Price.values)))
                st.write("Published by "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Publisher.values)))
                st.write("Developed by "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Developer.values)))
                st.write("Released on "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Release_Date.values)))
                st.write("")
                st.write("")
                st.write("")
                st.write("")
            with text_column:
                st.write("Steam categories classified under the game : "+ "/n ".join(map(str,steamresults.loc[steamresults.AppID == appid].Categories.values)))
                st.write("Steam genres classified under the game : "+ "/n ".join(map(str,steamresults.loc[steamresults.AppID == appid].Genres.values)))
                st.write("Fan/player tags are : "+ "/n ".join(map(str,steamresults.loc[steamresults.AppID == appid].Tags.values)))
                st.write("The total reviews : "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Total_Reviews.values)))
                st.write("Positive Review Percentage : "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Sentiment.values.round(2)*100))+"%")
                
st.title('Steam Game Recommender')
st.caption('Please note some games priced at $0 maybe unavailable, and that the data may become out-dated')
st.image(pimp.open(requests.get("https://www.vortez.net/contentteller.php?ct=news&action=file&id=18653", stream=True).raw))
with st.form("Steam Recommender"):
    game = st.selectbox("Enter a game you're interested in", steamgamelist)
    game2 = st.multiselect("Enter a second game you're interested in (Or leave blank)", steamgamelist)
    game3 = st.multiselect("Enter a third game you're interested in (Or leave blank)", steamgamelist)
    game4 = st.multiselect("Enter a fourth game you're interested in (Or leave blank)", steamgamelist)
    konrecokonreco = st.number_input("Number of Recommendations", 1, 20)
   # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        with st.spinner("Please wait..."):
            if len(game) == 0:
                game.append("")            
            if len(game2) == 0:
                game2.append("")
            if len(game3) == 0:
                game3.append("")
            if len(game4) == 0:
                game4.append("")                                
            if game[0] == "" and game2[0] == "" and game3[0] == "" and game4[0] == "":
                st.error("We encountered an error - Bob")
            else: 
                SteamRecommendMeMany(game,game2[0],game3[0],game4[0],konrecokonreco)



st.write("If you're interested in the following project, feel free to checkout the GitHub")
st.markdown('[Click Here for the Github](https://github.com/charlesmpan/SteamRecommender)')
