@echo off
curl -s -X POST "localhost:50021/audio_query?text=%1&speaker=%2" > tmp/query.json