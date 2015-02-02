dirs = $(shell find . -name 'res*.txt')

clean:
	rm -rf db_if*
	rm -rf s3_if*
	rm -rf gd_if*
	rm -rf GoogleDriveBench*
	rm -rf DropboxBench*
	rm -rf Bench*
	rm -rf sweeps
	rm -rf results.txt
	rm -f *.pyc
	rm -rf stdout+stderr

compile:
    @$(foreach dir,$(dirs),echo $(dir) >> all_results.txt;)