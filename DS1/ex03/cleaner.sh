#!/bin/sh

echo '"id","created_at","name","has_test","alternate_url"' > hh_positions.csv
tail -n +2 ../ex02/hh_sorted.csv | while IFS= read line; do

	part1=$(echo "$line" | awk -v n=1 'BEGIN{FPAT="([^,]+)|(\"[^\"]+\")"} {print $n}')
        part2=$(echo "$line" | awk -v n=2 'BEGIN{FPAT="([^,]+)|(\"[^\"]+\")"} {print $n}')
        part3=$(echo "$line" | awk -v n=3 'BEGIN{FPAT="([^,]+)|(\"[^\"]+\")"} {print $n}')
        part4=$(echo "$line" | awk -v n=4 'BEGIN{FPAT="([^,]+)|(\"[^\"]+\")"} {print $n}')
        part5=$(echo "$line" | awk -v n=5 'BEGIN{FPAT="([^,]+)|(\"[^\"]+\")"} {print $n}')
	
	part3=$(echo "$part3" | sed 's/^"//; s/"$//')

	correct=$(echo "$part3" | grep -oiE 'Senior|Junior\+?|Middle\+?|Intern' | paste -sd/ -)
	
	if [ -z "$correct" ]; then
		correct='-'
	fi

	echo "$part1,$part2,\"$correct\",$part4,$part5" >> hh_positions.csv

done
