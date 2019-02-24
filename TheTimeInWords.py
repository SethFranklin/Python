
import math

def timeInWords(h, m):
	if (m == 0):
		return NumToWord(h) + " o' clock"
	elif (m == 1):
		return NumToWord(m) + " minute past " + NumToWord(h)
	elif ((m >= 2 and m <= 14) or (m >= 16 and m <= 29)):
		return NumToWord(m) + " minutes past " + NumToWord(h)
	elif (m == 15):
		return "quarter past " + NumToWord(h)
	elif (m == 30):
		return "half past " + NumToWord(h)
	elif (m == 45):
		return "quarter to " + NumToWord((h + 1) % 12)
	elif ((m >= 31 and m <= 44) or (m >= 46 and m <= 58)):
		return NumToWord(60 - m) + " minutes to " + NumToWord((h + 1) % 12)
	elif (m == 59):
		return NumToWord(60 - m) + " minute to " + NumToWord((h + 1) % 12)

def NumToWord(num):
	NumDict = {

	1: "one",
	2: "two",
	3: "three",
	4: "four",
	5: "five",
	6: "six",
	7: "seven",
	8: "eight",
	9: "nine",
	10: "ten",
	11: "eleven",
	12: "twelve",
	13: "thirteen",
	14: "fourteen",
	15: "fifteen",
	16: "sixteen",
	17: "seventeen",
	18: "eighteen",
	19: "nineteen",
	20: "twenty",
	30: "thirty",
	40: "fourty",
	50: "fifty",

	}

	if (num % 10 == 0 or (num >= 1 and num <= 19)):
		return NumDict[num]
	else:
		return NumDict[math.floor(num / 10) * 10] + " " + NumDict[num % 10]

print(timeInWords(3, 30))