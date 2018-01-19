import itertools
import networkx as nx

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

        #print(coalition)



    return set_of_coalitions

def sort_coal(coal_list):
    coal_list.sort(key=lambda s: len(s))
    coal_list.reverse()
    return coal_list

def delete_losers(coal_list):
    coal_list = coal_list[:21]
    coal_list.append("A")
    coal_list = coal_list[1:]
    return coal_list

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

def find_coal(forward, backward, sideways,coal_list):
    list_of_winning_coals = []
    winning_coal = []
    count = 0

    for j in range(1, len(coal_list)+1):
        winning_coal = []
        for i in range(j):
            winning_coal.append(coal_list[i])
        #Checks iterating is working correctly
        print("main coal",winning_coal)

        working_up = True

        for item in winning_coal:
            print(item)
            if forward.has_node(item):
                print(item)
                for key in forward[item]:
                    print("Children ",key)
                    if backward.has_node(key):
                        for parent in backward[key]:
                            #print(parent)
                            if parent not in winning_coal and working_up == True:
                                print("No Parent")
                                working_up = False

                        #TODO Right not only adds one child in at a time
                        #Idea: create list of all children
                        #then add all possible combinations
                        if working_up == True and key not in winning_coal:
                            print("yes parent")
                            new_coal = list(winning_coal)
                            new_coal.append(key)
                            if new_coal not in list_of_winning_coals:
                                list_of_winning_coals.append(new_coal)
                            print("Appending new coal",new_coal)

            print("appending coal", winning_coal)
            if winning_coal not in list_of_winning_coals:
                list_of_winning_coals.append(winning_coal)




        #for coal in winning_coal:
         #   for children in forward[coal]:
          #      for parents in backward[children]:
           #         if parents in winning_coal:
            #            #winning_coal.append(children)
             #           count = 0


    return(list_of_winning_coals)




def main():

    list5 = create_perms(5)

    amb5 = find_amb(list5, samelength=False)
    #print(amb5)

    sorted_list5 = sort_coal(list5)
    final_list5 = delete_losers(sorted_list5)
    #print(final_list5)
    lattice5 = create_lattice(final_list5)

    lattice5_forward = lattice5[0]
    lattice5_backward = lattice5[1]
    lattice5_sideways = lattice5[2]

    #for keys in lattice5_forward["ABCDE"]:
    #    print(keys)

    #print(lattice5_sideways.edges())
    #print(find_coal(lattice5_forward,lattice5_backward,lattice5_sideways,final_list5))

    list3 = create_perms(3)
    amb3 = find_amb(list3)
    sorted_list3 = sort_coal(list3)
    final_list3 = sorted_list3[:5]
    final_list3 = final_list3[1:]
    lattice3 = create_lattice(final_list3)
    #print(final_list3)
    lattice3_forward = lattice3[0]
    lattice3_backward = lattice3[1]
    lattice3_sideways = lattice3[2]
    #print(find_coal(lattice3_forward, lattice3_backward, lattice3_sideways, final_list3))

    list4 = create_perms(4)
    amb4 = find_amb(list4)
    sorted_list4 = sort_coal(list4)
    final_list4 = sorted_list4[:9]
    final_list4 = final_list4[1:]
    lattice4 = create_lattice(final_list4)
    lattice4_forward = lattice4[0]
    lattice4_backward = lattice4[1]
    lattice4_sideways = lattice4[2]
    print(find_coal(lattice4_forward, lattice4_backward, lattice4_sideways, final_list4))


main()