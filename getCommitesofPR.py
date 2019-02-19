from github import Github
from utils import *
import sys
import getopt

NBtestsPasAJour = 0
NBtestsMalEcrit = 0
NBcodeAjouteMauvais = 0
NBcodeAjouteMarche = 0


def main(argv):
    repo_name = ''
    inputfile = ''
    helpMsg = "test.py -r <github/repo> -i <inputfile>"
    try:
        opts, args = getopt.getopt(argv, "hr:i:", ["repo=", "ifile="])
    except getopt.GetoptError:
        print(helpMsg)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(helpMsg)
            sys.exit()
        elif opt in ("-r", "--repo"):
            repo_name = arg
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    if repo_name == '' or inputfile == '':
        print(helpMsg)
        sys.exit(2)

    print("start get commits of pull")
    g = Github("9517082cce9860b93b7117f40989b1a92de39de9")
    repo = g.get_repo(repo_name)
    with open(inputfile, "r") as ins:
        for line in ins:
            commits = get_commits(g, repo, int(line))
            hisCodeIsBad(commits, int(line))
    print("----------------------resultat:--------------------")
    print("NBtestsPasAJour:" + str(NBtestsPasAJour) + " NBtestsMalEcrit:" + str(NBtestsMalEcrit) +
          " NBcodeAjouteMauvais:" + str(NBcodeAjouteMauvais) + " NBcodeAjouteMarche:" + str(NBcodeAjouteMarche))


def get_commits(g, repo, numeroPull):
    myCommits = []
    pr = repo.get_pull(numeroPull)
    commits = pr.get_commits()
    i = 0
    for c in commits:
        status = "good"
        filesModified = []
        wait_limit_reset(g, 100)
        for f in c.files:
            filesModified.append(f.filename)
        if is_build_fail(c):
            status = "error"
            if i is not 0 and myCommits[i-1]["status"] == "error":
                myCommits[i - 1]["files"].extend(filesModified)
                continue
        myCommits.append({"status": status, "files": filesModified})
        i += 1
    return myCommits


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


def hisCodeIsBad(commits, pullrequest):
    print("####" + str(pullrequest))
    global NBtestsPasAJour
    global NBtestsMalEcrit
    global NBcodeAjouteMauvais
    global NBcodeAjouteMarche
    for i in range(len(commits) - 1):
        if commits[i]["status"] == "error":
            if testsPasMisAJour(commits[i]["files"], commits[i+1]["files"]):
                NBtestsPasAJour += 1
                print("Tests pas mis à jour")
            if testsMalEcrit(commits[i]["files"], commits[i+1]["files"]):
                NBtestsMalEcrit += 1
                print("Tests mal écrit")
            CAD2 = False
            if i != 0:
                CAD2 = codeAjouteDefectueux2(
                    commits[i-1]["files"], commits[i]["files"], commits[i+1]["files"])
            if codeAjouteDefectueux(commits[i]["files"], commits[i+1]["files"]) or CAD2:
                NBcodeAjouteMauvais += 1
                print("Le code ajouter contient des erreurs")
            CAM2 = False
            if i != 0:
                CAM2 = codeAjouteMarche2(
                    commits[i-1]["files"], commits[i]["files"], commits[i+1]["files"])
            if codeAjouteMarche(commits[i]["files"], commits[i+1]["files"]) or CAM2:
                NBcodeAjouteMarche += 1
                print(
                    "Le code ajouter ne contient pas erreurs mais produit des erreurs dans le reste du system")


if __name__ == "__main__":
    main(sys.argv[1:])
