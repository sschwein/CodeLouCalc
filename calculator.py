import random
import pdb

#initialize stuff
print("Welcome to the Code Louisville calculator!!!")


### Function to get two input numbers ###
def get_inputs():
    number_one = 0
    number_two = 0
    operator = '+'
    #this is used to loop until the user inputs valid content
    while True:
        #first, try to get an integer, and if it's not an integer, loop until we get an integer
        try:
            number_one = int(input("First number: "))
            break
        except:
            print("Sorry, that wasn't a valid number.")
            continue
    while True:
        try:
            number_two = int(input("Second number: "))
            break
        except:
            print("Sorry, that wasn't a valid number.")
            continue
    while True:
        operator = input("Operator ('+', '-', '*', '/', '%'): ")
        if operator not in ['+', '-', '*', '/', '%']:
            print("Sorry, that isn't a valid operator.")
        else:
            break
    return number_one, number_two, operator



### Add two numbers ###
def add_two(num1, num2):
    return num1 + num2


### Subtract two numbers ###
def sub_two(num1, num2):
    return num1 - num2


### Multiply two numbers ###
def mult_two(num1, num2):
    return num1 * num2


### Divide two numbers ###
def div_two(num1, num2):
    return num1 / num2


### Take the modulus of a dividend and a divisor ###
def mod_two(num1, num2):
    return num1 % num2


### Add multiple numbers ###
def add_multi(nums):
    # Add code here
    return 0


### Subtract multiple numbers ###
def sub_multi(nums):
    # Add code here
    return 0


### Loop through the results array and print out each line ###
def print_results(all_results):
    for r in all_results:
        if 'Sum' in r['operator']:
            print(r['operator'], '=', r['result'])
        else:
            print(format(r['num1'], '02d'), r['operator'], format(r['num2'], '02d'), '=', r['result'])


### This function creates a random number of random numbers in a list (it gets trippy) ###
def get_random_nums(maxc):
    nums = []
    for i in range(int(random.random() * maxc + 1)):
        nums.append(int(random.random() * 99 + 1))
    return nums

### Main execution function ###
def main():
    total_eq = 0
    #loop until you get tired
    while True:
        
        #array that stores results from each equation
        all_results = []
        num_loops = 1

        #Ask the user for their choice 
        choice = input("\nWould you like to enter your own equation (Enter 1), randomly generate equations (Enter 2), or leave (Enter 0): ")
        #choose user input
        if choice == '1':
            number_one, number_two, operator = get_inputs()
        #choose to auto run 10 equations
        elif choice == '2':
            num_loops = 10
        #exit program
        elif choice == '0':
            break
        #the input choice was not valid, try again
        else:
            print("Sorry, that input wasn't valid.")
            continue

        #loop for either 1 iteration or 10 iterations
        for i in range(num_loops):
            #print(i)

            #temporary dictionary that holds the equation and results
            single_result = {'num1': 0, 'operator': '', 'num2': 0, 'result': 0}

            #if choice is to automatically generate numbers and equations,
            #this loop will go through, select up to 10 numbers, 
            #and either add them all or subtract them all together
            if choice == '2':
                random_nums = get_random_nums(10)
                if int(random.random() * 2) == 1:
                    single_result['result'] = add_multi(random_nums)
                    single_result['operator'] = 'Sum (add)'
                else:
                    single_result['result'] = sub_multi(random_nums)
                    single_result['operator'] = 'Sum (subtract)'
                all_results.append(single_result)
                continue


            #if-else chain to determine what operator should be used
            #addition
            if operator == '1' or operator == '+':
                #pdb.set_trace()
                single_result['result'] = add_two(number_one, number_two)
                single_result['operator'] = '+'
                #print(single_result['result'])
            #subtraction
            elif operator == '2' or operator == '-':
                single_result['result'] = sub_two(number_one, number_two)
                single_result['operator'] = '-'
            #multiplication
            elif operator == '3' or operator == '*':
                single_result['result'] = mult_two(number_one, number_two)
                single_result['operator'] = '*'
            #division
            elif operator == '4' or operator == '/':
                single_result['result'] = div_two(number_one, number_two)
                single_result['operator'] = '/'
            #modulus
            elif operator == '5' or operator == '%':
                single_result['result'] = mod_two(number_one, number_two)
                single_result['operator'] = '%'

            #make sure to add the two original numbers to the result so the equation prints properly
            single_result['num1'] = number_one
            single_result['num2'] = number_two
                
            #append the temp result to the results array
            all_results.append(single_result)

            #increase the total counter by 1
            total_eq += 1

        print_results(all_results)
    print("\nTotal number of equations: ", total_eq)


#Call main function
main()