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
def streamTweets(accessToken):
  headers = {
    'Authorization': 'Bearer {}'.format(accessToken)
  }

  tweetsResponse = requests.get(
    'https://api.twitter.com/2/tweets/sample/stream?tweet.fields=created_at&expansions=author_id&user.fields=created_at',
    headers=headers, stream=True
  )

  print(tweetsResponse.status_code)

  for tweetInfo in tweetsResponse.iter_lines():
    tweet = json.loads(tweetInfo)
    print(json.dumps(tweet, indent=2))

if __name__ == '__main__':
  with open('config.json') as json_data_file:
    config = json.load(json_data_file)

    encodedTokenSecret = getEncodedTokenSecret(config['consumerToken'], config['consumerSecret'])
    accessToken = getAccessToken(encodedTokenSecret)

    streamTweets(accessToken)
