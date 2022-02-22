.PHONY: all, clean

all:
	./extract_to_spice.sh
	./synth.ys
	./find_comb.py

clean:
	rm -r ext sim synth

