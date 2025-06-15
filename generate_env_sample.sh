#!/bin/bash

# Check if .env exists
if [[ ! -f .env ]]; then
  echo ".env file not found!"
  exit 1
fi

# Generate .env.sample
echo "Generating .env.sample..."
awk -F= '
  NF && $1 !~ /^#/ {
    printf("%s=\n", $1)
  }
  /^#/ || NF==0 {
    print
  }
' .env > .env.sample

echo ".env.sample created successfully."

