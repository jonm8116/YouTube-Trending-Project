from bs4 import BeautifulSoup as bs
import requests
import json
import urllib
import re
import operator
import pandas as pd
import time

#Global video list
videos=[]

class VideoResource():
    def __init__(self, title, publishedAt, viewCount, categoryId, durationMs, likeCount=0, dislikeCount=0, commentCount=0, tags=[]):
        self.title = title
        self.publishedAt = publishedAt
        self.viewCount = viewCount
        self.categoryId = categoryId
        self.durationMs = durationMs
        self.likeCount = likeCount
        self.dislikeCount = dislikeCount
        self.commentCount = commentCount
        self.tags = tags

def getApiKey(filename):
    keyfile = open(filename)
    return keyfile.readlines()[-1].rstrip()

def readFile(filename):
    dataframe = pd.read_csv()

def queryYtApi(fiftyVideoIds, api_key):
    searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+fiftyVideoIds+"&key="+api_key+"&part=statistics,snippet"
    print(searchUrl)
    return urllib.request.urlopen(searchUrl).read().decode('latin-1')

def getVideoStats(api_key):
    dataframe = pd.read_csv("../data/NonTrending-YouTube.csv")
    listofIds = dataframe['URL'].dropna()
    start_time = time.time()
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
                # print("counter " + str(counter))
            else:
                # print("Took " + str(time.time() - start_time) + " seconds.")
                response = queryYtApi(fiftyVideoIds, api_key)
                #iterate through response
                formJson = json.loads(response)
                return
                #print(formJson)
                # print("after request")

                for item in formJson['items']:
                    print("entered loop")
                    title = item['snippet']['title']
                    print(title)
                    publishedAt = item['snippet']['publishedAt']
                    viewCount = item['statistics']['viewCount']
                    categoryId = item['snippet']['categoryId']
                    durationMs = item['fileDetails']['durationMs']
                    likeCount = item['statistics']['likeCount']
                    dislikeCount = item['statistics']['dislikeCount']
                    commentCount = item['statistics']['commentCount']
                    tags = item['snippet']['tags']
                    videos.append(VideoResource(title,publishedAt,viewCount,categoryId,durationMs,likeCount=likeCount,dislikeCount=dislikeCount,commentCount=commentCount,tags=tags))
                    break

                outerCounter+=1
                print("Exit the loop " + str(outerCounter))
                counter=0
                fiftyVideoIds=""
                break


        except (IndexError, KeyError):
            continue
        # if(counter==5):
        #     break
    print(videos)
    # return response
    #return map(int, duration_min_sec)

def mainCall():
    # start_time = time.time()
    # print("This is the start time " + str(start_time))
    print("starting program..")
    apiKey = getApiKey("../credentials/yt-api-credentials.txt")
    getVideoStats(apiKey)
    print("Took " + str(time.time() - start_time) + " seconds.")

print("Before starting main call")
mainCall()
