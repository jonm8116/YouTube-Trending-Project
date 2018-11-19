from bs4 import BeautifulSoup as bs
import requests
import json
import urllib
import re
import operator
import pandas as pd
import time

def getApiKey(filename):
    keyfile = open(filename)
    return keyfile.readlines()[-1].rstrip()

def readFile(filename):
    dataframe = pd.read_csv()

def getVideoStats(api_key):
    dataframe = pd.read_csv("../data/NonTrending-YouTube.csv")
    listofIds = dataframe['URL'].dropna()
    viewCount=[]
    likeCount=[]
    dislikeCount=[]
    commentCount=[]
    # print(dataframe['URL'])
    # print('END OF FIRST DATAFRAME')
    counter = 0
    outerCounter=0
    fiftyVideoIds =""
    for video_id in listofIds:
        # print(video_id)
        try:
            if(counter<50):
                if(counter>=49):
                    fiftyVideoIds+=video_id
                else:
                    fiftyVideoIds+=video_id+","
                counter+=1

                if(video_id == listofIds[-1]):
            else:
                searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+fiftyVideoIds+"&key="+api_key+"&part=statistics"
                #print(searchUrl)
                response = urllib.request.urlopen(searchUrl).read().decode('utf-8')
                formJson = json.loads(response)
                #print(formJson)
                print("Took " + str(time.time() - start_time) + " seconds.")

                viewCount.append(formJson['items'][0]['statistics']['viewCount'])
                likeCount.append(formJson['items'][0]['statistics']['likeCount'])
                dislikeCount.append(formJson['items'][0]['statistics']['dislikeCount'])
                commentCount.append(formJson['items'][0]['statistics']['commentCount'])
                counter=0
                fiftyVideoIds=""


        except (IndexError, KeyError):
            continue
        # if(counter==5):
        #     break

    #data = json.loads(str(response))
    # print("this is viewcount")
    # dataframe['viewCount'] = viewCount
    # dataframe['likeCount'] = likeCount
    # dataframe['dislikeCount'] = dislikeCount
    # dataframe['commentCount'] = commentCount
    print(dataframe)


    # return response
    #return map(int, duration_min_sec)

def mainCall():
    # start_time = time.time()
    apiKey = getApiKey("../credentials/yt-api-credentials.txt")
    getVideoStats(apiKey)

mainCall()
