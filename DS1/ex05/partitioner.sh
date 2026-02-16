#!/bin/sh

tail -n +2 ../ex03/hh_positions.csv | while IFS=, read -r id created_at name has_test url; do

    date=$(echo "$created_at" | cut -d'T' -f1 | tr -d '"')

    file="${date}.csv"

    if [ ! -f "$file" ]; then
        echo '"id","created_at","name","has_test","alternate_url"' > "$file"
    fi

    echo "$id,$created_at,$name,$has_test,$url" >> "$file"

done



