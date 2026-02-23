from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Query
from client.rq_client import queue
from queues.worker import process_query

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/chat")
def chat(
    query: str = Query(
        ...,
        description="The query to process",
    ),
):
    job = queue.enqueue(process_query, query)
    return {"job_id": job.get_id(), "status": job.get_status()}


@app.get("/result/{job_id}")
def get_job_result(
    job_id: str = Query(
        ...,
        description="The ID of the job to check",
    ),
):
    job = queue.fetch_job(job_id)
    result = job.return_value()
    if job is None:
        return {"error": "Job not found"}
    elif job.is_finished:
        return {"result": result}
    elif job.is_failed:
        return {"error": "Job failed"}
    else:
        return {"status": "Job is still processing"}
