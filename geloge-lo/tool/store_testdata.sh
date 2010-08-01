#!/bin/bash
curl -d '{"id": 1, "name":"Testdesu", "screen_name": "test"}' http://localhost:8080/internal/read_user_from_json
for i in `seq 10 59`; do
    curl -d "{\"text\": \"test\", \"created_at\": \"Sat Jul 31 23:19:${i} +0000 2010\", \"coordinates\": {\"coordinates\": [${i},${i}]}, \"id\": ${i}, \"user\": {\"id\": 1, \"screen_name\": \"test_user\"}}" http://localhost:8080/internal/read_tweet_from_json
done
echo
