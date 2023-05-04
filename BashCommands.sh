#!/bin/bash

# 1. open cmd

ssh ubuntu@control.brandsonroad.com << EOF

mongodump --forceTableScan --db led --gzip --archive=mongoBackup_`date +"%Y-%m-%d.gz"`

ll

EOF

scp ubuntu@control.brandsonroad.com:mongoBackup_2021-08-02.gz ./

ssh brodata2@192.168.7.209:/home/siladmin/mongo-db << EOF

docker ps -a

docker ps

cd ..

cd siladmin/

ls

cd mongo-db

docker-compose down

docker volume ls

docker volume rm <volume name>

EOF

docker cp F:/mongo/filename.gz container_name:/path/to/destination


scp Filename brodata2@192.168.7.209:/home/siladmin/mongo-db

brodata2@192.168.7.209:/home/siladmin/mongo-db

scp .\mongoBackup_2022-07-29.gz siladmin@192.168.7.209:~/mongo-db/mongoBackup.gz

ll

mv Filename.gz mongoBackup.gz

docker-compose up -d

cd ..cd ..

docker ps
