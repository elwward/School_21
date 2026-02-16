#!/bin/sh

echo '"name","count"' > hh_uniq_positions.csv 
tail -n +2 ../ex03/hh_positions.csv | cut -d',' -f3 | tr -d '"' | tr '/ ' '\n' | sort | uniq -c   | grep -v '-' | sort -nr -t',' -k2,2 | awk '{print "\"" $2 "\",\"" $1 "\""}' >> hh_uniq_positions.csv
