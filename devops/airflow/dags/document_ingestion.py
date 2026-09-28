"""
Apache Airflow DAG: Scheduled Document Ingestion Pipeline.
ASD&D Exp 12: Workflow Automation using Directed Acyclic Graphs (DAGs).
"""
from datetime import datetime, timedelta

try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator

    default_args = {
        'owner': 'campusmind',
        'depends_on_past': False,
        'start_date': datetime(2026, 1, 1),
        'email_on_failure': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    }

    def scan_new_documents():
        print("Scanning data/sample_documents for incoming PDFs...")

    def compute_integrity_checksums():
        print("Computing CRC32 and SHA-256 checksums on newly discovered documents...")

    def generate_embeddings():
        print("Extracting document chunks and vectorizing via ChromaDB...")

    with DAG(
        'campusmind_document_pipeline',
        default_args=default_args,
        description='Automated syllabus and notes ingestion DAG',
        schedule_interval=timedelta(days=1),
        catchup=False,
    ) as dag:

        t1 = PythonOperator(
            task_id='scan_documents',
            python_callable=scan_new_documents,
        )

        t2 = PythonOperator(
            task_id='verify_checksums',
            python_callable=compute_integrity_checksums,
        )

        t3 = PythonOperator(
            task_id='embed_and_index',
            python_callable=generate_embeddings,
        )

        t1 >> t2 >> t3
except ImportError:
    # Allows repository to run in standalone dev mode without requiring full Airflow server
    pass
