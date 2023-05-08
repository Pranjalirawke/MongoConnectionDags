#!/bin/bash

# Connect to remote server
ssh ubuntu@control.brandsonroad.com 

cd ~
mongodump --forceTableScan --db led --gzip --archive=mongoBackup_$(date +"%Y-%m-%d.gz")
ll
cd F:mongoDB
scp ubuntu@control.brandsonroad.com:mongoBackup_2021-08-02.gz ./
ssh brodata2@192.168.7.209 '/home/siladmin/mongo-db'
docker ps -a
docker ps
cd ..
cd siladmin/
ls
cd mongo-db
docker-compose down
docker volume ls
docker volume rm <volume name> #replace the volume name
cd ..
cd ..
scp F:mongo/Filename brodata2@192.168.7.209:/home/siladmin/mongo-db #replace the filename
ssh brodata2@192.168.7.209 '/home/siladmin/mongo-db'
scp .\mongoBackup_2022-07-29.gz siladmin@192.168.7.209:~/mongo-db/mongoBackup.gz
ll
mv Filename.gz mongoBackup.gz #replce the filenam
docker-compose up -d
cd ..
cd ..
docker ps

