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


src_files := $(shell find src/ -type f -not -name '.DS_Store')


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
		$(src_files) \
		$(TMP)/uv-sync.stamp.txt
	uv run -m mypy --check-untyped-defs src
	date > $@


$(TMP)/uv-sync.stamp.txt : uv.lock | $$(dir $$@)
	uv sync --frozen
	date > $@


$(TMP)/ :
	mkdir -p $@
