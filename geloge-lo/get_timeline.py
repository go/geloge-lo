from google.appengine.ext.webapp.util import run_wsgi_app
from gelotter.statuses import user_timeline
import cgi

def application ( environ, start_response ):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    form = cgi.FieldStorage(fp=environ['wsgi.input'], 
                            environ=environ)
    if not form.has_key('uid'):
        return "please input uid"
    

    tls = user_timeline(form['uid'].value)

    # TODO use stringio
    response_str = ""
    for tl in tls:
        response_str += tl[u'text'].encode('utf-8') + "\n"
    return response_str


def main ():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
