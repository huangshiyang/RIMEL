from github import Github


def is_build_fail(commit):
    status = c.get_statuses()
    for s in status:
        if s.context == "continuous-integration/travis-ci/pr" and s.state == "failure":
            return True
    return False


g = Github("9517082cce9860b93b7117f40989b1a92de39de9")

repo = g.get_repo("SonarSource/sonarqube")
pull_requests = repo.get_pulls(state='closed', base='master')


merged_pull_requests = filter(lambda pr: pr.is_merged(), pull_requests)

had_failed_pull_requests = []

for pr in merged_pull_requests:
    commits = pr.get_commits()
    for c in commits:
        if is_build_fail(c):
            print("pull request #", pr.number, " is added")
            had_failed_pull_requests.append(pr)
            break

print(len(had_failed_pull_requests))
