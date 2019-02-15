from github import Github
import re


print("start")
g = Github("9517082cce9860b93b7117f40989b1a92de39de9")


addition_res = False
deletion_res = False
addition_and_deletion_res = False
import_added_res = False
modif_res = False


def get_files(pull_requests_nb):
    repo = g.get_repo("apache/incubator-heron")
    pull_requests = repo.get_pull(pull_requests_nb)
    files = pull_requests.get_files()
    files_list = []
    for file in files:
        files_list.append(file)
    return files_list


def files_comparing(pull_requests_nb):
    files_list = get_files(pull_requests_nb)
    repo = g.get_repo("apache/incubator-heron")
    pull_request = repo.get_pull(pull_requests_nb)
    commits = pull_request.get_commits()
    for c in commits:
        print("#####")
        files_list = c.files
        i = 0
        global addition_res
        global deletion_res
        global addition_and_deletion_res
        global import_added_res
        global modif_res
        addition_res = False
        deletion_res = False
        addition_and_deletion_res = False
        import_added_res = False
        modif_res = False
        for file in files_list:
            file_content = file.patch
            if i == 0 or i == 1:
                # print(file_content)
                addition = file_only_addition(file_content)
                if addition:
                    addition_res = True
                import_file = file_import_added(file_content)
                if import_file:
                    import_added_res = True
                deletion = file_only_deletion(file_content)
                if deletion:
                    deletion_res = True
                both = file_addition_and_deletion(file_content)
                if both:
                    addition_and_deletion_res = True
                modif = file_modified_function(file_content)
                if modif:
                    modif_res = True
                i += 1
                print("File " + str(file.filename) + " has additions = " + str(addition_res) + ", has deletions = " + str(deletion_res) + ", both = " +
                      str(addition_and_deletion_res) + ", has added imports = " + str(import_added_res) + " and has modifieded functions  = " + str(modif_res))


# doesn't take in the account whether it is an import or not
def file_only_addition(file):
    tab = []
    tab = file.split('\n')
    addition = False
    for i in range(0, len(tab)):
        ligne = tab[i]
        if (ligne[0] == "-"):
            return False
        if (ligne[0] == "+"):
            addition = True
# if ligne_modif:
    if addition:
        return True
    return False


def file_only_deletion(file):
    tab = []
    tab = file.split('\n')
    deletion = False
    for i in range(0, len(tab)):
        ligne = tab[i]
        if (ligne[0] == "+"):
            return False
        if (ligne[0] == "-"):
            deletion = True
    if deletion:
        return True
    return False


def file_addition_and_deletion(file):
    tab = []
    tab = file.split('\n')
    addition = False
    deletion = False
    for i in range(0, len(tab)):
        ligne = tab[i]
        if (ligne[0] == "-"):
            deletion = True
        if (ligne[0] == "+"):
            addition = True
    if addition and deletion:
        return True


def file_import_added(file):
    tab = []
    tab = file.split('\n')
    import_ = False
    for ligne in tab:
        ligne = ligne.split(" ")
        if (len(ligne) > 1):
            if (ligne[0] == "+import" or (len(ligne) > 2 and (ligne[0] == "+" and ligne[1] == "import"))):
                return True
    return False


def file_modified_function(file):
    tab = []
    tab = file.split('\n')
    ligne_modif = -1
    for i in range(0, len(tab)):
        ligne = tab[i]
        if (ligne[0] == ("+" or "-")):
            ligne_modif = if_function_modified(tab, i)
    if ligne_modif == -1:
        return False
    return True


def if_function_modified(file_tab, ligne_nb):
    # print("**********************************")

    size_of_indentation = count_indentation(file_tab, ligne_nb)
    #print("size_of_indentation : " + str(size_of_indentation))
    #   print(file_tab[size_of_indentation])
    # only if indentation is bigger that 2 it can be part of function body
    if size_of_indentation < 5:
        #print(" NO FUCNTION")
        return False

    # if definition of the function just have been added/deleted then it can't be modification
    if_fn_def = if_function_def(file_tab[ligne_nb])
    if if_fn_def:
        # print("false")
        return False

    # checking previous lignes till the one that has smaller indentation
    index_file = ligne_nb-1
    for i in range(1, ligne_nb):
        size_indent = count_indentation(file_tab, index_file)
        if (size_indent != size_of_indentation):
            fn_def = if_function_def(file_tab[index_file])
            if (fn_def):
                print("FOUND MEEEEEEE")
                return index_file
            else:
                return -1
        index_file -= 1
    return -1


# modification in differetn method
# def modified_different_method(file_older, file_current):
def if_function_def(ligne):
    words = ligne.split()
    if (ligne[0] == ("+" or "-")):
        if (len(words) > 1 and (words[1] == ("public" or "private")) and (words[len(words)-1] == "{")):
            return True
    return False


def count_indentation(file_tab, ligne_nb):
    ligne = file_tab[ligne_nb]
    # print(ligne)
    words = ligne.split(" ")
    #print("len(words)  " + str(len(words)))
    size_of_indentation = -1
    for i in range(2, 10):
        if (len(words)-1 > i):
            size_of_indentation = i
            # print(str(words[i]))
            if (words[i] != ""):
                break
    return size_of_indentation


files_comparing(3111)

print("end")
