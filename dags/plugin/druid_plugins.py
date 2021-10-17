import json

from airflow import AirflowException
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.sensors.http_sensor import HttpSensor
from airflow.plugins_manager import AirflowPlugin


class DruidJobOperator(SimpleHttpOperator):
    """
    Custom operator for Druid OLAP population APIs.
    """

    def execute(self, context):
        job_response = super(DruidJobOperator, self).execute(context)
        if job_response:
            livy_job_id = json.loads(job_response).get('task')
            context['task_instance'].xcom_push('druid_task_id', livy_job_id)
        else:
            AirflowException('Failed to execute spark job')


class DruidJobSensor(HttpSensor):
    """
    Custom sensor for Druid OLAP population API status checks.
    """

    def poke(self, context):
        response = self.hook.run(self.endpoint,
                                 data=self.request_params,
                                 headers=self.headers,
                                 extra_options=self.extra_options)
        self.log.info(response.json()['status'])
        status = response.json().get('status').get('status')
        if status.lower() in ['failed']:
            raise AirflowException('Druid data load status failed')
        return True if status.lower() == 'success' else False


class DruidPlugins(AirflowPlugin):
    name = "druid_plugins"
    DEFAULT_PLUGIN = "1.0"
    operators = [DruidJobOperator]
    sensors = [DruidJobSensor]
