from github import Github

# clauses :

# code qui

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
    global myCommits
    myCommits = []
    pr = repo.get_pull(numeroPull)
    commits = pr.get_commits()
    for c in commits:
        status = "good"
        filesModified = []
        if is_build_fail(c):
            status = "error"
        for f in c.files:
            filesModified.append(f.filename)
        myCommits.append(
            {"commite": c, "status": status, "files": filesModified})
    return myCommits


def run():
    with open("had_failed_pull_requests_number.txt", "r") as ins:
        for line in ins:
            hisCodeIsBad(int(line))
    print("----------------------resultat:--------------------")
    print("NBtestsPasAJour:" + str(NBtestsPasAJour) + " NBtestsMalEcrit:" + str(NBtestsMalEcrit) +
          " NBcodeAjouteMauvais:" + str(NBcodeAjouteMauvais) + " NBcodeAjouteMarche:" + str(NBcodeAjouteMarche))


def testsPasMisAJour(array1, array2):
    for element in array1:
        for element2 in array2:
            if element[0:-5] in element2 and ("Test" in element or "Test" in element2):
                return True
    return False


def testsMalEcrit(array1, array2):
    for element in array1:
        for element2 in array2:
            if element == element2 and "Test" in element:
                return True
    return False


def codeAjouteDefectueux(array1, array2):
    for element in array1:
        for element2 in array2:
            if element == element2:
                return True
    return False


def codeAjouteDefectueux2(before, errorCommit, after):
    for element in errorCommit:
        if not "Test" in element:
            return False
    return codeAjouteDefectueux(before, after)


def codeAjouteMarche(array1, array2):
    for element in array1:
        for element2 in array2:
            if element == element2:
                return False
    return True


def codeAjouteMarche2(before, errorCommit, after):
    for element in errorCommit:
        if not "Test" in element:
            return False
    return codeAjouteMarche(before, after)


NBtestsPasAJour = 0
NBtestsMalEcrit = 0
NBcodeAjouteMauvais = 0
NBcodeAjouteMarche = 0


def hisCodeIsBad(pullrequest):
    print("####" + str(pullrequest))
    get_commits(pullrequest)
    global NBtestsPasAJour
    global NBtestsMalEcrit
    global NBcodeAjouteMauvais
    global NBcodeAjouteMarche
    for i in range(len(myCommits) - 1):
        if(myCommits[i]["status"] == "error"):
            if testsPasMisAJour(myCommits[i]["files"], myCommits[i+1]["files"]):
                NBtestsPasAJour += 1
                print("Tests pas mis à jour")
            if testsMalEcrit(myCommits[i]["files"], myCommits[i+1]["files"]):
                NBtestsMalEcrit += 1
                print("Tests mal écrit")
            CAD2 = False
            if i != 0:
                CAD2 = codeAjouteDefectueux2(
                    myCommits[i-1]["files"], myCommits[i]["files"], myCommits[i+1]["files"])
            if codeAjouteDefectueux(myCommits[i]["files"], myCommits[i+1]["files"]) or CAD2:
                NBcodeAjouteMauvais += 1
                print("Le code ajouter contient des erreurs")
            CAM2 = False
            if i != 0:
                CAM2 = codeAjouteMarche2(
                    myCommits[i-1]["files"], myCommits[i]["files"], myCommits[i+1]["files"])
            if codeAjouteMarche(myCommits[i]["files"], myCommits[i+1]["files"]) or CAM2:
                NBcodeAjouteMarche += 1
                print(
                    "Le code ajouter ne contient pas erreurs mais produit des erreurs dans le reste du system")
    # print("----------------------resultat:--------------------")
    #print("NBtestsPasAJour:" + str(NBtestsPasAJour) + " NBtestsMalEcrit:"+ str(NBtestsMalEcrit) + " NBcodeAjouteMauvais:"+ str(NBcodeAjouteMauvais) + " NBcodeAjouteMarche:"+ str(NBcodeAjouteMarche))


# hisCodeIsBad(2924)

run()
