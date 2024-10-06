import csv
import random
import sys

def build_data(data_size=1, equalize=False, name="math_data", small=1, big=20):

    with open(name+'.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        field = ['input', 'output']

        writer.writerow(field)

        #If need to can add more stuff to the list at op[0]
        ops = {
            "addition": ([" + "], lambda a,b : a + b), 
            "subtraction": ([" - "], lambda a,b : a - b), 
            "multiplication": ([" * "], lambda a,b : a * b), 
            "division": ([" / "], lambda a,b : round(a/b, 2) if a % b else int(a/b))
            }

        #Random Loop
        for i in range(data_size):
            try:
                op = ops[random.choice(list(ops.keys()))]
                #"Equalization" will occur if -e or -s is typed as the second argument, and small and big will refer to the number of digits
                #If -s is typed, both numbers will have the same number of digits
                # If -e is typed, numbers may have different numbers of digits
                sign = [-1, 1]
                signA = random.choice(sign)
                signB = random.choice(sign)
                if equalize == "-s":
                    digits = random.randint(small, big)
                    a = signA * random.randint(10**(digits-1), 10**(digits)-1)
                    b = signB * random.randint(10**(digits-1), 10**(digits)-1)
                elif equalize == "-e":
                    digitsA = random.randint(small, big)
                    digitsB = random.randint(small, big)
                    a = signA * random.randint(10**(digitsA-1), 10**(digitsA)-1)
                    b = signB * random.randint(10**(digitsB-1), 10**(digitsB)-1)
                else:
                    a = signA * random.randint(10**(small-1), 10**(big)-1)
                    b = signB * random.randint(10**(small-1), 10**(big)-1)
                if b == 0 and op == "division":
                    b = 1
                row = ["what is " + str(a) + random.choice(op[0]) + str(b), str(op[1](a,b))]
                writer.writerow(row)
            except KeyboardInterrupt:
                print("terminated with "+str(i)+" data points")
                break

#Command Line Arguments are of form: (Size of Dataset) (Name of Dataset) (Equalization [-e, -s]) (Smallest Possible Number of Digits) (Largest Possible Value)
def main():
    x = 1 if len(sys.argv) < 2 else int(sys.argv[1])
    name = "math_data" if len(sys.argv) < 2 else sys.argv[2]
    equalize = "none" if len(sys.argv) < 4 else sys.argv[3]
    small = 1 if len(sys.argv) < 5 else int(sys.argv[4])
    big = 20 if len(sys.argv) < 6 else int(sys.argv[5])
    build_data(x, equalize, name, small, big)


if __name__ == "__main__":
    main()