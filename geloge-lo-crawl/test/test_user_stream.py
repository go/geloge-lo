#coding: utf-8
import sys
import os
import unittest

sys.path.append(os.path.realpath(os.path.dirname( os.path.realpath( __file__ )) + '/../'))
import user_stream

class TestDictWrapper(unittest.TestCase):
    def setUp(self):
        pass
    def test_get_value(self):
        dw = user_stream.DictWrapper({'a':'b'})
        self.assertEqual(dw.get_value('a'), 'b')
        self.assertEqual(dw.get_value('b'), None)
        
    def test_get_value_rec(self):
        dw = user_stream.DictWrapper({'a': {'b': 'ok'}})
        self.assertEqual(dw.get_value('a'), {'b': 'ok'})
        self.assertEqual(dw.get_value('a', 'b'), 'ok')
        self.assertEqual(dw.get_value('a', 'c', 'd'), None)
        self.assertEqual(dw.get_value('a', 'c', 'd', 'e'), None)
        
class TestUserStream(unittest.TestCase):
    def setUp(self):
        self.user_stream = user_stream.UserStream(None, None)

    def test_parse_line(self):
        tweet_str = '''{"truncated":false,"text":"\u660e\u3089\u304b\u306b\u8ca7\u4e4f\u304f\u3058\u3059\u304e\uff3c(^o^)\uff0f","coordinates":null,"place":null,"in_reply_to_screen_name":null,"source":"web","geo":null,"in_reply_to_user_id":null,"favorited":false,"in_reply_to_status_id":null,"created_at":"Fri Jul 23 06:51:05 +0000 2010","user":{"show_all_inline_media":false,"lang":"ja","profile_use_background_image":true,"followers_count":586,"profile_image_url":"http://a1.twimg.com/profile_images/853227017/tw_icon_normal.jpg","contributors_enabled":false,"following":null,"friends_count":701,"location":"\u611b\u77e5\u306e\u897f\u306e\u7aef\u21d4\u76db\u5ca1\u306e\u5317\u306e\u65b9","geo_enabled":false,"profile_background_color":"9ae4e8","screen_name":"goto_h","favourites_count":151,"description":"\u3078\u3063\u307d\u3053\u5927\u5b66\u751f/\u3078\u3063\u307d\u3053DJ\u3002zippie\u3002\u6020\u60f0\u306a\u65e5\u3005\u3002\u304a\u83d3\u5b50\u62c5\u5f53\u3002\u30d5\u30a9\u30ed\u30fc/\u30ea\u30e0\u30fc\u30d6\u306f\u3054\u81ea\u7531\u306b\u3002\u307e\u307e\u30fc\u308a\u307e\u307e\u30fc\u308a\u3002fave:\u68ee\u535a\u55e3/\u5869\u91ce\u4e03\u751f/\u5ca1\u5d8b\u4e8c\u4eba/\u6d0b\u697d/\u30cd\u30c3\u30c8\u30ef\u30fc\u30af/\u30bb\u30ad\u30e5\u30ea\u30c6\u30a3/Mac/\u5c01\u795e\u6f14\u6280/\u304a\u83d3\u5b50\u4f5c\u308a/\u6c34\u3069\u3046/\u7f8e\u8853\u9928\u5de1\u308a/\u30b9\u30a4\u30d5\u30c8/MT","verified":false,"profile_text_color":"000000","follow_request_sent":null,"time_zone":"Tokyo","url":"http://iddy.jp/profile/goto_h/","notifications":null,"profile_link_color":"0000ff","profile_background_image_url":"http://s.twimg.com/a/1279649509/images/themes/theme1/bg.png","protected":false,"created_at":"Tue Apr 17 19:18:01 +0000 2007","profile_sidebar_fill_color":"e0ff92","name":"goto_h","listed_count":null,"profile_background_tile":false,"id":5031281,"statuses_count":9929,"utc_offset":32400,"profile_sidebar_border_color":"87bc44"},"id":19319391433,"contributors":null}'''
        tweet = self.user_stream.parse_line(tweet_str)
        self.assertEqual(tweet.text(), u"明らかに貧乏くじすぎ＼(^o^)／")
        self.assertEqual(tweet.tid(), 19319391433)
        self.assertEqual(tweet.uid(), 5031281)
        self.assertEqual(tweet.screen_name(), 'goto_h')
        self.assertEqual(tweet.lat(), None)
        self.assertEqual(tweet.lng(), None)
        self.assertEqual(tweet.created_at(), "Fri Jul 23 06:51:05 +0000 2010")

        friends_str = '''{"friends":[106960234,116181613,111552081,104825864,42807898,110946451,106423999,98843721,50895367,5031281,115015713,64370156,108819802,17919343,16611656,110405126,98406437,83079946,90089024,62562922,63394880,131095851,62459412,27244954,20347991,18160311,106693607,7653412,14071573,97447508,140039488,19586865,131096179,63447201,44940172,131080037,149067639,108812865,76903408,88440367,110622593]}'''
        friends = self.user_stream.parse_line(friends_str)
        self.assertEqual(friends.friends(), 
                         [106960234,116181613,111552081,104825864,42807898,110946451,106423999,
                          98843721,50895367,5031281,115015713,64370156,108819802,17919343,16611656,
                          110405126,98406437,83079946,90089024,62562922,63394880,131095851,62459412,
                          27244954,20347991,18160311,106693607,7653412,14071573,97447508,140039488,
                          19586865,131096179,63447201,44940172,131080037,149067639,108812865,76903408,88440367,110622593])

if __name__ == '__main__':
    unittest.main()
