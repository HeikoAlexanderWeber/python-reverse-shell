init:
	pip install -r requirements.txt

run:
	python ./shell/program.py

compile:
	rm -rf ./build
	pyinstaller ./shell/program.py --distpath ./build/bin --onefile
	rm -rf ./build/program