#/bin/bash

if [ -z "$ADVENT_SESSION" ]
then
  echo "\$ADVENT_SESSION is empty"
  exit 1
fi

if [ -z "$1" ]
then
  echo "\$please specify day number"
  exit 1
fi

echo "Le 1er paramètre est : $1"


curl "https://adventofcode.com/2024/day/$1/input" \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: max-age=0' \
  -H "cookie: _ga=GA1.2.1123142468.1733050974; _gid=GA1.2.1900221213.1733050974; session=$ADVENT_SESSION; _ga_MHSNPJKWC7=GS1.2.1733050974.1.1.1733051004.0.0.0" \
  -H 'priority: u=0, i' \
  -H 'sec-ch-ua: "Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: none' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' \
  > ../ressources/day$1.txt 
