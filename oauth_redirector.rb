#!/usr/bin/env ruby
require 'webrick'

server = WEBrick::HTTPServer.new({:BindAddress => '127.0.0.1',
                               :Port => 80})

server.mount_proc('/authcallbacktest') {|req, res|
  res.status = 302
  res['location'] = 'http://geloge-lo.appspot.com:8080' + req.unparsed_uri
  #res.body=req.unparsed_uri
  res
}

trap(:INT){server.shutdown}
server.start

