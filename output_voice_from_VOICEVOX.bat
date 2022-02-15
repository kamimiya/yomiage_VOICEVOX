@echo off
curl -s -H "Content-Type: application/json" -X POST -d @tmp/query.json localhost:50021/synthesis?speaker=%1 > tmp/tmp_voice.wav