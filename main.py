from fastapi import FastAPI
from pydantic import BaseModel

from sql_generator import QueryGenerator

app = FastAPI()

class Query(BaseModel):
    query: str
    
def operator(query):
    
    query_generator = QueryGenerator()
    filtered_query = query_generator.text_to_query_generator(query.query)

    query_results = query_generator.execute_generated_queries(filtered_query)    
    nl_response = query_generator.generate_nl_responses(query, query_results)
    
    return nl_response

@app.post("/databse_copilot")
def main(query: Query):
    nl_response = operator(query)
    print(nl_response)
    return {"response" : nl_response}