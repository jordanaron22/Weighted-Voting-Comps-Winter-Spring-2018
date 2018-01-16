import itertools

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

def main():
    coal_list = ["ABCD","ABC","ABD","BCD","AB","AC","AD","BC","BD","CD"]
    coal_list = ["ABCDE","ABCD","ABCE","ABDE","ACDE","BCDE","ABC","ABD","ABE","ACD","ACE","ADE","BCD","BCE","BDE","CDE","AB","AC","AD","AE","BC","BD","BE","CD","CE","DE","A","B","C","D","E"]

    list4 = create_perms(4)
    list5 = create_perms(5)
    list6 = create_perms(6)
    list6.sort()
    print(list6)
    print(len(list6))

    print(find_amb(list4, False))
    print(find_amb(list5))
    print(find_amb(list6))


main()