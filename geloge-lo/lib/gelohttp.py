
def redirect_to(start_response, to_url):
    start_response('302 Found', 
                   [('Content-Type', 'text/html; charset=UTF-8'), 
                    ('Location', to_url)])
    return '''<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>301 Moved</TITLE></HEAD><BODY>
<H1>301 Moved</H1>
The document has moved
<A HREF="%s">here</A>.
</BODY></HTML>''' % to_url

def get_requested_url(environ):
    return '%s://%s%s' % (environ['wsgi.url_scheme'], environ['HTTP_HOST'], environ['PATH_INFO'])
    
def redirect_login_url(start_response, environ):
    login_url = 'http://geloge-lo.appspot.com/login?return_to=%s' % get_requested_url(environ)
    return redirect_to(start_response, login_url)
