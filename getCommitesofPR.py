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
    testPasJour = False
    for element in array1:
        for element2 in array2:
            if (element[0:-5] in element2):
                if("Test" in element or "Test" in element2):
                    testPasJour = True
    return testPasJour


def testsMalEcrit(array1, array2):
    testMalEcrit = False
    for element in array1:
        for element2 in array2:
            if (element == element2):
                if("Test" in element):
                    testMalEcrit = True
    return testMalEcrit


def testsMalEcrit2(array1):
    testMalEcrit = True
    for element in array1:
        if("Test" not in element):
            testMalEcrit = False
    return testMalEcrit


def codeAjouteDefectueux(array1, array2):
    same = False
    for element in array1:
        for element2 in array2:
            if (element == element2):
                same = True
    return same


def codeAjouteMarche(array1, array2):
    same = True
    for element in array1:
        for element2 in array2:
            if (element == element2):
                same = False
    return same


NBtestsPasAJour = 0
NBtestsMalEcrit = 0
NBcodeAjouteMauvais = 0
NBcodeAjouteMarche = 0


def hisCodeIsBad(pullrequest):
    print("####"+str(pullrequest))
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
            if testsMalEcrit(myCommits[i]["files"], myCommits[i+1]["files"]) or testsMalEcrit2(myCommits[i]["files"]):
                NBtestsMalEcrit += 1
                print("Tests mal écrit")
            if codeAjouteDefectueux(myCommits[i]["files"], myCommits[i+1]["files"]):
                NBcodeAjouteMauvais += 1
                print("Le code ajouter contient des erreurs")
            if codeAjouteDefectueux(myCommits[i]["files"], myCommits[i+1]["files"]):
                NBcodeAjouteMarche += 1
                print(
                    "Le code ajouter ne contient pas erreurs mais produit des erreurs dans le reste du system")
    # print("----------------------resultat:--------------------")
    #print("NBtestsPasAJour:" + str(NBtestsPasAJour) + " NBtestsMalEcrit:"+ str(NBtestsMalEcrit) + " NBcodeAjouteMauvais:"+ str(NBcodeAjouteMauvais) + " NBcodeAjouteMarche:"+ str(NBcodeAjouteMarche))


# hisCodeIsBad(2924)

run()
