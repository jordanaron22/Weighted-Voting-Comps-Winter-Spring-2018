def main():

    #These lists will have the final answers in them
    winning_combos = []
    winning_combos_power =[]

    def summary():
        print("The possible winning combinations are:")
        print(winning_combos)
        print("")
        print("There are ", len(winning_combos_power), " different power distributions")
        print("")
        print("The possible power distributions are: ")
        print(winning_combos_power)

    #Calculates power from list of winning combinations
    def power_calc(local_winning_combo):
        #Used later to tally
        list_a = []
        list_b = []
        list_c = []
        list_d = []

        #iterates through each winning coalition
        for combo in local_winning_combo:
            #iterates through each member of a winning coalition
            for i in range(0, len(combo)):
                #iteratively removes each member and checks if winning coalition goes to losing
                check = combo.replace(combo[i], "")
                if check not in local_winning_combo:
                    if combo[i] == "A":
                        list_a.append(1)
                    elif combo[i] == "B":
                        list_b.append(1)
                    elif combo[i] == "C":
                        list_c.append(1)
                    else:
                        list_d.append(1)

        denom = len(list_a) + len(list_b) + len(list_c) + len(list_d)
        power_a = len(list_a)/denom
        power_b = len(list_b)/denom
        power_c = len(list_c)/denom
        power_d = len(list_d)/denom

        power_list = [power_a, power_b, power_c, power_d]
        return power_list

    #Calculates every possible combination of values for ABCD
    for a in range(1, 101):
        for b in range(0, 100 - a + 1):
            for c in range(0, 100 - a - b + 1):
                for d in range(0,100 - a - b - c +1):

                    #Only look at valid combinations
                    if a + b + c + d == 100 and a >= b >= c >= d:
                        #Every possible threshold value
                        for i in range(1, 100):
                            local_winning_combo = []
                            #Checks if coalition is a winning one
                            if a + b + c + d > i:
                                local_winning_combo.append("ABCD")
                            if a + b + c > i:
                                local_winning_combo.append("ABC")
                            if a + b + d > i:
                                local_winning_combo.append("ABD")
                            if a + c + d > i:
                                local_winning_combo.append("ACD")
                            if b + c + d > i:
                                local_winning_combo.append("BCD")
                            if a + b > i:
                                local_winning_combo.append("AB")
                            if a + c > i:
                                local_winning_combo.append("AC")
                            if a + d > i:
                                local_winning_combo.append("AD")
                            if b + c > i:
                                local_winning_combo.append("BC")
                            if b + d > i:
                                local_winning_combo.append("BD")
                            if c + d > i:
                                local_winning_combo.append("CD")
                            if a > i:
                                local_winning_combo.append("A")
                            if b > i:
                                local_winning_combo.append("B")
                            if c > i:
                                local_winning_combo.append("C")
                            if d > i:
                                local_winning_combo.append("D")



                            #adds to list of winning coalitions
                            if not local_winning_combo in winning_combos:
                                winning_combos.append(local_winning_combo)

                                #adds to list of power distributions
                                power_dist = power_calc(local_winning_combo)
                                if power_dist not in winning_combos_power:
                                    winning_combos_power.append(power_dist)


    summary()

main()
