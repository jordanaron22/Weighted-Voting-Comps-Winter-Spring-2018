import itertools
import networkx as nx
import copy
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import random


def create_perms(size):
    lst = list(itertools.product([0, 1], repeat=size))
    set_of_coalitions = []

    for item in lst:
        coalition = ""

        for index in range(size):
            value = item[index] * (65 + index)
            if item[index] != 0:
                coalition = coalition + chr(value)
        set_of_coalitions.append(coalition)

    set_of_coalitions.sort(key=len)
    set_of_coalitions.reverse()
    set_of_coalitions.pop()

    return set_of_coalitions

def bigger(coal1, coal2):
    greater_than = True
    if coal1 == coal2:
        return False

    min_length = min(len(coal1),len(coal2))


    if len(coal1) == len(coal2):
        for i in range(min_length):
            #change this equality to get other direction
            if coal1[i] < coal2[i]:
                return False

    elif len(coal1) < len(coal2):
        for i in range(min_length):
            #change this equality to get other direction
            if coal1[i] < coal2[i]:
                return False

    else:
        return False

    return greater_than

def findBigger(all_coals):
    bigger_dict = {}
    for coal_index in range(len(all_coals)):
        bigger_than = []
        for test_coal_index in range(len(all_coals)):
            if bigger(all_coals[coal_index],all_coals[test_coal_index]):
                bigger_than.append(all_coals[test_coal_index])

        bigger_than.reverse()
        bigger_dict[all_coals[coal_index]] = bigger_than

    return bigger_dict

def create_structure(coal_list,coal_dict):
    Graph = nx.DiGraph()

    layer_dict = {}

    layer_dict["ABC"] = 2
    layer_dict["ABCD"] = 1

    for coal in coal_list:
        layers = []
        for entry in coal_dict[coal]:
            layers.append(layer_dict[entry])
            Graph.add_edge(entry,coal)

            to_remove = False
            for path in list(nx.all_simple_paths(Graph, entry, coal)):
                if len(path) > 2:
                    to_remove = True

            if to_remove:
                Graph.remove_edge(entry, coal)

        if len(layers) > 0:
            layer_dict[coal] = max(layers) + 1


    return [Graph, layer_dict]


def calculateLayer(structure):
    layer_dict = {}
    count = 0
    for edge in nx.edges(structure):
        print(edge)
        if count == 0:
            print("Count is 0 ")
            layer_dict[edge[0]] = 2
            layer_dict[edge[1]] = 3
        else:
            print("non zero count")
            layer_dict[edge[1]] = layer_dict[edge[0]] + 1
        count += 1


    return layer_dict


def invert_dict(layer_dict):
    inverted_dict = {}
    for k, v in layer_dict.items():
        if v not in inverted_dict.keys():
            inverted_dict[v] = [k]
        else:
            inverted_dict[v].append(k)
    return inverted_dict


def parents(coal, structure):
    list_of_parents = []
    for node in structure[coal].keys():
        list_of_parents.append(node)

    return list_of_parents


def parentFinder(list_of_coals, structure):
    structure = structure.reverse()
    list_of_parents = []
    for coal in list_of_coals:
        for parent in parents(coal, structure):
            if parent not in list_of_parents:
                list_of_parents.append(parent)

    return list_of_parents



def check_complement(list_of_winning_coals):
    inds_remove = []
    for collection in range(len(list_of_winning_coals)):
        for index1 in range(len(list_of_winning_coals[collection])):
            for index2 in range (index1, len(list_of_winning_coals[collection])):
                c1 = set(list_of_winning_coals[collection][index1])
                c2 = set(list_of_winning_coals[collection][index2])
                if len(c1 & c2) == 0:
                    if collection not in inds_remove:
                        inds_remove.append(collection)

    inds_remove.sort(reverse=True)
    for entry in inds_remove:
        del list_of_winning_coals[entry]

    return list_of_winning_coals


