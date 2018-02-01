import itertools
import networkx as nx


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

    for coal in coal_list:
        for entry in coal_dict[coal]:
            Graph.add_edge(entry,coal)

            to_remove = False
            for path in list(nx.all_simple_paths(Graph, entry, coal)):
                if len(path) > 2:
                    to_remove = True

            if to_remove:
                Graph.remove_edge(entry, coal)


    return Graph


def main():
    all_coals = create_perms(5)
    coal_dict = findBigger(all_coals)
    structure = create_structure(all_coals,coal_dict)
    print(nx.edges(structure))

main()