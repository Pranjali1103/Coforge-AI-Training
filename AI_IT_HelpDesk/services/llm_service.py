from models.helpdesk_model import HelpdeskRequest
from graph.helpdesk_graph import helpdesk_graph

def process_helpdesk_request(request:HelpdeskRequest):
    inital_state={
        "employeeId":request.employeeId,
        "employeeName":request.employeeName,
        "issue":request.issue,

        "category":"",
        "priority":"",

        "resolution":[],
        "toolsCalled":[],

        "reviewStatus":"Not Reviewed",
        "reviewReason":"",

        "ticketId":None,
        "status":"Pending",

        "finalResponse":{}

    }
    result=helpdesk_graph.invoke(inital_state)
    return result["finalResponse"]