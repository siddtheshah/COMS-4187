# Siddhant Shah
# uses python3.7

import secrets
import timeit
import random
from functools import partial

def main():

	# Timer does 1000 runs 10 times and returns best time of the set of 10

	times = timeit.Timer(partial(random.getrandbits, 128)).repeat(10, 1000)
	print("Standard time Time: {0}\n".format(min(times)))
	
	times = timeit.Timer(partial(secrets.token_bytes, 16)).repeat(10, 1000)
	print("Cryptosecure Time: {0}\n".format(min(times)))

	return

main()
