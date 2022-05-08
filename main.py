import requests
import json
import base64

# encode the consumer token and secret in base64 format
def getEncodedTokenSecret(consumerToken, consumerSecret):
  consumerTokenSecret = '{}:{}'.format(consumerToken, consumerSecret)
  encodedConsumerTokenSecret = base64.b64encode(bytes(consumerTokenSecret, 'utf-8'))

  return encodedConsumerTokenSecret.decode('utf-8')

# get an access token from the base64 encoded consumer token secret
def getAccessToken(encodedTokenSecret):
  headers = {
    'Authorization': 'Basic {}'.format(encodedTokenSecret)
  }

  accessTokenResponse = requests.post(
    'https://api.twitter.com/oauth2/token?grant_type=client_credentials',
    headers=headers
  )

  return accessTokenResponse.json()['access_token']

# get the tweets using the api key
def streamTweets(accessToken,filename,filesize):
  headers = {
    'Authorization': 'Bearer {}'.format(accessToken)
  }

  tweetsResponse = requests.get(
    'https://api.twitter.com/2/tweets/sample/stream?tweet.fields=created_at&expansions=author_id&user.fields=created_at',
    headers=headers, stream=True
  )

  print(tweetsResponse.status_code)

  for tweetInfo in tweetsResponse.iter_lines():
    try:
      tweet = json.loads(tweetInfo)
      print(json.dumps(tweet, indent=2),file=filename)
      if filename.tell() > filesize: # ensure file caps around 10 Mb
        return
    except ValueError:
      return

if __name__ == '__main__':
  max_file_size = 10000000 # 10 Mb
  tweets_file_path = 'tweets/tweets2.txt' # file to hold tweets

  with open('config.json') as json_data_file:
    config = json.load(json_data_file)

    encodedTokenSecret = getEncodedTokenSecret(config['consumerToken'], config['consumerSecret'])
    accessToken = getAccessToken(encodedTokenSecret)

    with open(tweets_file_path,'a') as tweets:
      streamTweets(accessToken,tweets,max_file_size)