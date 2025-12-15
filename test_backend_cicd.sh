#!/bin/bash
#test_backend.sh

URL="http://localhost/cicd/api/health"

echo "Testataan backend /api/health..."

response=$(curl -s $URL)

if [[ $response == *"ok"* ]]; then
  echo "Backend is healthy ✅"
  exit 0
else
  echo "Backend test FAILED ❌"
  echo "Response: $response"
  exit 1
fi