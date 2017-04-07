# Print out the list of integers from 1 to 100. If the number is divisable
# by 3 replace it with buzz, if it is divisible by 5 replace with fizz, and if
# it is divisible by 15 replace it with buzzfizz.

for i in range(100):
    j = i + 1
    if j%15 == 0:
        print "buzzfizz"
    elif j%5 == 0:
        print "fizz"
    elif j%3 == 0:
        print "buzz"
    else:
        print j
