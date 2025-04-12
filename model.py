
#from transformers import AutoTokenizer, AutoModelForCausalLM
#import sqlite3
#import pandas as pd

#class DataAnalyzer:
 #   """Handles data analysis and visualization using LLM for query interpretation"""
 #   
 #   def __init__(self):
 #       self.model_name = "mistralai/Mistral-7B-Instruct-v0.1"
 #       self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
 #       self.model = AutoModelForCausalLM.from_pretrained(
 #           self.model_name,
 #           device_map="auto",
 #           torch_dtype="auto"
 #       )
 #       self.visualizer = DataVisualizer()
#        self.columns = self._get_table_info(db_path)

 #   def _get_table_info(db_path: str) -> dict:
 #    """Get table names and column names from database"""
 #    conn = sqlite3.connect(db_path)
 #    try:
 #        tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
 #        columns = {table: pd.read_sql_query(f"PRAGMA table_info({table})", conn)['name'].tolist() for table in tables['name']} 
 #        return columns
 #    finally:
 #        conn.close()     

 #   def analyze_request(self, user_input: str, db_path: str) -> plt.Figure:
 #       """Process user request using LLM and return visualization"""
 #       # Generate SQL query from natural language input
 #       sql_query = self._generate_sql_query(user_input)
 #       
 #       # Execute query and get results
 #       results = self._execute_sql_query(sql_query, db_path)
 #       
 #       # Determine visualization type based on query and results
 #       viz_type = self._determine_visualization(user_input, sql_query)
 #       
 #       return self._create_visualization(results, viz_type)
 #       
 #   def _generate_sql_query(self, user_input: str) -> str:
 #       """Generate SQL query from natural language using Mistral"""

 #
 #       schema_context = get_table_info(db_path)

 # #      schema_context = """
 # #      Available tables and columns:
 # #      - companies: code, title, industry, vertical, canton, city, year, genderCEO, oob, funded
 # #      - company_highlights: company_code, highlight_text, highlight_date
 # #      - deals: id, company_code, amount, valuation, type, phase, dateOfFundingRound
 # #      """


 #       
 #       prompt = f"""Convert this request into SQL, using the following schema:
 #       {schema_context}
 #       
 #       Request: {user_input}
 #       
 #       SQL Query:"""
 #       
 #       inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
 #       outputs = self.model.generate(
 #           **inputs,
 #           max_new_tokens=200,
 #           do_sample=True,
 #           temperature=0.7,
 #           top_p=0.95
 #       )
 #       
 #       generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
 #       return generated_text.split("SQL Query:")[-1].strip()
 #       
 #   def _execute_sql_query(self, sql_query: str, db_path: str) -> pd.DataFrame:
 #       """Execute SQL query and return results as DataFrame"""
 #       conn = sqlite3.connect(db_path)
 #       try:
 #           results = pd.read_sql_query(sql_query, conn)
 #       finally:
 #           conn.close()
 #       return results
 #       
 #   def _determine_visualization(self, user_input: str, sql_query: str) -> str:
 #       """Determine appropriate visualization type using LLM"""
 #       prompt = f"""
 #       Based on this user request and SQL query, what type of visualization would be most appropriate?
 #       Options: time_series, comparison, distribution, geographic
 #       
 #       User request: {user_input}
 #       SQL query: {sql_query}
 #       
 #       Visualization type:"""
 #       
 #       inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
 #       outputs = self.model.generate(
 #           **inputs,
 #           max_new_tokens=50,
 #           do_sample=False
 #       )
 #       
 #       viz_type = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
 #       return viz_type.split("Visualization type:")[-1].strip()
 #       
 #   def _create_visualization(self, data: pd.DataFrame, viz_type: str) -> plt.Figure:
 #       """Create appropriate visualization based on data and type"""
 #       fig = plt.figure(figsize=(12, 8))
 #       
 #       if viz_type == 'time_series':
 #           plt.plot(data.index, data.values)
 #           plt.xticks(rotation=45)
 #           
 #       elif viz_type == 'comparison':
 #           plt.bar(range(len(data)), data.values)
 #           plt.xticks(range(len(data)), data.index, rotation=45)
 #           
 #       elif viz_type == 'distribution':
 #           sns.histplot(data=data)
 #           
 #       elif viz_type == 'geographic':
 #           # Assuming geographic data is available
 #           sns.scatterplot(data=data, x='longitude', y='latitude')
 #           
 #       plt.tight_layout()
 #
 #       return fig
# data_analyzer = DataAnalyzer()

#user_input = input("Enter your request: ")
#db_path = "path/to/your/database.db"
#fig = data_analyzer.analyze_request(user_input, db_path)
# fig.show()





















