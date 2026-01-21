from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
from docker.types import Mount
from datetime import datetime

with DAG(
    dag_id="crawl_topcv_category_copy_and_run",
    start_date=datetime(2024, 1, 1),
    schedule_interval="0 2 * * *",
    catchup=False,
    tags=["crawler", "selenium", "topcv"],
) as dag:

    # =========================
    # Task 1: Copy code từ Windows -> /data/crawler
    # =========================
    copy_code = BashOperator(
        task_id="copy_code",
        bash_command="""
        mkdir -p /data/crawler && \
        cp /src/crawl_category_job.py /data/crawler/
        """
    )

    # =========================
    # Task 2: Run crawler (run.cmd style)
    # =========================
    crawl_topcv = DockerOperator(
        task_id="crawl_topcv",

        image="selenium-crawler",

        # giống: python crawl_category_job.py
        command="python crawl_category_job.py",

        auto_remove=True,
        api_version="auto",

        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",

        mount_tmp_dir=False,

        mounts=[
            Mount(
                source="/data/crawler",
                target="/app",
                type="bind",
            )
        ],
    )

    copy_code >> crawl_topcv
