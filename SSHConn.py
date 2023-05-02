from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 5, 2),
    'depends_on_past': False,
    'retries': 1
}

with DAG('mongo_backup_transfer', default_args=default_args, schedule_interval=None) as dag:

    ssh_to_server = BashOperator(
        task_id='ssh_to_server',
        bash_command='ssh ubuntu@control.brandsonroad.com',
        dag=dag
    )

    backup_mongo = BashOperator(
        task_id='backup_mongo',
        bash_command='mongodump --forceTableScan --db led --gzip --archive=mongoBackup_`date +"%Y-%m-%d.gz"`',
        dag=dag
    )

    list_files = BashOperator(
        task_id='list_files',
        bash_command='ll',
        dag=dag
    )

    ssh_to_local = BashOperator(
        task_id='ssh_to_local',
        bash_command='cd F:mongoDB',
        dag=dag
    )

    copy_to_local = BashOperator(
        task_id='copy_to_local',
        bash_command='scp ubuntu@control.brandsonroad.com:mongoBackup_{{ ds }}.gz ./',
        dag=dag
    )

    ssh_to_docker = BashOperator(
        task_id='ssh_to_docker',
        bash_command='ssh brodata2@192.168.7.209:/home/siladmin/mongo-db',
        dag=dag
    )

    copy_to_docker = BashOperator(
        task_id='copy_to_docker',
        bash_command='scp ./mongoBackup_{{ ds }}.gz brodata2@192.168.7.209:/home/siladmin/mongo-db',
        dag=dag
    )

    docker_ps = BashOperator(
        task_id='docker_ps',
        bash_command='docker ps -a',
        dag=dag
    )

    ssh_to_server >> backup_mongo >> list_files >> ssh_to_local >> copy_to_local >> ssh_to_docker >> copy_to_docker >> docker_ps