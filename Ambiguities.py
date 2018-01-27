import itertools

import networkx as nx

#fins ambiguities
#creates dictionary with key being coalition and value all of its ambiguities
def find_amb(coal_list, samelength = True):
    amb_dict = {}

    for coal1 in coal_list:
        for coal2 in coal_list:
            c1_geq_c2 = 0
            c1_leq_c2 = 0

            if len(coal1) < len(coal2):
                c1_leq_c2 = 1
                length = len(coal1)
            elif len(coal2) < len(coal1):
                c1_geq_c2 = 1
                length = len(coal2)
            else:
                length = len(coal2)

            for i in range(length):
                if coal1[i] < coal2[i]:
                    c1_geq_c2 = 1
                if coal2[i] < coal1[i]:
                    c1_leq_c2 = 1

            if c1_leq_c2 == 1 and c1_geq_c2 == 1:
                if samelength == True:
                    if len(coal1) == len(coal2):
                        if coal1 not in amb_dict.keys():
                            amb_dict[coal1] = [coal2]
                        else:
                            amb_dict[coal1].append(coal2)
                else:
                    if coal1 not in amb_dict.keys():
                        amb_dict[coal1] = [coal2]
                    else:
                        amb_dict[coal1].append(coal2)

    return amb_dict

#Creates all possible permutations (coalitions) of size n
#need to create possible COWS from this
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

    return set_of_coalitions

#Sorts coalitions
#ToDo look into fixing this
def sort_coal(coal_list):
    coal_list.sort(key=lambda s: len(s))
    coal_list.reverse()
    return coal_list

#Should delete all coalitions that cannot win (i.e. "C")
#ToDo generalize
def delete_losers(coal_list):
    coal_list = coal_list[:21]
    coal_list.append("A")
    coal_list = coal_list[1:]
    return coal_list

#Finds all subsets
def find_all_subsets(super_set):
    list_of_subsets = []
    #might need to be 1
    for i in range(1, len(super_set)):
        list_of_subsets.append(list(itertools.combinations(super_set, i)))

    flat_list = [item for sublist in list_of_subsets for item in sublist]
    flat_list.append(super_set)

    return flat_list

#Creates 3 lattices that differ in direction
#G1.forward is a parent to child digraph
#G1.backward is a child to parent digraph
#G2 is a sibling graph (i.e. coals of same size) from bigger to smaller
def create_lattice(coal_list):
    G1_forward = nx.DiGraph()
    G1_backward = nx.DiGraph()

    for coal in coal_list:
        if len(coal) > 0:
            for voter in reversed(coal):
                mini_coal = coal.replace(voter,"")
                if mini_coal in coal_list:
                    G1_forward.add_edge(coal,mini_coal)
                    G1_backward.add_edge(mini_coal,coal)

    G2 = nx.DiGraph()
    for i in range(len(coal_list)-1):
        if len(coal_list[i]) == len(coal_list[i+1]):
            G2.add_edge(coal_list[i],coal_list[i+1])


    return [G1_forward,G1_backward,G2]

#Given digraphs and current winning coalition, finds all children 1 step below
#needs to run multiple times to find all children of children
def find_children(forward,backward,winning_coal):
    list_of_children = []
    for item in winning_coal:
        if forward.has_node(item):
            for key in forward[item]:
                working_up = True
                if backward.has_node(key):
                    for parent in backward[key]:
                        if parent not in winning_coal and working_up == True:
                            working_up = False

                    if working_up == True and key not in winning_coal:
                        if key not in list_of_children:
                            list_of_children.append(key)
    return list_of_children

#Checks if all parents reside in set
def parent_checker(children,coal_list,backward):
    if len(children) == 0:
        return False

    for child in children:
        if backward.has_node(child):
            for parents in backward[child]:
                if parents not in coal_list:
                    return False

    return True

#removes COWS that contain complementing elements (i.e. "A" and "BC")
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


