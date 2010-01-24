all:
	@env python ./slidetool.py allbundle

clean:
	@git clean -f -d 00bundles
