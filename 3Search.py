def main():

    def power_calc(local_winning_combo):
        list_a = []
        list_b = []
        list_c = []

        for combo in local_winning_combo:
            for i in range(0,len(combo)):
                check = combo.replace(combo[i], "")
                if check not in local_winning_combo:
                    if combo[i] == "A":
                        list_a.append(1)
                    elif combo[i] == "B":
                        list_b.append(1)
                    else:
                        list_c.append(1)

        denom = len(list_a)+len(list_b)+len(list_c)
        power_a = len(list_a)/denom
        power_b = len(list_b)/denom
        power_c = len(list_c)/denom

        power_list = [power_a, power_b, power_c]
        return power_list

    winning_combos = []
    winning_combos_power =[]
    for a in range(1,101):
        for b in range(0,100-a+1):
            for c in range(0,100-a-b+1):
                if a + b + c == 100 and a >= b >= c:
                    #print("A is ", a)
                    #print("B is ", b)
                    #print("C is ", c)
                    #print("")

                    for i in range(1,100):
                        local_winning_combo = []
                        if a+b+c > i:
                            #print("Winning combination: ABC")
                            local_winning_combo.append("ABC")
                        if a+b > i:
                            #print("Winning combination: AB")
                            local_winning_combo.append("AB")
                        if a+c > i:
                            #print("Winning combination: AC")
                            local_winning_combo.append("AC")
                        if b+c > i:
                            #print("Winning combination: BC")
                            local_winning_combo.append("BC")
                        if a > i:
                            #print("Winning combination: A")
                            local_winning_combo.append("A")
                        if b > i:
                            #print("Winning combination: B")
                            local_winning_combo.append("B")
                        if c > i:
                            #print("Winning combination: C")
                            local_winning_combo.append("C")

                        #print(local_winning_combo)

                        if not local_winning_combo in winning_combos:
                            winning_combos.append(local_winning_combo)

                            power_dist = power_calc(local_winning_combo)
                            if power_dist not in winning_combos_power:
                                winning_combos_power.append(power_dist)

    print("The possible winning combinations are:")
    print(winning_combos)
    print("")
    print("There are ",len(winning_combos_power), " different power distributions")
    print("")
    print("The possible power distributions are: ")
    print(winning_combos_power)

main()
