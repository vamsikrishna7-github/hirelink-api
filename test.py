import time
import sys

if __name__ == "__main__":
	max = 100_000
	if(len(sys.argv) > 1):
		max = int(sys.argv[1])
	st = time.time()
	s = 0	
	for i in range(max):
		s+=i
	end = time.time()-st
	print("Completed in",end,"ms")
