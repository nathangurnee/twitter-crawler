import scrapy
import ijson
import os
import sys

class TweetURLSpider(scrapy.Spider):
  name = 'tweeturlspider'
  start_urls = ['https://google.com']

  def __init__(self, name=None, **kwargs):
      super().__init__(name, **kwargs)

  def parse(self, response):
    hello = response.css('title::text').get()
    file = open('tweeturls.txt', 'a')
    file.write(hello)

# stream the tweets from the json files (user will provide the file count)
# detect if the tweet's text contains a URL
# if it does, add it's id and url to a list

class TweetReader(object):
  def __init__(self, fileCount):
    self.fileCount = fileCount

  def streamTweets(self):
    for i in range(self.fileCount):
      fileExists = os.path.isfile('tweets/tweets_{}.json'.format(i+1))

      if not fileExists:
        print('The tweet file (tweets/tweets_{}.json) does not exist'.format(i+1))
        sys.exit(0)

      with open('tweets/tweets_{}.json'.format(i+1)) as f:
        for tweet in ijson.items(f, "item"):
          # go through all users within a tweet
          for user in tweet['includes']['users']:
            # check if the tweet contains a URL
            if 'entities' in user and 'url' in user['entities']:
              print(user['id'], user['entities']['url']['urls'][0]['expanded_url'])

if __name__ == '__main__':
  numFiles = int(input('Enter the number of JSON files that have tweets within them (only in the tweets folder, they should have the format tweets_1.json, tweets_2.json, etc.): '))

  reader = TweetReader(numFiles)
  reader.streamTweets()
