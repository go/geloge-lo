#!/usr/bin/env ruby
require 'webrick'

server = WEBrick::HTTPServer.new({:BindAddress => '127.0.0.1',
                               :Port => 80})

redirector = Proc.new{|req, res|
  res.status = 302
  res['location'] = 'http://localhost:8080' + req.unparsed_uri
  res
}

server.mount_proc('/logincb', redirector) 
server.mount_proc('/login', redirector)
server.mount_proc('/incremental', redirector)

trap(:INT){server.shutdown}
server.start
