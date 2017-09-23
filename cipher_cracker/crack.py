import re

def crack(plain_text, cipher_text):
	regex = re.compile('[^a-zA-Z]');
	plain_text = regex.sub('', plain_text);
	cipher_text = regex.sub('', cipher_text);

	digraph_dict = {};
	
	#string length must be even
	for i in range(len(plain_text)):
		if i % 2 != 0:
			continue;
		digraph_dict[plain_text[i:i+2]] = cipher_text[i:i+2];

	

crack('commander in chief fleet to naval headquarter', 'BPLYKRLHFEKIDBNFVUVIVZHZOPKERVNDFVLXWFESFE');
