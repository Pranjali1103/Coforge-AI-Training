from fastapi import FastAPI
from models.customer_model import CustomerRequest,CustomerResponse
from services.customer_service import analyze_customer_feedback
from workflow.customer_workflow import workflow_graph
app=FastAPI(
    title="AI Customer Feedback Analyzer"
)

@app.get("/description")
def getApplicationName():
    return{
        "application":"AI Customer Feedback Analyzer",
        "description":"It analyzes customer feedback and generate response"
    }

@app.get("/helath")
def getHealth():
    return "Application is working"

@app.post("/api/v1/analyze-feedback",response_model=CustomerResponse)
def analyze_feedback(request:CustomerRequest):

    result=workflow_graph.invoke({
        "customer_id":request.customer_id,
        "customer_name":request.customer_name,
        "order_id":request.order_id,
        "rating":request.rating,
        "feedback":request.feedback
    })
    return CustomerResponse(
        customer_id=result["customer_id"],
        sentiment=result["sentiment"],
        issue_category=result["issue_category"],
        priority=result["priority"],
        reply=result["reply"],
        status=result["status"]

    )
    



    # result=analyze_customer_feedback(request)
    # return result