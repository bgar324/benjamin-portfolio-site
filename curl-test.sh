#!/bin/bash

BASE_URL="http://127.0.0.1:5000/api/timeline_post"
RANDOM_ID="$(date +%s)"
NAME="Test User $RANDOM_ID"
EMAIL="test$RANDOM_ID@example.com"
CONTENT="Random timeline post $RANDOM_ID"

echo "Creating timeline post..."

POST_RESPONSE=$(curl -s -X POST "$BASE_URL" \
  -d "name=$NAME" \
  -d "email=$EMAIL" \
  -d "content=$CONTENT")

echo "$POST_RESPONSE"

echo
echo "Checking that the post exists..."

GET_RESPONSE=$(curl -s "$BASE_URL")

if echo "$GET_RESPONSE" | grep -Fq "$CONTENT"; then
  echo "PASS: Timeline post was added."
  exit 0
else
  echo "FAIL: Timeline post was not found."
  echo "$GET_RESPONSE"
  exit 1
fi