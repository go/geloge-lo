import json
from pprint import pprint
class UserTimeline:
    def __init__(self, oauth_client):
        self.client = oauth_client

    def call(self):
        tweets = []
        query = {
            'screen_name' : 'go_chiba',
            'count' : 200
            }
        running = True
        while running:
            new_tweets = []
            try:
                self.resp = self.client.do_http_request_with_oauth('GET', 'http://twitter.com/statuses/user_timeline.json', query)
                json_obj = json.loads(self.resp.read())
                
                if len(json_obj) == 1:
                    running = False
                else:
                    oldest = json_obj.pop()
                    query['max_id'] = oldest['id']

                for tweet in json_obj:
                    new_tweets.append(tweet)

                for i in new_tweets:
                    tweets.append(i)
                    print i['text'].encode('utf-8')
            except:
                pass
