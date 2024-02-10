TMP ?= $(abspath tmp)


.SECONDEXPANSION :


.PHONY : all
all : check


.PHONY : check
check : $(TMP)/.coverage


.PHONY : clean
clean :
	-rm -rf .mypy_cache
	-rm -rf .pytest_cache
	rm -rf $(TMP)


python_files := \
	src/music.py \
	src/music_test.py \
	\
	src/cuesheet/__init__.py \
	src/cuesheet/cuesheet.py \
	src/cuesheet/cuesheet_test.py \
	\
	src/cuesheet/fields/__init__.py \
	src/cuesheet/fields/field.py \
	src/cuesheet/fields/file.py \
	src/cuesheet/fields/file_test.py \
	src/cuesheet/fields/index.py \
	src/cuesheet/fields/index_test.py \
	src/cuesheet/fields/parse.py \
	src/cuesheet/fields/performer.py \
	src/cuesheet/fields/performer_test.py \
	src/cuesheet/fields/split.py \
	src/cuesheet/fields/title.py \
	src/cuesheet/fields/title_test.py \
	src/cuesheet/fields/track.py \
	src/cuesheet/fields/type_map.py \
	\
	src/cuesheet/fields/lines/__init__.py \
	src/cuesheet/fields/lines/blank.py \
	src/cuesheet/fields/lines/error.py \
	src/cuesheet/fields/lines/line.py

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
