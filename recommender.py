import pandas as pd

#import data
data = pd.read_csv('/home/pi/RSL/userReviews.csv',sep=';')
print(data.head())

#make a subset with the same columns as the data of userreviews.csv
subset = pd.DataFrame(columns=data.columns.tolist())
subset = data[data.movieName == 'mean-girls']
#print(subset)

#Create the final recommender dataframe
recommendation = pd.DataFrame(columns=data.columns.tolist()+['rel_inc','abs_inc'])

for idx, Author in subset.iterrows():
    #print(Author)
    author = Author[['Author']].iloc[0]
    ranking = Author[['Metascore_w']].iloc[0]
    
    filter1 = (data.Author==author)
    filter2 = (data.Metascore_w>ranking)
    possible_recommendation = data[filter1 & filter2]
    #print(possible_recommendation.head())
    # the loc function locates a specific value
    # rel_inc = relative increase: to compare the metascore the auther gave to another movie (percentage). e.g. mean girls has a metascore of 5 and la la land 7, so the increase is 1.4
    # abs_inc = abstract increase: to compare the metascore the auther gave to another movie (number). e.g. mean girls has a metascore of 5 and la la land 7, so the increase is two.
    possible_recommendation.loc[:,'rel_inc'] = possible_recommendation.Metascore_w/ranking
    possible_recommendation.loc[:,'abs_inc'] = possible_recommendation.Metascore_w - ranking
    
    #add the possible recommendations to the recommendations dataframe
    recommendation = recommendation.append(possible_recommendation)

#sort values first relative score, then absolute score
recommendation = recommendation.sort_values(['rel_inc','abs_inc'], ascending=False)
#drop duplicates to decrease size
recommendation = recommendation.drop_duplicates(subset='movieName', keep="first")

#make a new csv file with the top 50 recommendations 
recommendation.head(50).to_csv("/home/pi/RSL/recommendationbasedonmetascore.csv", sep=";", index=False)
print(recommendation.head(50))
print(recommendation.shape)