def treeTraversal(structure, layer_dict):
    cow_list = [["ABCD"],["ABCD","ABC"]]
    current_layer = 3
    max_layer = max(layer_dict.keys())

    while current_layer <= max_layer:
        #print(current_layer)
        parent_dict = {}
        parent_list = parentFinder(layer_dict[current_layer], structure)
        current_children = layer_dict[current_layer]
        for child in current_children:
            parent_dict[child] = []

        #Creates dictionary where each key is a current child
        #Value is a list
        #List at index i means that the cow at index i in cow_list contains child's parents
        for cow in cow_list:
            for child in current_children:
                current_parents = parents(child, structure.reverse())
                contains_parents = True
                for parent in current_parents:
                    if parent not in cow:
                        contains_parents = False
                if contains_parents == True:
                    parent_dict[child].append(1)
                else:
                    parent_dict[child].append(0)




        # list_of_current = list(parent_dict.keys())
        #
        # length_to_delete = len(parent_dict[list_of_current[0]])
        # 
        # print(length_to_delete)
        # print(parent_dict)
        #
        # for key in parent_dict:
        #     parent_dict[key] = parent_dict[key][length_to_delete:]
        #
        # print(parent_dict)



        possible_coals = []
        for i in range(len(cow_list)):
            temp_possible_coals = []
            for child in current_children:
                toAppendList = []
                toAppend = True

                if parent_dict[child][i] == 0:
                    toAppend = False

                if toAppend:
                   temp_possible_coals.append(child)
            possible_coals.append(temp_possible_coals)



        new_addition = []
        for possibilities in range(len(possible_coals)):
            for i in range(len(possible_coals[possibilities])):
                combo = list(itertools.combinations(possible_coals[possibilities],i+1))

                for combination in combo:
                    cleaned_combination = []
                    for element in combination:
                        cleaned_combination.append(element)

                    temp_new_addition = copy.copy(cow_list[possibilities])
                    for coalition in cleaned_combination:
                        temp_new_addition.append(coalition)

                    new_addition.append(temp_new_addition)

        for addition in new_addition:
            cow_list.append(addition)

        current_layer += 1

    return cow_list

def run4():
    all_coals = create_perms(4)[1:9]
    all_coals.append("A")

    coal_dict = findBigger(all_coals)
    structure = create_structure(all_coals, coal_dict)
    layer_dict = calculateLayer(structure)


    layer_dict = invert_dict(layer_dict)


    pre_comp = treeTraversal(structure, layer_dict)

    post_comp = check_complement(pre_comp)


def run5():
    all_coals = create_perms(5)

    # 5 specific
    all_coals = all_coals[1:21]
    all_coals.append("A")

    coal_dict = findBigger(all_coals)
    structure = create_structure(all_coals, coal_dict)
    layer_dict = calculateLayer(structure)

    layer_dict["ABCDE"] = 1

    layer_dict = invert_dict(layer_dict)

    parent_list = parentFinder(layer_dict[2], structure)

    pre_comp = treeTraversal(structure, layer_dict)
    post_comp = check_complement(pre_comp)

    return post_comp

def run6():
    all_coals = create_perms(6)[1:48]
    all_coals.append("A")

    coal_dict = findBigger(all_coals)
    structure = create_structure(all_coals, coal_dict)
    layer_dict = calculateLayer(structure)

    layer_dict = invert_dict(layer_dict)

    parent_list = parentFinder(layer_dict[2], structure)

    pre_comp = treeTraversal(structure, layer_dict)
    # print(pre_comp)
    # print(len(pre_comp))
    # print("")
    post_comp = check_complement(pre_comp)
    # print("")
    # print(post_comp)
    # print(len(post_comp))

    return post_comp


