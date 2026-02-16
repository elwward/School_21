#!/bin/sh

echo '"id","created_at","name","has_test","alternate_url"' > all.csv

for csv in *.csv; do
	if [ "$csv" = "all.csv" ]; then continue; fi
    	tail -n +2 "$csv" >> all.csv

done
