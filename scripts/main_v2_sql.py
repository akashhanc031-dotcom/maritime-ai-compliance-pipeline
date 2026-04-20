import sqlite3
import datetime
from crewai import Agent, Task, Crew, Process

# 1. LLM SETUP
local_llm = 'ollama/phi3'

# 2. AGENT DEFINITIONS
auditor = Agent(
  role='Maritime Data Verifier',
  goal='Determine if a ship is regulated under EU ETS (Threshold: 5000 GT)',
  backstory='Senior inspector at Bureau Veritas. Expert in EU MRV laws.',
  llm=local_llm,
  verbose=True
)

analyst = Agent(
  role='Carbon Emissions Analyst',
  goal='Calculate 40% carbon phase-in for 2024 using a 3.114 factor.',
  backstory='Technical analyst. Expert in maritime carbon allowance math.',
  llm=local_llm,
  verbose=True
)

# 3. PREPARE THE OUTPUT FILE
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
report_filename = f"SQL_Migration_Report_{timestamp}.txt"

with open(report_filename, "w") as report_file:
    report_file.write("===============================================\n")
    report_file.write("BUREAU VERITAS: SQL-DRIVEN COMPLIANCE REPORT\n")
    report_file.write(f"Source Database: maritime_fleet.db\n")
    report_file.write(f"Generated: {datetime.datetime.now()}\n")
    report_file.write("===============================================\n\n")

# 4. DATABASE QUERY (The SQL Integration)
conn = sqlite3.connect('maritime_fleet.db')
cursor = conn.cursor()

# Execute SQL to fetch all ship data
cursor.execute("SELECT ship_name, tonnage, fuel_consumed FROM ships")
ship_records = cursor.fetchall()

print(f"\n🚀 SQL PIPELINE ACTIVE: Processing {len(ship_records)} vessels from database...")

# 5. LOOP THROUGH SQL RECORDS
for record in ship_records:
    name, gt, fuel = record  # Unpacking the SQL row
    
    print(f"\n>>> PROCESSING FROM SQL: {name} <<<")
    
    t1 = Task(
        description=f"Analyze {name} ({gt} GT). Is it regulated by EU ETS?",
        agent=auditor,
        expected_output="Exempt or Regulated status."
    )
    
    t2 = Task(
        description=f"Calculate 2024 allowances for {name} with {fuel} tons of fuel.",
        agent=analyst,
        expected_output="Final CO2 allowance calculation."
    )

    crew = Crew(agents=[auditor, analyst], tasks=[t1, t2], process=Process.sequential)
    result = crew.kickoff()
    
    # SAVE INDIVIDUAL RESULT TO FILE
    with open(report_filename, "a", encoding="utf-8") as report_file:
        report_file.write(f"VESSEL: {name}\n")
        report_file.write(f"DATABASE DATA: {gt} GT | {fuel} Tons Fuel\n")
        report_file.write(f"AGENT DETERMINATION:\n{result}\n")
        report_file.write("\n" + "="*50 + "\n\n")

conn.close()
print(f"\n✅ PIPELINE COMPLETE! Final report saved to: {report_filename}")