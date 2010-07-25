import urllib2
import urllib
import time
import urlparse
import hmac, hashlib
import os
import random
import pickle
import re

class OAuthTokenError(Exception): pass
class OAuthTokenExpiredError(Exception): pass

class OAuthToken:
    def __init__(self, token, token_secret):
        self.token = token
        self.token_secret = token_secret

    def dump(self, filename):
        self.filename = filename
        f = open(self.filename, 'w')
        pickle.dump(self, f)
    
    def remove(self):
        os.unlink(self.filename)

    @classmethod
    def load(self, filename):
        f = open(filename, 'r')
        token = pickle.load(f)
        token.filename = filename
        return token

class OAuthConfig:
    def __init__(self, realm, consumer_key, consumer_secret, request_token_url, oauth_token_url, oauth_authorize_url, oauth_file):
        self.realm = realm
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.request_token_url = request_token_url
        self.oauth_token_url = oauth_token_url
        self.request_auth_url_base = oauth_authorize_url
        self.oauth_file = oauth_file

class OAuthClient:
    def __init__(self, oauth_config):
        self.oauth_token = None

        self.config = oauth_config

        if os.path.exists(self.config.oauth_file):
            self.oauth_token = OAuthToken.load(self.config.oauth_file)            

    @classmethod
    def code_input_stdin_callback(self, url):
        print 'please access and confirm'
        print url
        print 'input code and enter'
        code = raw_input()
        return code

    def do_oauth(self, code_callback):
        if self.oauth_token:
            return None

        print 'oauth requesting'
        self.get_request_token()
        code = code_callback(self.request_auth_url)
        self.get_token(code)
        print self.oauth_token
        self.oauth_token.dump(self.config.oauth_file)

    def get_request_token(self):
        query = self._get_oauth_param('HMAC-SHA1')
        query['oauth_callback'] = 'oob'
        query['oauth_lang_pref'] = 'en-us'
        query['oauth_signature'] = self._get_oauth_signature('POST',self.config.request_token_url, query)
        
        querystr = urllib.urlencode(query)
        try:
            resp = urllib2.urlopen(self.config.request_token_url,data=querystr)
            request_token = urlparse.parse_qs(resp.read())
            self.request_token = OAuthToken(request_token['oauth_token'][0],
                                            request_token['oauth_token_secret'][0])

            if request_token.has_key('xoauth_request_auth_url'):
                self.request_auth_url = request_token['xoauth_request_auth_url'][0]
            else:
                self.request_auth_url = self.config.request_auth_url_base + '?oauth_token=' + self.request_token.token
        except urllib2.HTTPError, e:
            print e.info()
            print e.read()
        
    def get_token(self, code):
        query = self._get_oauth_param('HMAC-SHA1')
        query['oauth_verifier'] = code
        query['oauth_token'] = self.request_token.token
        query['oauth_signature'] = self._get_oauth_signature('POST',self.config.request_token_url, query)
        
        querystr = urllib.urlencode(query)
        try:
            resp = urllib2.urlopen(self.config.oauth_token_url,data=querystr)
            resp_obj = urlparse.parse_qs(resp.read())
            token = OAuthToken(resp_obj['oauth_token'][0],
                               resp_obj['oauth_token_secret'][0])
            self.oauth_token = token
            return token
        except urllib2.HTTPError, e:
            print e.info()
            return None

    def _get_oauth_param(self, signature_method):
        param = {}
        param['oauth_nonce'] = str(random.getrandbits(64))
        param['oauth_timestamp'] = int(time.time())
        param['oauth_consumer_key'] = self.config.consumer_key
        param['oauth_signature_method'] = signature_method
        param['oauth_version'] = '1.0'
        return param

    def _get_oauth_signature(self, method, url, oauth_query, original_query = {}):
        query = {}
        query.update(original_query)
        query.update(oauth_query)
        
        queries = []
        for k in sorted(query.keys()):
            queries.append('='.join([k,self.quote(str(query[k]))]))
            
        basestr = '&'.join([method, self.quote(url), self.quote('&'.join(queries))])
        token_secret = ''
        if self.oauth_token:
            token_secret = self.oauth_token.token_secret
        key = self.config.consumer_secret + '&' + token_secret
        return hmac.new(key, basestr, hashlib.sha1).digest().encode('base64').strip()

    def _get_authorization_header(self, header_query):
        header_values = []
        for k in header_query:
            header_values.append('='.join([k,self.double_quote(self.quote(str(header_query[k])))]))

        header_values.append('realm=' + self.double_quote(self.config.realm))

        value = 'OAuth ' + ', '.join(header_values)
        header = {
            'Authorization' : value
            }
        return header

    def quote(self, str, safe=''):
        return urllib.quote(str, safe='')

    def double_quote(self, str):
        return '"' + str + '"'

    def build_http_get_url(self, url, query):
        if len(query.keys()) > 0:
            return url + '?' + urllib.urlencode(query)
        else:
            return url

    def do_http_request(self, method, url, param={}, header={}):
        if method == 'GET':
            url = self.build_http_get_url(url, param)
            param = None
        else:
            param = urllib.urlencode(param)

        req = urllib2.Request(url, param, header)
        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            header = e.info()
            auth_result = header.get('WWW-Authenticate')
            if auth_result:
                match_result = re.match('.*?oauth_problem="(.+?)".*', auth_result)
                if match_result:
                    if match_result.groups()[0] == 'token_expired':
                        raise OAuthTokenExpiredError, header
                    else:
                        raise OAuthTokenError, header

            print header
            print e.read()
            raise e
            
        return resp

    def do_http_request_with_oauth(self, method, url, param={}, header={}):
        oauth_query = self._get_oauth_param('HMAC-SHA1')
        oauth_query['oauth_token'] = self.oauth_token.token
        signature = self._get_oauth_signature(method, url, oauth_query, param)
        
        header_query = {}
        header_query.update(oauth_query)
        header_query['oauth_signature'] = signature
        header = self._get_authorization_header(header_query)

        try:
            return self.do_http_request(method, url, param, header)
        except OAuthTokenExpiredError:
            self.oauth_token.remove()
            self.request_token = None
            self.oauth_token = None
            self.do_oauth(self.code_input_stdin_callback)
            self.do_http_request(method, url, param, header)