#Returns all possible coalitions for given digraphs and all sets
def find_coal(forward, backward, sideways,coal_list):

    #list of collections
    list_of_winning_coals = []

    #this first for loop will iterate once through all possible coalitions
    #j keeps track of where we are in the process
    for j in range(1, len(coal_list)+1):
        winning_coal = []
        #appends everything up until and including j
        for i in range(j):
            winning_coal.append(coal_list[i])

        #base coalition for algorithm
        #print("main coal is ", winning_coal)

        #finds children 1 and 2 steps below
        list_of_children = find_children(forward,backward,winning_coal)
        list_of_children2 = find_children(forward,backward,list_of_children)
        print(list_of_children2, "   LIST OF CHILD 2")



        #iterates through all children one step down
        for entry in range(len(list_of_children)):
            #holder list for adding children 1 step down
            new_collection = []
            #successivly adds children to holder list
            for add_child in range(entry+1):
                new_collection.append(list_of_children[add_child])
            #adds parent collection to holder list
            new_collection = winning_coal + new_collection
            new_collection = sort_coal(new_collection)

            #same logic as above, except for childrens children
            for entry2 in range(len(list_of_children2)):
                new_collection2 = []
                for add_child2 in range(entry2+1):
                    new_collection2.append(list_of_children2[entry2])
                if parent_checker(new_collection2,new_collection,backward):
                    new_collection2 = new_collection + new_collection2
                    new_collection2 = sort_coal(new_collection2)
                    new_collection2.sort()
                    if new_collection2 not in list_of_winning_coals:
                        list_of_winning_coals.append(new_collection2)




            new_collection.sort()
            if new_collection not in list_of_winning_coals:
                list_of_winning_coals.append(new_collection)

        winning_coal = sort_coal(winning_coal)
        winning_coal.sort()
        if winning_coal not in list_of_winning_coals:
            list_of_winning_coals.append(winning_coal)

    list_of_winning_coals = check_complement(list_of_winning_coals)
    return list_of_winning_coals

#large function to create variables in preparation
#Todo generalize if possible
def prep(size):
    if size == 3:
        list3 = create_perms(3)
        amb3 = find_amb(list3)
        sorted_list3 = sort_coal(list3)
        final_list3 = sorted_list3[:5]
        final_list3 = final_list3[1:]
        lattice3 = create_lattice(final_list3)
        lattice3_forward = lattice3[0]
        lattice3_backward = lattice3[1]
        lattice3_sideways = lattice3[2]
        return [list3, amb3, final_list3, lattice3_forward, lattice3_backward, lattice3_sideways]

    elif size == 4:
        list4 = create_perms(4)
        amb4 = find_amb(list4)
        sorted_list4 = sort_coal(list4)
        final_list4 = sorted_list4[:9]
        final_list4 = final_list4[1:]
        final_list4.append("A")
        lattice4 = create_lattice(final_list4)
        lattice4_forward = lattice4[0]
        lattice4_backward = lattice4[1]
        lattice4_sideways = lattice4[2]
        return [list4, amb4, final_list4, lattice4_forward, lattice4_backward, lattice4_sideways]

    elif size == 5:
        list5 = create_perms(5)
        amb5 = find_amb(list5)
        sorted_list5 = sort_coal(list5)
        final_list5 = delete_losers(sorted_list5)
        lattice5 = create_lattice(final_list5)
        lattice5_forward = lattice5[0]
        lattice5_backward = lattice5[1]
        lattice5_sideways = lattice5[2]
        return [list5, amb5, final_list5, lattice5_forward, lattice5_backward, lattice5_sideways]

#adds largest parent to each COW and creates a COW with just largest parent
def finishing_touches(final_list, size):
    parent = ""
    if size == 4:
        parent = "ABCD"
    elif size == 5:
        parent = "ABCDE"

    for cow in final_list:
        cow.append(parent)

    final_list.append([parent])

    return final_list



def main():



    #[list4, amb4, final_list4, lattice4_forward, lattice4_backward, lattice4_sideways] = prep(4)
    #final_list = find_coal(lattice4_forward, lattice4_backward, lattice4_sideways, final_list4)
    #final_list = finishing_touches(final_list, 4)
    #final_list = list(final_list for final_list,_ in itertools.groupby(final_list))

    [list5, amb5, final_list5, lattice5_forward, lattice5_backward, lattice5_sideways] = prep(5)
    final_list = find_coal(lattice5_forward, lattice5_backward, lattice5_sideways, final_list5)
    final_list = finishing_touches(final_list, 5)
    final_list = list(final_list for final_list, _ in itertools.groupby(final_list))

    for entry in final_list:
        print(entry)


    print(len(final_list))



main()