from github import Github

print("start get commits of pull")
g = Github("9517082cce9860b93b7117f40989b1a92de39de9")
repo = g.get_repo("SonarSource/sonarqube")
myCommits = []

def is_build_fail(commit):
    status = commit.get_statuses()
    for s in status:
        if s.context == "continuous-integration/travis-ci/pr" and s.state == "failure":
            return True
    return False


def get_commits(numeroPull):
    pr = repo.get_pull(numeroPull)
    commits = pr.get_commits()
    for c in commits:
        status = "good"
        filesModified = []
        if is_build_fail(c):
            status = "error"
        for f in c.files:
            filesModified.append(f.filename)
        myCommits.append({"commite":c,"status":status,"files":filesModified})
    return myCommits


def run():
    with open("had_failed_pull_requests_number.txt", "r") as ins:
        for line in ins:
            print(get_commits((int(line))))

def oneElementIsSame(array1, array2):
    same = False
    for element in array1:
        for element2 in array2:
            if (element == element2):
                same = True
    return same

def hisCodeIsBad(pullrequest):
    get_commits(pullrequest)
    for i in range(len(myCommits)):
        if(myCommits[i]["status"] == "error"):
            if(i < len(myCommits)):
                print(myCommits[i]["commite"])
                if oneElementIsSame(myCommits[i]["files"],myCommits[i+1]["files"]) :              
                    print("L'erreur a été corriger, elle a été possiblement causé par le code ajouté")
                else :
                    print("L'erreur ne vient pas du code ajouté")


hisCodeIsBad(2924)


print("end")

#for i in range(len(myCommits)):
#    print(myCommits[i])


