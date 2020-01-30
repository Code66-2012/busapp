#!/bin/sh
rm stops_db
./mysql2sqlite.sh abqride route_stop_map -u root -pF@t4mutant | sqlite3 stops_db
./mysql2sqlite.sh abqride stops_local -u root -pF@t4mutant | sqlite3 stops_db
./mysql2sqlite.sh abqride routes -u root -pF@t4mutant | sqlite3 stops_db
sqlite3 stops_db < sqlite_init.sql
