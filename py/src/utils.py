def maprange( a, b, s):
	(a1, a2), (b1, b2) = a, b
	return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

def stringifyLEDData(LEDData):
	s = "."

	for i in range(len(LEDData)):

		d =  LEDData[i]
		ed = 0

		if d > 0:
			while int(d / (10 ** ed)) > 0:
				ed +=1
		else:
			ed = 1
			
		z = 3 - ed
		
		

		for _ in range(z):
			s += '0'
		s+= str(LEDData[i])
	s += "\n"
		

	return s.encode()