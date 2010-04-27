#!/usr/bin/env ruby
require 'webrick'

server = WEBrick::HTTPServer.new({:BindAddress => '127.0.0.1',
                               :Port => 80})

server.mount_proc('/logincb') {|req, res|
  res.status = 302
  res['location'] = 'http://localhost:8080' + req.unparsed_uri
  #res.body=req.unparsed_uri
  res
}
server.mount_proc('/login') {|req, res|
  res.status = 302
  res['location'] = 'http://localhost:8080' + req.unparsed_uri
  #res.body=req.unparsed_uri
  res
}


trap(:INT){server.shutdown}
server.start

