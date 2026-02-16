#!/bin/sh

if [ -z "$1" ]; then
    echo "You must enter an argument"
    exit 1
fi

#profession=$(echo "$1" | tr ' ' '+')
#data="https://api.hh.ru/vacancies?text=$profession&per_page=20"
#curl "$data" | jq '.items[]' > hh.json

curl -G \
	--data-urlencode "text=$1" \
	--data-urlencode "per_page=20" \
	"https://api.hh.ru/vacancies" \
	| jq '.items[]' > hh.json
