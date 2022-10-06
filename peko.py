#Imports
import streamlit as st
import csv
import numpy as np
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer
from IPython.display import display
from IPython.display import Image
from IPython.core.display import display, HTML
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
steamgamelist = list(steam.Name.values)
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

def SteamRecommendMe(game,recs):
    #This limits the game and finds the index at which it is aka the APPID, this will refer back to the actual dataframe not the mlb one later
    game = steam.index[steam.Name == game]
    # Pulling out an individual row indexed by steam app ID
    y = np.array(mlb_df.loc[game])
    # Need to reshape so it can be passed into cosine_sim function
    y = y.reshape(1, -1)
    # Utilize cosine_similarity from sklearn to return similarity scores based on cosine distance
    cos_sim = cosine_similarity(mlb_df, y)
    # Create a dataframe with similairty scores with book product ID ('asin') as index
    cos_sim = pd.DataFrame(data=cos_sim, index=mlb_df.index)
    cos_sim.sort_values(cos_sim.columns[0], ascending = False).head(int(recs)+1)
    results = cos_sim.sort_values(cos_sim.columns[0], ascending = False).head(int(recs)+1).index
    steamresults = steam.loc[results]
    steamresults.reset_index(inplace=True)
    pd.options.display.float_format = '{:.2f}'.format
    recommendations = steamresults[['AppID', 'Name','Publisher','Developer','Release_Date','Price','Categories','Genres', 'Tags', 'Total_Reviews'
               ,'Sentiment']].iloc[1: , :]
    for appid in list(results)[1:]:
        display(Image("https://cdn.akamai.steamstatic.com/steam/apps/"+str(appid)+"/header.jpg"))
        display(HTML("""<a href=https://store.steampowered.com/app/%s/">Steam Website Link</a>"""%(appid)))
        print("The AppID on Steam for the Game is "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].AppID.values)))
        print("The Game Developer = "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Name.values)))
        print("The Game Publisher is "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Publisher.values)))
        print("The game was developed by "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Developer.values)))
        print("The game was released on "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Release_Date.values)))
        print("These are the following categories classified under the game : "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Categories.values)))
        print("These are the following genres classified under the game : "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Genres.values)))
        print("These are the following tags classified under the game : "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Tags.values)))
        print("The following are the total reviews "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Total_Reviews.values)))
        print("The following is the Positive Reviews/Total Reviews : "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Sentiment.values)))
        print("The Game Currently Costs ... "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Price.values)))
    return(recommendations)

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
        display(Image("https://cdn.akamai.steamstatic.com/steam/apps/"+str(appid)+"/header.jpg"))
        display(HTML("""<a href=https://store.steampowered.com/app/%s/">Steam Website Link</a>"""%(appid)))
        print("The AppID on Steam for the Game is "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].AppID.values)))
        print("The Game Developer = "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Name.values)))
        print("The Game Publisher is "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Publisher.values)))
        print("The game was developed by "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Developer.values)))
        print("The game was released on "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Release_Date.values)))
        print("These are the following categories classified under the game : "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Categories.values)))
        print("These are the following genres classified under the game : "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Genres.values)))
        print("These are the following tags classified under the game : "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Tags.values)))
        print("The following are the total reviews "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Total_Reviews.values)))
        print("The following is the Positive Reviews/Total Reviews : "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Sentiment.values)))
        print("The Game Currently Costs ... "+ " ".join(map(str,steamresults.loc[steamresults.AppID == appid].Price.values)))
    # Changing certain columns to display integer instead of float for more appealing final display
    return(recommendations)


#game = input('Game Name: ')
#recs = input('Number of Recommendations: ')
#SteamRecommendMe(game,recs)

st.title('Hi World')
game = st.multiselect('gameone', steamgamelist)
game2 = st.multiselect('gametwo', steamgamelist)
game3 = st.multiselect('gamethree', steamgamelist)
game4 = st.multiselect('gamefour', steamgamelist)
url = 'https://cdn.akamai.steamstatic.com/steam/apps/10/header.jpg'
im = pimp.open(requests.get(url, stream=True).raw)
st.image(im)
st.write('pig')
st.markdown('[clickme](https://store.steampowered.com/app/726990/)')