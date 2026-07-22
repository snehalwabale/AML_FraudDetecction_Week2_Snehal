import time


metrics = {

    "tool_calls":0,

    "hitl_requests":0,

    "rag_queries":0,

    "total_latency":0

}



def start_timer():

    return time.time()



def record_latency(
    start_time
):

    latency = (
        time.time()
        -
        start_time
    )


    metrics[
        "total_latency"
    ] += latency


    return latency



def increment_metric(
    name
):

    if name in metrics:

        metrics[name] += 1



def get_metrics():

    return metrics