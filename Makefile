all:
	@env python ./create-bundle.py --all

clean:
	@git clean -f -d 00bundles
