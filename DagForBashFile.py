from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime,timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 8),
    'retry_delay': timedelta(minutes=1),
    'retries': 1
}

dag = DAG('Bash_operator', default_args=default_args, schedule_interval=None)

task1 = BashOperator(
    task_id='run_remote_script',
    bash_command='C:/Users/Mayur/Desktop/BashCommands.sh',
    dag=dag
)
