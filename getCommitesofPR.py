from github import Github
from utils import *
import sys
import getopt
import getFileChangedLine as gfch

NBtestsPasAJour = 0
NBtestsMalEcrit = 0
NBcodeAjouteMauvais = 0
NBcodeAjouteMarche = 0

NBcommits = 0
NBcommitsError = 0

nb_addition_res = 0
nb_deletion_res = 0
nb_addition_and_deletion_res = 0
nb_import_added_res = 0
nb_modif_res = 0


def transform_files_comparing(res):
    nb_addition_res = res[0]
    nb_deletion_res = res[1]
    nb_addition_and_deletion_res = res[2]
    nb_import_added_res = res[3]
    nb_modif_res = res[4]



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
            res = gfch.files_comparing(repo, int(line))
            transform_files_comparing(res)
    print("----------------------resultat:--------------------")
    print("NBtestsPasAJour:" + str(NBtestsPasAJour) + " NBtestsMalEcrit:" + str(NBtestsMalEcrit) +
          " NBcodeAjouteMauvais:" + str(NBcodeAjouteMauvais) + " NBcodeAjouteMarche:" + str(NBcodeAjouteMarche))
    print("NBcommits:" + str(NBcommits) +
          " NBcommitsError:" + str(NBcommitsError))
    print("nb_addition_res:", nb_addition_res, " nb_deletion_res:", nb_deletion_res, " nb_addition_and_deletion_res:", nb_addition_and_deletion_res, " nb_import_added_res:" , nb_import_added_res, " nb_modif_res:" , nb_modif_res )

def get_commits(g, repo, numeroPull):
    myCommits = []
    pr = repo.get_pull(numeroPull)
    commits = pr.get_commits()
    i = 0
    for c in commits:
        status = "good"
        number = 1
        filesModified = []
        wait_limit_reset(g, 100)
        for f in c.files:
            filesModified.append(f.filename)
        if is_build_fail(c):
            status = "error"
            if i is not 0 and myCommits[i-1]["status"] == "error":
                number += 1
                myCommits[i - 1]["files"].extend(filesModified)
                continue
        myCommits.append({"status": status, "files": filesModified, "number": number})
        i += 1
    return myCommits


# Commit_Error : files [ x.java, v.java] ---> Commit_Good : files [x.test ]
def testsPasMisAJour(array1, array2):
    for element in array1:
        for element2 in array2:
            if element[0:-5] in element2 and ("Test" in element or "Test" in element2):
                return True
    return False

# Commit_Error : files [x.test, v.test] ---> Commit_Good : files [ x.test ]
def testsMalEcrit(array1, array2):
    for element in array1:
        for element2 in array2:
            if element == element2 and "Test" in element:
                return True
    return False

# Commit_Error : files [x.java, v.java] ---> Commit_Good : files [ x.java ]
def codeAjouteDefectueux(array1, array2):
    for element in array1:
        for element2 in array2:
            if element == element2:
                return True
    return False

# Commit_Good : files [x.java, o.java] ---> Commit_Error : files [x.test, v.test, o.test] ---> Commit_Good : files [x.java]
def codeAjouteDefectueux2(before, errorCommit, after):
    for element in errorCommit:
        if not "Test" in element:
            return False
    return codeAjouteDefectueux(before, after)

# Commit_Error : files [x.java , v.java] ---> Commit_Good : files [ o.java ]
def codeAjouteMarche(array1, array2):
    for element in array1:
        for element2 in array2:
            if element == element2:
                return False
    return True

# Commit_Good : files [x.java, o.java] ---> Commit_Error : files [x.test, v.test, o.test] ---> Commit_Good : files [v.java]
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
    global NBcommits
    global NBcommitsError
    for i in range(len(commits) - 1):
        NBcommits += commits[i]["number"]
        if commits[i]["status"] == "error":
            NBcommitsError += commits[i]["number"]
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
