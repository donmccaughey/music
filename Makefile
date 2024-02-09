TMP ?= $(abspath tmp)


.SECONDEXPANSION :


.PHONY : all
all : check


.PHONY : check
check : $(TMP)/.coverage


.PHONY : clean
clean :
	rm -rf $(TMP)


python_files := \
	src/music.py \
	src/music_test.py \
	\
	src/cuesheet/__init__.py \
	src/cuesheet/cuesheet.py \
	src/cuesheet/file.py \
	src/cuesheet/index.py \
	src/cuesheet/index_test.py \
	src/cuesheet/parse.py \
	src/cuesheet/performer.py \
	src/cuesheet/performer_test.py \
	src/cuesheet/title.py \
	src/cuesheet/title_test.py \
	src/cuesheet/track.py

source_files := $(filter-out %_test.py, $(python_files))

test_files := $(filter %_test.py, $(python_files))


$(TMP)/.coverage : \
		.coveragerc \
		$(TMP)/mypy.stamp.txt \
		| $$(dir $$@)
	rm -rf "$(TMP)/coverage"
	COVERAGE_FILE=$@ \
	python3 -m pytest \
		--cov \
		--cov-config=$< \
		--cov-report=html:"$(TMP)/coverage" \
		--cov-report=xml:"$(TMP)/coverage.xml" \
		--quiet --quiet


$(TMP)/mypy.stamp.txt : \
		.mypy.ini \
		$(source_files) \
		$(test_files) \
		$(TMP)/pip-install-requirements.stamp.txt \
		$(TMP)/pip-install-requirements-dev.stamp.txt
	python3 -m mypy --check-untyped-defs src
	date > $@


$(TMP)/pip-install-requirements.stamp.txt : requirements.txt | $$(dir $$@)
	python3 -m pip install \
		--quiet --quiet --quiet \
		--requirement $<
	date > $@


$(TMP)/pip-install-requirements-dev.stamp.txt : requirements-dev.txt | $$(dir $$@)
	python3 -m pip install \
		--quiet --quiet --quiet \
		--requirement $<
	date > $@


$(TMP)/ :
	mkdir -p $@
