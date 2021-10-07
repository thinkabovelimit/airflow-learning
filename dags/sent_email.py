from datetime import timedelta

from airflow import DAG
from airflow.operators.email_operator import EmailOperator
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
    'email_send',
    default_args=default_args,
    description='Dag to send email to an id',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['example'],
) as dag:

    email = EmailOperator(
        task_id='send_email',
        to='kkrishnaprasad.mec@gmail.com',
        subject='Airflow Alert',
        html_content="""<h3>Email Test</h3>""",
        dag=dag

    )

email
