from datetime import datetime
from typing import List
import uuid


from fastapi import FastAPI, UploadFile, File


from app.models import (
    ChatRequest,
    HealthResponse,
    AMLResponse
)


from app.memory import (
    add_message,
    clear_memory
)


from app.chains import (
    run_chat,
    run_retrieve
)


from app.logger import log_interaction


from app.tools import (
    ingest_documents,
    get_sources,
    delete_source,
    run_evaluation
)



from mcp.api import router as mcp_router
from hitl.api import router as hitl_router
from prompt_manager.api import router as prompt_router
from rbac.api import router as rbac_router



app = FastAPI(

    title="AML & Fraud Detection Co-Pilot",

    version="Week 8"

)



# Week 8 Modules

app.include_router(mcp_router)

app.include_router(hitl_router)

app.include_router(prompt_router)

app.include_router(rbac_router)



START_TIME = datetime.now()





@app.get("/")

def root():

    return {

        "project":
        "AML & Fraud Detection Co-Pilot",

        "status":
        "Running",

        "version":
        "Week 8"

    }







@app.get(

    "/health",

    response_model=HealthResponse

)

def health():


    uptime=datetime.now()-START_TIME


    return {


        "status":"healthy",


        "uptime":str(uptime),


        "model":"gpt-4o-mini",


        "version":"Week 8"

    }








@app.post("/reset")

def reset(session_id:str=""):


    clear_memory(

        session_id if session_id else None

    )


    return {


        "success":True,


        "message":
        "Conversation memory cleared"

    }









@app.post(

    "/chat",

    response_model=AMLResponse

)

def chat(req:ChatRequest):


    try:


        session_id=req.session_id


        if not session_id:

            session_id=str(uuid.uuid4())



        add_message(

            session_id,

            "user",

            req.message

        )



        result=run_chat(

            req.message,

            session_id

        )



        add_message(

            session_id,

            "assistant",

            result.response

        )



        log_interaction(

            session_id=session_id,

            query=req.message,

            response=result.response,

            tool_used=result.tool_used

        )


        return result



    except Exception as e:



        return AMLResponse(

            response=f"Internal Error : {str(e)}",

            risk_score=0,

            risk_level="LOW",

            action="Retry",

            tool_used="ERROR",

            intent="error",

            recommendation="Check logs",

            decision="Failed",

            evidence=[],

            citations=[],

            retrieval_trace=[]

        )









@app.post("/retrieve")

def retrieve(

    query:str,

    top_k:int=5

):


    return run_retrieve(

        query,

        top_k

    )









@app.post("/ingest")

async def ingest(

    files:List[UploadFile]=File(...)

):


    job_id=str(uuid.uuid4())


    return ingest_documents(

        files,

        job_id

    )









@app.get("/ingest/status/{job_id}")

def ingest_status(job_id:str):


    return {


        "job_id":job_id,


        "status":"completed"

    }









@app.get("/sources")

def sources():


    return get_sources()










@app.delete("/sources/{doc_id}")

def remove_source(doc_id:str):


    return delete_source(

        doc_id

    )









@app.post("/evaluate")

def evaluate():


    return run_evaluation()