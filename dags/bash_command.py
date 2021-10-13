from datetime import timedelta
from textwrap import dedent

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),

}

with DAG(
        'bash_command',
        default_args=default_args,
        description='Airflow dags to execute bash commands',
        schedule_interval=timedelta(days=1),
        start_date=days_ago(2),
        tags=['example'],
) as dag:
    t1 = BashOperator(
        task_id='print_date1',
        bash_command='date'

    )

    t2 = BashOperator(
        task_id='sleep_5_seconds',
        bash_command='sleep 5'
    )
    t3 = BashOperator(
        task_id='print_date2',
        bash_command='date'

    )
    t4 = BashOperator(
        task_id='print_date3',
        bash_command='date'

    )

    t1 >> t2 >> [t3, t4]
