from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'example_ssh_scp_and_bash_no_hook', 
    default_args=default_args, 
    schedule_interval=timedelta(days=1))

upload_script = SSHOperator(
    task_id='upload_script',
    ssh_conn_id='con_id',
    command='scp /path/to/local/script.sh user@remote_host:/path/to/remote/script.sh',
    dag=dag
)

run_script = BashOperator(
    task_id='run_script',
    bash_command='ssh user@remote_host "/path/to/remote/script.sh"',
    dag=dag
)

upload_script >> run_script
