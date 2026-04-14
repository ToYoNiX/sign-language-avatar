#/usr/bin/sh
# Build Algerian Sign Language 3D avatar

default: all
# Clean build files
clean:
	
backup: 
	
#create all files 
all:
# Publish to github
publish:
	git push origin master 

server:
	poetry run python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload

test:
	poetry run python -m pytest
docs:
	epydoc -v --config epydoc.conf
SOURCE=../data/sigml
OUTPUT=output
test_all:
	# test generate all files to output
	cd tests;python extract_data_word_list.py  -s $(SOURCE)  -o $(OUTPUT) -a all

test_json:
	# test generate json file to output
	cd tests;python extract_data_word_list.py  -s $(SOURCE)  -o $(OUTPUT) -a json

test_wordlist:
	# test generate wordlist file to output
	cd tests;python extract_data_word_list.py  -s $(SOURCE)  -o $(OUTPUT) -a wordlist

test_categories:
	# test generate categories file to output
	cd tests;python extract_data_word_list.py  -s $(SOURCE)  -o $(OUTPUT) -a categories

test_stat:
	# test generate statistics file to output
	cd tests;python extract_data_word_list.py  -s $(SOURCE)  -o $(OUTPUT) -a statistics
