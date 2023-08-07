from utils.livepeer.serverless import orchestrator_performance_status

orchestrators_with_status =orchestrator_performance_status()

low_performing_orchestrators = []

for key, val in orchestrators_with_status.items():
    if val == "Low":
        low_performing_orchestrators.append(key)
    else:
        continue




print(low_performing_orchestrators)



