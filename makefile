dirs = $(shell find . -name 'res*.txt')

clean:
	rm -rf Results
	rm -f *.pyc

compile:
	@$(foreach dir,$(dirs),cat $(dir) >> all_results.txt;)
