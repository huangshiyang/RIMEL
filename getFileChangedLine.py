from github import Github
import time
from datetime import datetime


print("start")
g = Github("9517082cce9860b93b7117f40989b1a92de39de9")

repo = g.get_repo("SonarSource/sonarqube")
pull_requests = repo.get_pull(1496)
file = pull_requests.get_files()[0]
print(file.patch)

print("end")
