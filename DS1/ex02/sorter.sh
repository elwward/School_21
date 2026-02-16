#!/bin/sh

{
  echo "id,created_at,name,has_test,alternate_url"
  tail -n +2 ../ex01/hh.csv | sort -t, -k2,2 -k1,1
} > hh_sorted.csv
