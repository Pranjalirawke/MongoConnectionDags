from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 5),
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

dag = DAG(
    'backup_mongo_data',
    default_args=default_args,
    description='Backup MongoDB data from control.brandsonroad.com',
    schedule_interval=None,
)

# Step 1: SSH into server
ssh_command = 'ssh ubuntu@control.brandsonroad.com'
ssh_operator = BashOperator(
    task_id='ssh_into_server',
    bash_command=ssh_command,
    dag=dag,
)

# Step 2: Run mongodump command
mongodump_command = 'mongodump --forceTableScan --db led --gzip --archive=mongoBackup_`date +"%Y-%m-%d.gz"`'
mongodump_operator = BashOperator(
    task_id='mongodump_command',
    bash_command=mongodump_command,
    dag=dag,
)

# Step 3: Open command prompt from F:\mongoDB
open_cmd_command = 'cd /mnt/f/mongoDB && start cmd'
open_cmd_operator = BashOperator(
    task_id='open_command_prompt',
    bash_command=open_cmd_command,
    dag=dag,
)

# Step 4: scp ubuntu@control.brandsonroad.com:mongoBackup_2021-08-02.gz ./

copy_command = 'scp ubuntu@control.brandsonroad.com:mongoBackup_2021-08-02.gz ./'
copy_operator = BashOperator(
    task_id='copy_backup_file',
    bash_command=copy_command,
    dag=dag,
)

# Step 5: ssh brodata2@192.168.7.209:/home/siladmin/mongo-db   docker ps -a  (see all  container/database)

list_containers_command = 'ssh brodata2@192.168.7.209 "cd /home/siladmin/mongo-db && docker ps -a"'
list_containers_operator = BashOperator(
    task_id='list_containers',
    bash_command=list_containers_command,
    dag=dag,
)


# Set dependencies
ssh_operator >> mongodump_operator >> open_cmd_operator >> copy_operator >> list_containers_operator 