def run7():
    all_coals = create_perms(7)
    all_coals = all_coals[1:106]
    all_coals.remove('DEF')
    all_coals.remove('DEG')
    all_coals.remove('DFG')
    all_coals.remove('EFG')
    all_coals.append('A')

    coal_dict = findBigger(all_coals)
    structure = create_structure(all_coals, coal_dict)
    layer_dict = {'ABSDEFG': 1, 'ABCDEF': 2, 'ABCDEG': 3, 'ABCDFG': 4, 'ABCDE': 4, 'ABCEFG': 5, 'ABCDF': 5, 'ABDEFG': 6, 'ABCEF': 6, 'ACDEFG': 7, 'ABDEF': 7, 'BCDEFG': 8, 'ACDEF': 8, 'BCDEF': 9, 'ABCDG': 6, 'ABCEG': 7, 'ABCD': 7, 'ABCFG': 8, 'ABDEG': 8, 'ABCE': 8, 'ABDFG': 9, 'ABCF': 9, 'ACDEG': 9, 'ABDE': 9, 'ABEFG': 10, 'ACDFG': 10, 'ABDF': 10, 'ACEFG': 11, 'ABEF': 11, 'BCDEG': 10, 'ACDE': 10, 'BCDFG': 11, 'ACDF': 11, 'ADEFG': 12, 'BCEFG': 12, 'ACEF': 12, 'BDEFG': 13, 'ADEF': 13, 'BCDE': 11, 'BCDF': 12, 'BCEF': 13, 'CDEFG': 14, 'BDEF': 14, 'CDEF': 15, 'ABCG': 10, 'ABDG': 11, 'ABC': 11, 'ABEG': 12, 'ACDG': 12, 'ABD': 12, 'ABFG': 13, 'ACEG': 13, 'ABE': 13, 'ACFG': 14, 'ABF': 14, 'BCDG': 13, 'ACD': 13, 'ADEG': 14, 'BCEG': 14, 'ACE': 14, 'ADFG': 15, 'BCFG': 15, 'ACF': 15, 'BDEG': 15, 'ADE': 15, 'AEFG': 16, 'BDFG': 16, 'ADF': 16, 'BEFG': 17, 'AEF': 17, 'BCD': 14, 'BCE': 15, 'BCF': 16, 'CDEG': 16, 'BDE': 16, 'CDFG': 17, 'BDF': 17, 'CEFG': 18, 'BEF': 18, 'CDE': 17, 'CDF': 18, 'DEFG': 19, 'CEF': 19, 'DEF': 20, 'ABG': 15, 'ACG': 16, 'AB': 16, 'ADG': 17, 'BCG': 17, 'AC': 17, 'AEG': 18, 'BDG': 18, 'AD': 18, 'AFG': 19, 'BEG': 19, 'AE': 19, 'BFG': 20, 'AF': 20, 'CDG': 19, 'CEG': 20, 'CFG': 21, 'DEG': 21, 'DFG': 22, 'EFG': 23, 'AG': 21, 'A': 22}

    layer_dict = invert_dict(layer_dict)

    pre_comp = treeTraversal(structure, layer_dict)
    post_comp = check_complement(pre_comp)

    writeFile(post_comp,"cow7.txt")
    return post_comp


def writeFile(cow_list, filename):
    thefile = open(filename, 'w')
    for item in cow_list:
        thefile.write("%s\n" % item)
    thefile.write("%s\n" % len(cow_list))


def getHandCow():
    df = pd.read_csv(r"C:\Users\jorda\PycharmProjects\Comps\cows5.csv", header=None)
    df = df.fillna(0)
    cow_list = []
    for key, value in df.iterrows():
        current_cow = []

        for i in range(len(value)):
            if value[i] != 0:
                current_cow.append(value[i])

        cow_list.append(current_cow)
    return cow_list


def compareLists(hand_cow,post_comp):
    for cow in post_comp:
        cow.sort()
    for cow in hand_cow:
        cow.sort()
    post_comp.sort()
    hand_cow.sort()

    hand_cow_tuple = [tuple(lst) for lst in hand_cow]
    post_comp_tuple = [tuple(lst) for lst in post_comp]

    hand_cow_set = set(hand_cow_tuple)
    post_comp_set = set(post_comp_tuple)

    return hand_cow_set.symmetric_difference(post_comp_set)


def removeSmall(current):
    if 71 in current:
        new_current = copy.copy(current)
        new_current.remove(71)
        return new_current



def quickCreate():
    current_list = [65, 66, 67, 68, 69, 70, 71]
    final_list = [[65, 66, 67, 68, 69, 70, 71]]
    while True:
        to_add = []
        to_add.append(removeSmall(current_list))



        current_list = to_add

        for cow in to_add:
            if cow != None:
                final_list.append(cow)

        if to_add == [None]:
            break

    return final_list


def parent_checker(structure,cow_list):
    structure2 = structure.reverse()
    for cow in cow_list:
        for coal in cow:
            if coal == "ABCDEFG" or coal == "ABCDEF":
                continue
            elif list(structure2[coal])[0] not in cow:
                return False

    return True






def main():

    # [structure, layer_dict] = create_structure(all_coals, coal_dict)
    #
    # to_save = [structure, layer_dict]
    #
    # pickle.dump(to_save, open("structure and dict size 7.p", 'wb'))
    # both = pickle.load(open("structure and dict size 7.p", "rb"))

    all_coals = create_perms(4)
    coal_dict = findBigger(all_coals)
    [structure, layer_dict] = create_structure(all_coals, coal_dict)

    layer_dict = invert_dict(layer_dict)

    pre_comp = treeTraversal(structure, layer_dict)
    post_comp = check_complement(pre_comp)

    print(post_comp)



main()