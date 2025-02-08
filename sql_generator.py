import os
import yaml

import psycopg2 as pg2
from loguru import logger

import markdown
import pdfkit

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import markdown2
import re

import markdown2

from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv(override=True)


class QueryGenerator:
    def __init__(self):
        self.openai_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),  
            api_version="2024-08-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")
        )
    
    def __repr__(self):
        return "Initialising Query Generator 🚀"
    
    @staticmethod
    def execute_generated_queries(sql_query, database_name="moonberg", user_name="raimeno", host="localhost"):
        db_password = os.getenv("DATABASE_PASSWORD")
        
        try:
            database_connection = pg2.connect(f"dbname='{database_name}' user='{user_name}' host='{host}' password='{db_password}'")
            logger.info("Successfully established connection to PostgreSQL server!")
        except:
            logger.error("Trouble establishing connection to PostgreSQL server")

        try:
            with database_connection.cursor() as curs:
                curs.execute(sql_query)
                fetched_results = curs.fetchall()

                return fetched_results

        except Exception as ex:
            logger.error(f"Query execution failed due to : {ex}")
        
    @staticmethod
    def read_sys_prompt(file_path="system_prompt.yaml"):
        with open(file_path) as file:
            prompt = yaml.full_load(file)

        return prompt


    @staticmethod
    def parse_markdown_table(md_text):
        tables = []
        lines = md_text.split("\n")
        table_data = []
        
        for line in lines:
            if "|" in line:  
                row = [cell.strip() for cell in line.split("|")[1:-1]] 
                if "---" not in row: 
                    table_data.append(row)
            elif table_data: 
                tables.append(table_data)
                table_data = []
        
        if table_data:
            tables.append(table_data)
        
        return tables

    @staticmethod
    def generate_business_report(markdown_text: str, output_pdf: str):
        html_content = markdown2.markdown(markdown_text)

        tables = QueryGenerator.parse_markdown_table(markdown_text)

        doc = SimpleDocTemplate(output_pdf, pagesize=letter)
        styles = getSampleStyleSheet()

        styles.add(ParagraphStyle(name="SpacingAfter", spaceAfter=12)) 
        styles.add(ParagraphStyle(name="SpacingBefore", spaceBefore=12))  

        story = []

        html_lines = html_content.split("\n")
        for line in html_lines:
            if line.strip() and not re.match(r"^\|.*\|$", line):
                story.append(Paragraph(line, styles["SpacingAfter"])) 
                story.append(Spacer(1, 10))

        for table_data in tables:
            if table_data:
                table = Table(table_data)

                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey), 
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black)
                ]))

                story.append(table)
                story.append(Spacer(1, 15)) 

        doc.build(story)
        logger.info("Generated business report 🌟")

    def text_to_query_generator(self, query):
        logger.info("Understanding user requirements and generating appropraiate user query...")
        
        system_prompt = self.read_sys_prompt()
        raw_sql_query = self.openai_client.chat.completions.create(
                            model="gpt-4o", 
                            messages=[
                                {"role": "system", "content": system_prompt["QUERY_GENERATOR_PROMPT"]},
                                {"role": "user", "content": query},
                            ]
                        )

        filtered_query = str(raw_sql_query.choices[0].message.content).replace("```", "").replace("sql", "")

        return filtered_query

    def generate_nl_responses(self, user_query, sql_response, business_report=False, pdf_output_path=None):
        nl_generator_prompt = self.read_sys_prompt()
        querry_mapping = f"{user_query} : {sql_response}"
            
        if business_report:
            natural_language_response = self.openai_client.chat.completions.create(
                                            model="gpt-4o", 
                                            messages=[
                                                {"role": "system", "content": nl_generator_prompt["NL_BR_RESPONSE_GENERATOR"]},
                                                {"role": "user", "content": querry_mapping},
                                            ]
                                        )

            filtered_response = str(natural_language_response.choices[0].message.content)
            self.generate_business_report(nl_response, pdf_output_path)

        else:
            natural_language_response = self.openai_client.chat.completions.create(
                                            model="gpt-4o", 
                                            messages=[
                                                {"role": "system", "content": nl_generator_prompt["NL_RESPONSE_GENERATOR"]},
                                                {"role": "user", "content": querry_mapping},
                                            ]
                                        )

            filtered_response = str(natural_language_response.choices[0].message.content)
        
            logger.info("Generated business insights 🌟")
        return filtered_response
    


if __name__ == "__main__":
    query="Find the Token Pair with the Highest Difference Between Buy and Sell Transactions in the Last 24 Hours"
    
    query_generator = QueryGenerator()
    
    filtered_query = query_generator.text_to_query_generator(query)

    query_results = query_generator.execute_generated_queries(filtered_query)
    
    nl_response = query_generator.generate_nl_responses(query, query_results)
    
    
    print("The sql query is: ", filtered_query)
    print("The response is: ", nl_response)

