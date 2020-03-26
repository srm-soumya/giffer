all: gif mp4

gif:
	python covid_spread.py

mp4: gif
	python gif2mp4.py

clean:
	rm -rf out/*
