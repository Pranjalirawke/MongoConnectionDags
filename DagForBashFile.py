from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 4),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG('ssh_operator', 
	default_args=default_args, 
	schedule_interval=None, 
	catchup=False) as dag:

    connect_to_aws = SSHOperator(
        task_id='connect_to_aws',
        ssh_conn_id='conn_id',  # SSH connection ID for your AWS instance
        command='echo "Connected to AWS."'
        
    )

    run_bash_script = SSHOperator(
        task_id='run_bash_script',
        ssh_conn_id='conn_id',  # SSH connection ID for your AWS instance
        bash_command='bash BashCommands.sh'  
        
    )

    connect_to_aws >> run_bash_script
