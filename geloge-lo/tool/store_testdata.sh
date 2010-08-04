#!/bin/bash
curl -d '{"id": 1, "name":"Testdesu1", "screen_name": "test_1"}' http://localhost:8080/internal/read_user_from_json
curl -d '{"id": 2, "name":"Testdesu2", "screen_name": "test_2"}' http://localhost:8080/internal/read_user_from_json

for i in `seq 10 59`; do
    curl -d "{\"text\": \"geotagged ${i}\", \"created_at\": \"Sat Jul 31 23:19:${i} +0000 2010\", \"coordinates\": {\"coordinates\": [${i},${i}]}, \"id\": ${i}, \"user\": {\"id\": 1, \"screen_name\": \"test_1\"}}" http://localhost:8080/internal/read_tweet_from_json
    curl -d "{\"text\": \"not geotagged ${i}\", \"created_at\": \"Sat Jul 31 23:19:${i} +0000 2010\", \"coordinates\": null, \"id\": 1${i}, \"user\": {\"id\": 2, \"screen_name\": \"test_2\"}}" http://localhost:8080/internal/read_tweet_from_json
done
echo
