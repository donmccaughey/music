CODESIGN_IDENTITY ?= "Donald McCaughey (K39VF43BJL)"
TMP ?= $(abspath tmp)


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
app : $(TMP)/Music.app


.PHONY : cov
cov : $(TMP)/coverage.sqlite
	open "$(TMP)/coverage/index.html"


.PHONY : run
run : $(TMP)/Music.app
	open $<


python_files := $(shell find src/ -type f -not -name '.DS_Store')


Music.spec :
	uv run pyi-makespec \
		--codesign-identity $(CODESIGN_IDENTITY) \
		--log-level ERROR \
		--name Music \
		--onedir \
		--osx-bundle-identifier cc.donm.music \
		--paths src \
		--specpath . \
		--windowed \
		src/run_app.py


uv.lock : pyproject.toml .python-version
	uv sync
	touch $@


$(TMP)/coverage.sqlite : \
		.coveragerc \
		$(TMP)/mypy.stamp
	rm -rf "$(TMP)/coverage"
	COVERAGE_FILE=$@ \
	uv run -m pytest \
		--cov \
		--cov-config=$< \
		--cov-report=html:"$(TMP)/coverage" \
		--cov-report=xml:"$(TMP)/coverage.xml" \
		--quiet --quiet


$(TMP)/Music.app : Music.spec $(TMP)/coverage.sqlite
	rm -rf $@
	uv run pyinstaller \
		--clean \
		--distpath $(TMP)/dist \
		--log-level ERROR \
		--noconfirm \
		--workpath $(TMP)/pyinstaller \
		$<
	mv $(TMP)/dist/Music.app $@


$(TMP)/mypy.stamp : \
		.mypy.ini \
		$(TMP)/ruff-format.stamp
	uv run -m mypy --check-untyped-defs src
	touch $@


$(TMP)/ruff-format.stamp : \
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
