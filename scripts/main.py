import csv
import datetime
from crewai import Agent, Task, Crew, Process

# 1. SETUP
local_llm = 'ollama/phi3'

# 2. DEFINE THE AGENTS
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

# 3. INITIALIZE THE REPORT FILE
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
report_filename = f"Fleet_Compliance_Report_{timestamp}.txt"

with open(report_filename, "w") as report_file:
    report_file.write("===============================================\n")
    report_file.write("BUREAU VERITAS: AUTOMATED COMPLIANCE REPORT\n")
    report_file.write(f"Generated on: {datetime.datetime.now()}\n")
    report_file.write("===============================================\n\n")

print(f"\n--- BATCH STARTING: Results will be saved to {report_filename} ---")

# 4. READ CSV AND PROCESS
with open('fleet_data.csv', mode='r') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        name = row['ship_name']
        gt = row['tonnage']
        fuel = row['fuel_consumed']
        
        print(f"\n>>> ANALYZING: {name} <<<")
        
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
        
        # 5. SAVE TO FILE (The "Professional Touch")
        with open(report_filename, "a", encoding="utf-8") as report_file:
            report_file.write(f"SHIP NAME: {name}\n")
            report_file.write(f"TONNAGE: {gt} GT\n")
            report_file.write(f"FUEL CONSUMED: {fuel} Tons\n")
            report_file.write("-" * 30 + "\n")
            report_file.write(f"ANALYSIS RESULT:\n{result}\n")
            report_file.write("\n" + "="*50 + "\n\n")

print(f"\n--- SUCCESS! Final report saved as: {report_filename} ---")