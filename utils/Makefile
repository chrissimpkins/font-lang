build-lang-dict:
	curl -L -o spec.txt https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry
	python3 lang-parser.py spec.txt
	rm spec.txt


.PHONY: build-lang-dict