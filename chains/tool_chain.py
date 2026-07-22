from langchain_core.runnables import RunnableLambda

import time

from app.tools import (

    analyze_transactions,
    screen_name,
    get_risk_score,
    transaction_velocity,
    counterparties,
    previous_alerts,
    typology,
    filing_deadline,
    enhanced_due_diligence,
    jurisdiction_check,
    str_fields,
    ultimate_beneficial_owner,
    alert_summary,
    investigation_timeline,
    escalation_memo

)

from chains.base import BaseChain

from mcp.client import invoke_mcp_tool



def execute_tool(tool, params):

    start = time.time()

    try:

        result = tool.invoke(params)

        duration = round(
            (time.time() - start) * 1000,
            2
        )

        return result, duration


    except Exception as e:

        return {

            "error": str(e)

        }, 0





def extract_risk_evidence(data):

    evidence=[]

    if isinstance(data, dict):

        for key,value in data.items():

            if key in [

                "risk",
                "risk_level",
                "risk_score",
                "indicators",
                "matches",
                "typologies"

            ]:

                evidence.append({

                    "field":key,

                    "value":value

                })


    return evidence





def run_investigation(question):

    result = {}

    trace=[]


    tools=[

        (
            "risk",
            get_risk_score,
            {
                "customer":question
            }
        ),

        (
            "sanctions",
            screen_name,
            {
                "name":question
            }
        ),

        (
            "transactions",
            analyze_transactions,
            {
                "query":question
            }
        ),

        (
            "alerts",
            previous_alerts,
            {
                "query":question
            }
        ),

        (
            "ubo",
            ultimate_beneficial_owner,
            {
                "query":question
            }
        ),

        (
            "typology",
            typology,
            {
                "query":question
            }
        )

    ]



    for name,tool,params in tools:


        output,time_taken = execute_tool(

            tool,

            params

        )


        result[name]=output


        trace.append({

            "tool":name,

            "execution_time_ms":time_taken

        })



    return result,trace





def tool_node(inputs):


    intent = inputs.get(
        "intent",
        ""
    )


    question = inputs.get(
        "question",
        ""
    )


    citations=[]

    trace=[]

    evidence=[]


    try:


        if intent=="investigation":


            output,trace = run_investigation(

                question

            )


        elif intent=="risk":


            output,_ = execute_tool(

                get_risk_score,

                {
                    "customer":question
                }

            )



        elif intent=="screen":


            output,_ = execute_tool(

                screen_name,

                {
                    "name":question
                }

            )


            try:


                mcp = invoke_mcp_tool(

                    "sanctions_screening",

                    {
                        "customer":question
                    }

                )


                output["mcp_screening"]=mcp


            except Exception as e:


                output["mcp_status"] = str(e)




        elif intent=="transactions":


            output,_ = execute_tool(

                analyze_transactions,

                {
                    "query":question
                }

            )



        elif intent=="velocity":


            output,_ = execute_tool(

                transaction_velocity,

                {
                    "query":question
                }

            )



        elif intent=="counterparty":


            output,_ = execute_tool(

                counterparties,

                {
                    "query":question
                }

            )



        elif intent=="alerts":


            output,_ = execute_tool(

                previous_alerts,

                {
                    "query":question
                }

            )



        elif intent=="typology":


            output,_ = execute_tool(

                typology,

                {
                    "query":question
                }

            )



        elif intent=="deadline":


            output,_ = execute_tool(

                filing_deadline,

                {
                    "query":question
                }

            )



        elif intent=="edd":


            output,_ = execute_tool(

                enhanced_due_diligence,

                {
                    "query":question
                }

            )



        elif intent=="jurisdiction":


            output,_ = execute_tool(

                jurisdiction_check,

                {
                    "query":question
                }

            )



        elif intent=="str":


            output,_ = execute_tool(

                str_fields,

                {
                    "query":question
                }

            )



        elif intent=="ubo":


            output,_ = execute_tool(

                ultimate_beneficial_owner,

                {
                    "query":question
                }

            )



        elif intent=="summary":


            output,_ = execute_tool(

                alert_summary,

                {
                    "query":question
                }

            )



        elif intent=="timeline":


            output,_ = execute_tool(

                investigation_timeline,

                {
                    "query":question
                }

            )



        elif intent=="memo":


            output,_ = execute_tool(

                escalation_memo,

                {
                    "query":question
                }

            )


        else:


            output={

                "message":
                "No tool required"

            }



        evidence = extract_risk_evidence(

            output

        )



        trace.append({

            "stage":"completed",

            "intent":intent

        })



        return {

            "tool_output":output,

            "citations":citations,

            "trace":trace,

            "evidence":evidence

        }



    except Exception as e:


        return {

            "tool_output":{

                "error":str(e)

            },

            "citations":[],

            "trace":[

                {

                    "stage":"failed",

                    "error":str(e)

                }

            ],

            "evidence":[]

        }





tool_chain = BaseChain(

    RunnableLambda(tool_node)

)