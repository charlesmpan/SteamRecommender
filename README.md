# SteamRecommender
![Top 10 Tags](/images/steam-banner.jpeg)
### Steam Recommender System - Content Based Approach
## Project Overview
Steam is one of the largest digital distributors for games and is well known by almost everyone who plays games. I created a content based recommendation system using cosine similarity from data I queried/requested from Steam API and Steam Spy API. All the user has to do is input one to four games and the number of recommendations they want, and they'll receive a game image, a URL to the games website on Steam, and information regarding the game.\
This repository contains four jupyter notebooks, an environment file, a python file for StreamLit, a requirement file for StreamLit, and a data folder containing the cleaned data. The first notebook is just the Requests/Data Query process for obtaining the data from Steam/SteamSpy. The second and third notebook consists of data cleaning and preprocessing. The fourth notebook consists of the recommender system that works solely on Python. The peko.py file on the other hand, works for Streamlit since it uses st.write and other code as opposed to Print. 

## Business and Data Understanding
Steam has a huge library of more than fifty thousand games and constantly gathering and obtaining new games to sell digitally. I have created a content based recommendation system for Steam using data from both Steam as well as SteamSpy which aggregates user data on games. The content based recommendation system uses cosine similarity to determine which games should be recommended to the user based on their input.

## Data Sourcing
There are many data sources from Kaggle which can be found; however, they are very out-dated.
I looked at the following initially but chose not to use the databases from kaggle.
https://www.kaggle.com/datasets/tamber/steam-video-games

The following link is really useful for pulling out data from Steam if you want to get information yourself. I used the following link as it was of great help, but I would not recommend doing the following as it takes hours on end to extract data from both ends. There are also times where the query gets interrupted due to an error so leaving it unattended is unreliable on a shorter time schedule.
https://nik-davis.github.io/posts/2019/steam-data-collection/

## Data Understanding
The data used collected from the Steam Website as well as SteamSpy which can be googled.
The major features that ended up in the Final CSV File will be explained below.
* = From Steam, ^ = From SteamSpy
1. *AppID : The unique identifier associated with each game on Steam
2. *Name : Name of the game 
3. *Description : Description of the Game (Too many issues, too little time)
4. *Publisher : The Publisher associated with the game
5. *Developer : The Developer associated with the game
6. *Release_Date : The date the game was released
7. ^Price : The Price of the Game (At the time of the query)
8. ^Categories : The Categories tags provided by Steam for the game
9. *Genres : The Genre tags provided by Steam for the game
10. ^Tags : The tags collected by user inputs from Steam (From SteamSpy)
11. *Total_Reviews : The Positive/Negative Reviews added together
12. Sentiment : The Positive reviews divided by the total reviews
13. PriceRange : Categorizing the price into ranges for the purpose of turning into a label
14. SentimentRange : Categorizing the sentiment into ranges for the purpose of turning into a label
15. ReviewRange : Categorizing the review into ranges for the purpose of turning into a label
16. Labels : All the labels used for the Content Based Recommendation system

Preview of the Largest Features used in the Recommender System
The following charts were created based off around seventeen thousand games remaining after all the cleaning and removal of games with no/low reviews.
![Top 10 Labels](/images/Categories.png)
The following are the top ten categories based off total count.
There is a missing column due to a small issue of empty entries in the lists.
![Top 10 Genres](/images/Genres.png)
The following are the top ten categories based off total count.
There is an issue for D since I removed all the numbers.
![Top 10 Tags](/images/Tags.png)
The following are the top ten categories based off total count.
There is gladly no issue here since SteamSpy data is a lot cleaner.

## The Steps in making the Recommendation Systems
Step 1. Data query (60h+ journey)\
Step 2. Merging the two dataframes from Steam/SteamSpy to create one massive dataframe\
Step 3. Data cleaning and removal of unnecessary features\
Step 4. Categorize/Bin certain features such as price, sentiment, and review count.\
Step 5. Ensure that all the features to be used format into a list, and add them all into one column called Labels\
Step 6. Run a MultiLabelBinarizer on the Labels to generate the matrix that will be used for cosine similarity\
Step 7. Create the recommender system based off user input that'll use the MLB and sort by score afterwards to return the top #(based off user entry) recommendations back\

## The Streamlit App
peko.py is the file used to open and access Streamlit. If you have downloaded the repository and have it opened, you can simply enter the following into your terminal\
```streamlit run peko.py```\
This opens up streamlit on your browser and you can finagle with the recommender from there.\
The coding for the streamlit app is a bit different from the jupyter notebooks and had to be modified so that the outputs changed. Streamlit does not really takes outputs such as print or return, but uses st.write(), st.markdown(), and etc. thus the things that usually print out results from the for-loop and whatnot had to be changed from print to st.write(). Also, the results had to be visually pleasing, so I added a lot more additions that utilize the streamlit library to output something pleasing to the eyes for the users.\
Unfortunately, I was unable to host this live so I can't provide a link that'll allow everyone to just use the recommender system. I am not sure what the issue is as Streamlit does a terrible job of logging or locating the issue at hand. The repository only really uses the final Steam cleaned csv file (sub 50mb), and the other dataframe produced by the Multi Label Binarizer is only around 350mb.


## Conclusion
The recommender system outputs recommendations based off the user input, and it seems to do a great job of pushing out games that have very similar labels. There are many limitations to this as it doesn't really factor in stuff such as sentiment and popularity too well, and essentially it does a great job of recommending games of similar nature. Alas, this is the flaw of the content recommender system and if I wanted a recommender system that recommends based off how people have enjoyed games and whatnot, I would have to build a collaborative recommender system.\
Another issue is that the multiple game recommendation input essentially just sums the scores of the cosine similarity scoring and returns that. I did a few test runs of multiple games and essentially if you put two visual novel games and one shooting games and only look for five recommendations back; it will return you basically five recommendations that will most likely be visual novels.


# Want to add/contribute/stare at the repository
Fork this repository\
Clone your forked repository\
Add your scripts\
Commit and push\
Create a pull request\
Star this repository\
Wait for pull request to merge\
Allow me to review your contribution\

# Repository Structure

├── README.md <- The README for this project\
├── 01_NotebookDataQueries.ipynb <- Data Query Notebook\
├── 02_NotebookDataCleaning.ipynb <- Data Cleaning Notebook\
├── 03_NotebookDataMoreCleaning.ipynb <- Data Cleaning Notebook\
├── 04_NotebookRecommenderModel.ipynb <- Recommender System Notebook\
├── peko.py <- Python script for Streamlit\
├── C-Capstone_Steam_Recommender.pptx\
├── C-Capstone_Steam_Recommender.pdf\
├── data\
    └── SteamFinal.csv <- Final Cleaned Notebook\
├── images\
    ├── Categories.png <- Top 10 Category Chart\
    ├── Genres.png <- Top 10 Genres Chart\
    ├── Tags.png <- Top 10 Tags Chart\
    └── steam-banner.jpg <- Banner image for Readme\
├── environment.yaml <- Environment file for Python\
├── requirements.txt <- Requirement file for Streamlit\
└── .gitignore <- The .Gitignore file