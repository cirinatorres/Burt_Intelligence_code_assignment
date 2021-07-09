# from time import time
# start_time = time()
import sys


# 1 <= n <= 500
n = int(sys.stdin.readline().rstrip())
for i in range(n):
	# len(line1) == len(line1) ~ len([1..50]),
	# letters (a-z, A-Z) or digits (0-9),
	# doesn't affect equality operator, O(1)
	line1 = sys.stdin.readline().rstrip()
	line2 = sys.stdin.readline().rstrip()

	# This option generates an iterator using zip() and
	# another one for join() which makes it more efficient.
	# List comprehension has a memory complexity of O(m)
	# as a function of the length of the list.
	difference = ''.join(['*' if c1 != c2 else '.' for (c1,c2) in zip(line1,line2)])
	# Average execution time over 5 trials.
	# The variable 'line' was being altered so that for every execution
	# it was line1 = 'ATCCGCTTAGAGGGATT'*j, where j in [1,1000,1000000].
	# --- 0.00003790855407714844 seconds ---
	# --- 0.00021004676818847656 seconds ---
	# --- 0.09899282455444336 seconds ---
	
	# Second option:
	# difference = ''
	# length = len(line1)
	# for i in range(length):
	# 	difference += '*' if line1[i] != line2[i] else '.'
	# Average execution time over 5 trials.
	# --- 0.000038146972656256 seconds ---
	# --- 0.0005619525909423828 seconds ---
	# --- 0.43646788597106934 seconds ---

	print(line1)
	print(line2)
	print(difference + '\n')
	# print("--- %s seconds ---" % (time() - start_time))
