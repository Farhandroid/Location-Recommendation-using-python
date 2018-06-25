# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 23:55:16 2018

@author: farhan
"""
import numpy as np 
import pandas as pd
#import scipy as scp
import time

dataFile='/Users/USER/Desktop/Thesis/Recommendation(Code)/dataset_new_23_6_18.csv'
df=pd.read_csv(dataFile,sep=",",header=None,skiprows=1,
                 names=['userID','venueID','venueCategoryID','venueCategoryName','Latitude','Longitude','distenceFromCenter','CheckinCount'],encoding = 'latin')

#df.head()

userPlacedCheckInMatrix=pd.pivot_table(df, values='CheckinCount',
                                    index=['userID'], columns=['venueID'])
#userPlacedCheckInMatrix.head()
#userPlacedCheckInMatrix.loc[698,'4d65c8b1a282a1cd9dc02764']
#w=0
from scipy.spatial.distance import correlation 
def similarity(user1,user2):
    user1=np.array(user1)-np.nanmean(user1)
    user2=np.array(user2)-np.nanmean(user2)
    
    #user1=np.array(user1)
    #user2=np.array(user2)
    """
    print("insert")
    x = user1[~np.isnan(user1)]
    print("user1 : ",x,sep="")
    x = user2[~np.isnan(user2)]
    print("user2 : ",x,sep="")
    """

    commonItemIds=[i for i in range(len(user1)) if user1[i]>0 and user2[i]>0]
   
    if len(commonItemIds)==0:
        return 0
    else:
        #print("commonitemidSize : ",len(commonItemIds))
        #time.sleep(5) 
        user1=np.array([user1[i] for i in commonItemIds])
        user2=np.array([user2[i] for i in commonItemIds])
        
        #user1 = scp.sparse.csr_matrix(user1)
        #user2 = scp.sparse.csr_matrix(user2)
        #corelation=correlation(user1,user2)
        #print("corelation : ",corelation,sep="")
        #print("user 1 : ",user1,sep="")
        #print("user 2 : ",user2,sep="")
        #time.sleep(10)
       
        #if user1>0 and user2>0 and w>2:
        return correlation(user1,user2)
        #else:
           # w=w+1
            #return 0
        
#correlation(4.70909091,7.59493671)

def nearestNeighbourCheckins(activeUser,K):
    similarityMatrix=pd.DataFrame(index=userPlacedCheckInMatrix.index,
                                  columns=['Similarity'])
    for i in userPlacedCheckInMatrix.index:
        similarityMatrix.loc[i]=similarity(userPlacedCheckInMatrix.loc[activeUser],
                                          userPlacedCheckInMatrix.loc[i])
    similarityMatrix=pd.DataFrame.sort_values(similarityMatrix,
                                              ['Similarity'],ascending=[0])
    nearestNeighbours=similarityMatrix[:K]
 
    
    neighbourItemRatings=userPlacedCheckInMatrix.loc[nearestNeighbours.index]
   # print("neighbourItemRatings : ",neighbourItemRatings)
    #time.sleep(10)
    
    predictItemCheckin=pd.DataFrame(index=userPlacedCheckInMatrix.columns, columns=['Checkin'])
    
    for i in userPlacedCheckInMatrix.columns:
        predictedCheckin=np.nanmean(userPlacedCheckInMatrix.loc[activeUser])
        for j in neighbourItemRatings.index:
            if userPlacedCheckInMatrix.loc[j,i]>0:
                predictedCheckin += (userPlacedCheckInMatrix.loc[j,i]
                                    -np.nanmean(userPlacedCheckInMatrix.loc[j]))*nearestNeighbours.loc[j,'Similarity']
        predictItemCheckin.loc[i,'Checkin']=predictedCheckin
    #print("predictItemCheckin : ",predictItemCheckin)
    #time.sleep(10)   
        
    return predictItemCheckin
    


def topNRecommendations(activeUser,N):
    predictPlaceCheckins=nearestNeighbourCheckins(activeUser,10)
    placeAlreadyChecked=list(userPlacedCheckInMatrix.loc[activeUser]
                              .loc[userPlacedCheckInMatrix.loc[activeUser]>0].index)
    predictPlaceCheckins=predictPlaceCheckins.drop(placeAlreadyChecked)
    #print("predictPlaceCheckins : ",predictPlaceCheckins)
    #time.sleep(10)
    
    topRecommendations=pd.DataFrame.sort_values(predictPlaceCheckins,
                                                ['Checkin'],ascending=[0])[:N]
    #print("topRecommendations : ",topRecommendations)
    #time.sleep(10)
    topRecommendationTitles=(df.loc[df.venueID.isin(topRecommendations.index)])
    
    #print("topRecommendationTitles : ",topRecommendationTitles)
    #time.sleep(10)
    topRecommendationTitles=topRecommendationTitles.drop_duplicates(['venueID'], keep='first')
    #print("topRecommendationCategoryName : ",topRecommendationTitles.venueCategoryName,sep="")
    #print("topRecommendationTitlesList : ",list(topRecommendationTitles.venueCategoryName))
    #time.sleep(10)
    
    return list(topRecommendationTitles.venueCategoryName)

#topNRecommendations(470,5)
def favoritePlaces(activeUser,N):
    topPlaceCheckedIn=pd.DataFrame.sort_values(
        df[df.userID==activeUser],['CheckinCount'],ascending=[0])[:N]
    return list(topPlaceCheckedIn.venueCategoryName)

recommendedPlace=topNRecommendations(599,3)
favouratePlace=favoritePlaces(599,3)
print("recommendedPlace : ",recommendedPlace,sep="")
print("favouratePlace : ",favouratePlace,sep="")
