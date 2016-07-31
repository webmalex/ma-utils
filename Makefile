N=mu
NN=MU
P=$(N).egg-info/source.sh
main:
	$(N)

install:
	pip install --editable .
	@echo `pwd`/$(P)
	eval "$$(_$(NN)_COMPLETE=source $(N))"
	_$(NN)_COMPLETE=source $(N) > $(P)

uninstall:
	pip uninstall $(N)
