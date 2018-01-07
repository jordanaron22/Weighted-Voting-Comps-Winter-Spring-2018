def main():
    winning_combos = []
    for a in range(1, 101):
        for b in range(0, 100 - a + 1):
            for c in range(0, 100 - a - b + 1):
                for d in range(0,100 - a - b - c +1):
                    if a + b + c + d == 100 and a >= b >= c >= d:
                        # print("A is ", a)
                        # print("B is ", b)
                        # print("C is ", c)
                        # print("")

                        for i in range(1, 100):
                            local_winning_combo = []
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



                            # print(local_winning_combo)

                            if not local_winning_combo in winning_combos:
                                winning_combos.append(local_winning_combo)

    print(winning_combos)


main()
