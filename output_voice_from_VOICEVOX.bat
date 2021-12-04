@echo off
curl -s -X POST "localhost:50021/audio_query?text=%1&speaker=%2" > tmp/query.json
curl -s -H "Content-Type: application/json" -X POST -d @tmp/query.json localhost:50021/synthesis?speaker=%2 > tmp/tmp_voice.wav