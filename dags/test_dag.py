# This is a test dag file
import os
import time
import logging
from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator

from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['viktor.opdebeke@4finance.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}


def task_function(s):
    logging.info("Task is starting")
    print("Task is starting")
    condition = True
    count = 0
    while condition:
        logging.info("Running iteration: {s}")
        print("Running iteration: {s}")
        logging.info("Current count: {count}")
        print("Current count: {count}")
        time.sleep(30)
        count += 1
        if count > 6:
            condition = False
    logging.info("Exiting task")
    print("Exiting task")


dag = DAG(
    'viktor_test',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(minutes=20)
)

t = PythonOperator(python_callable=task_function, op_args=[
                    "testing"],
                    task_id="task_1",
                    dag=dag)
