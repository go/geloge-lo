import sys
import json
import pprint
import os

class DictWrapper:
    def __init__(self, json_obj):
        self.json_obj = json_obj

    def __get_value(self, data, key):
        return data.get(key)

    def get_value(self, *key):
        data = self.json_obj
        for k in key:
            if data == None:
                return data
            data = self.__get_value(data, k)
        return data
    
class Friends(DictWrapper):
    def friends(self):
        return self.get_value('friends')


class Tweet(DictWrapper):
    def text(self):
        return self.get_value('text')

    def tid(self):
        return self.get_value('id')

    def lat(self):
        coordinates = self.get_value('coordinates', 'coordinates')
        if coordinates:
            return coordinates[0]
        return None

    def lng(self):
        coordinates = self.get_value('coordinates', 'coordinates')
        if coordinates:
            return coordinates[1]
        return None

    def uid(self):
        return self.get_value('user', 'id')

    def screen_name(self):
        return self.get_value('user', 'screen_name')

    def created_at(self):
        return self.get_value('created_at')

class UserStream:
    def __init__(self, oauth_client, logger = None):
        self.url = 'http://betastream.twitter.com/2b/user.json'
        self.client = oauth_client

    def logging(self, message):
        if not self.logger:
            return
        self.logger.write()
        
    def call(self):
        print "calling you-"
        self.resp = self.client.do_http_request_with_oauth('POST',self.url)
        print self.resp
        for line in self.resp:
            if line == "\n":
                continue

            obj = self.parse_line(line)
            yield obj

    def close(self):
        if self.resp:
            self.resp.close()
            
    def parse_line(self, jsonstr):
        try:
            data = json.loads(jsonstr)
        except Exception,e:
            return None
        obj = None
        if data.has_key('text'):
            obj = Tweet(data)
        elif data.has_key('friends'):
            obj = Friends(data)
        else:
            obj = DictWrapper(data)

        return obj
