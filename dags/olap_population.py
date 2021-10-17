import json
from datetime import timedelta
from airflow.models import Variable
from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.utils.dates import days_ago

from plugin.druid_plugins import DruidPlugins, DruidJobSensor, DruidJobOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),

}
payload = Variable.get('druid_test', deserialize_json=True)
with DAG(
        'populate_data',
        default_args=default_args,
        description='Airflow dags to execute bash commands',
        schedule_interval=timedelta(days=1),
        start_date=days_ago(2),
        tags=['example'],
) as dag:
    populate_data = SimpleHttpOperator(
        http_conn_id='druid_api',
        task_id='data_population',
        endpoint='druid/indexer/v1/task',
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        method='POST',
    )
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    print(populate_data.response_check)
    status_cehck=DruidJobSensor(
        http_conn_id='druid_api',
        task_id='check_job_status',
        endpoint=' http://localhost:8888/druid/indexer/v1/task/index_parallel_Downloads_dfdjchmb_2021-10-11T07:35:31.007Z/status'

    )

    populate_data
