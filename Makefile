TMP ?= $(abspath tmp)


.SECONDEXPANSION :


.PHONY : all
all : check


.PHONY : check
check : $(TMP)/coverage.sqlite


.PHONY : clean
clean :
	-rm -rf .mypy_cache
	-rm -rf .pytest_cache
	rm -rf $(TMP)


.PHONY : clobber
clobber : clean
	rm -rf .venv


.PHONY : cov
cov : $(TMP)/coverage.sqlite
	open "$(TMP)/coverage/index.html"


python_files := \
	src/music.py \
	src/music_test.py \
	\
	src/cuesheet/__init__.py \
	src/cuesheet/cuesheet.py \
	src/cuesheet/cuesheet_test.py \
	\
	src/cuesheet/commands/__init__.py \
	src/cuesheet/commands/command.py \
	src/cuesheet/commands/file.py \
	src/cuesheet/commands/file_test.py \
	src/cuesheet/commands/index.py \
	src/cuesheet/commands/index_test.py \
	src/cuesheet/commands/parse.py \
	src/cuesheet/commands/performer.py \
	src/cuesheet/commands/performer_test.py \
	src/cuesheet/commands/rem.py \
	src/cuesheet/commands/split.py \
	src/cuesheet/commands/title.py \
	src/cuesheet/commands/title_test.py \
	src/cuesheet/commands/track.py \
	src/cuesheet/commands/track_test.py \
	\
	src/cuesheet/commands/lines/__init__.py \
	src/cuesheet/commands/lines/blank.py \
	src/cuesheet/commands/lines/error.py \
	src/cuesheet/commands/lines/line.py

source_files := $(filter-out %_test.py, $(python_files))

test_files := $(filter %_test.py, $(python_files))


uv.lock : pyproject.toml .python-version
	uv sync
	touch $@


$(TMP)/coverage.sqlite : \
		.coveragerc \
		$(TMP)/mypy.stamp.txt \
		| $$(dir $$@)
	rm -rf "$(TMP)/coverage"
	COVERAGE_FILE=$@ \
	uv run -m pytest \
		--cov \
		--cov-config=$< \
		--cov-report=html:"$(TMP)/coverage" \
		--cov-report=xml:"$(TMP)/coverage.xml" \
		--quiet --quiet


$(TMP)/mypy.stamp.txt : \
		.mypy.ini \
		$(source_files) \
		$(test_files) \
		$(TMP)/uv-sync.stamp.txt
	uv run -m mypy --check-untyped-defs src
	date > $@


$(TMP)/uv-sync.stamp.txt : uv.lock | $$(dir $$@)
	uv sync --frozen
	date > $@


$(TMP)/ :
	mkdir -p $@
