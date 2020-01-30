#!/bin/sh
rm google_transit.zip
wget http://data.cabq.gov/transit/gtfs/google_transit.zip
rm *.txt
unzip google_transit.zip
mysqldump -u root -pF@t4mutant -v abqride > backup.sql
mysql -u root -pF@t4mutant -e "DROP DATABASE abqride"
mysql -u root -pF@t4mutant -e "CREATE DATABASE abqride"
mysql -u root -pF@t4mutant abqride < schema.sql
mv stop_times.txt times.txt
for i in "routes" "calendar" "shapes" "times" "stops" "trips"
do
cols=$(head -n 1 $i.txt)
mysqlimport -u root -pF@t4mutant abqride $i.txt --columns $cols --ignore-lines=1 -L --fields-terminated-by=',' --fields-optionally-enclosed-by='"' --lines-terminated-by='\n'
done
NOW=$(TZ=America/Denver date +"%Y%m%d")
mysql -u root -pF@t4mutant -e "DELETE FROM abqride.calendar WHERE end_date < $NOW"
mysql -u root -pF@t4mutant -e "DELETE FROM abqride.calendar WHERE start_date > $NOW"
mysql -u root -pF@t4mutant abqride < misc.sql
