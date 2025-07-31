TMP ?= $(abspath tmp)
MUSIC_ROOT ?= "~/Dropbox/Music/Don's Music"


.SECONDEXPANSION :


.PHONY : all
all : check


.PHONY : check
check : $(TMP)/coverage.sqlite


.PHONY : clean
clean :
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	-find src/ -type d -name '__pycache__' -exec rm -rf {} \; 2>/dev/null
	rm -rf $(TMP)


.PHONY : clobber
clobber : clean
	rm -rf .venv


.PHONY : app
app :
	PYTHONPATH=src \
	uv run -m music --app $(MUSIC_ROOT)


.PHONY : cov
cov : $(TMP)/coverage.sqlite
	open "$(TMP)/coverage/index.html"


python_files := $(shell find src/ -type f -not -name '.DS_Store')


uv.lock : pyproject.toml .python-version
	uv sync
	touch $@


$(TMP)/coverage.sqlite : \
		.coveragerc \
		$(TMP)/mypy.stamp \
		| $$(dir $$@)
	rm -rf "$(TMP)/coverage"
	COVERAGE_FILE=$@ \
	uv run -m pytest \
		--cov \
		--cov-config=$< \
		--cov-report=html:"$(TMP)/coverage" \
		--cov-report=xml:"$(TMP)/coverage.xml" \
		--quiet --quiet


$(TMP)/mypy.stamp : \
		.mypy.ini \
		$(python_files) \
		$(TMP)/ruff-format.stamp
	uv run -m mypy --check-untyped-defs src
	touch $@


$(TMP)/ruff-format.stamp : \
		pyproject.toml \
		$(python_files) \
		$(TMP)/uv-sync.stamp
	ruff format \
		--config pyproject.toml \
		src
	touch $@


$(TMP)/uv-sync.stamp : uv.lock | $$(dir $$@)
	uv sync --frozen
	touch $@


$(TMP)/ :
	mkdir -p $@
