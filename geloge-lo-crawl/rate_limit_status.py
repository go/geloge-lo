import json
import time
class RateLimitStatus:
    def __init__(self, oauth_client):
        self.client = oauth_client

    def call(self):
        self.resp = self.client.do_http_request_with_oauth('GET', 'http://api.twitter.com/1/account/rate_limit_status.json')
        json_obj = json.loads(self.resp.read())
        print json_obj
        if json_obj['remaining_hits'] == 0:
            print(time.asctime(time.localtime(json_obj['reset_time_in_seconds'])))
            print("api limit!!")
        import sys
        sys.exit()
        

