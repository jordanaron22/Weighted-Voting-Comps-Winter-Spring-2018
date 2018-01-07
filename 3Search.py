def main():
    winning_combos = []
    for a in range(1,101):
        for b in range(0,100-a+1):
            for c in range(0,100-a-b+1):
                if a + b + c == 100 and a >= b >= c:
                    #print("A is ", a)
                    #print("B is ", b)
                    #print("C is ", c)
                    #print("")

                    for i in range(1,101):
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

    print(winning_combos)

main()
