from github import Github

# First create a Github instance:

# or using an access token
g = Github("9517082cce9860b93b7117f40989b1a92de39de9 ")

repo = g.get_repo("SonarSource/sonarqube")
pulls = repo.get_pulls(state='open', sort='created', base='master')

for pr in pulls:
    print(pr.number)

pull=repo.get_pull(2651)

commits=pull.get_commits()
for c in commits:
    print(c)