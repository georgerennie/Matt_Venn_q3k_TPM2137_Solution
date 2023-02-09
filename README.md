# Matt Venn/q3k MPW1 TPM2137 Solution

A solution to the [reverse engineering challenge](https://github.com/mattvenn/TPM2137/)
Matt Venn taped out on MPW1 recently. This requires quite a mix of tools to run,
a nonexhaustive list being magic, yosys, python, pysmt, jinja, prodict, iverilog
make.

The solution can be run simply with `make all`

The targeted hardware uses a serial interface to read in 8 ascii characters, and
compares them to a secret key. If they match, an output becomes high. A key
insight in this attack is that the actual key check occurs entirely
combinationally, so separating the highly sequential serial interface (which
would require a large depth for model checking tools) from the key checking
logic means the key check can be reverse engineered quickly by a SAT solver.

The rough structure of the solution is as follows:
- `extract_to_spice.sh`: Extract a gate level spice netlist from `challenge.gds`
	using `Magic`
- `spice2verilog.py`: Convert spice netlist into a gate level Verilog netlist
	using basic textual substitutions
- `create_lib.py`: Create Verilog models for the standard cells used in the
	netlist
- `synth.ys`: Synthesise the gate level netlist with the Verilog models to
	create a flattened netlist that only uses a few logic operators in json
	format
- `find_comb.py`: Does a depth first search from the output node to the
	flip-flop outputs, constructing an SMT model of the combinational circuit,
	then uses an SMT solver to find the values at the outputs of the flip-flops
	needed to set the output node. It then runs a series of simulations with
	different Serial input patterns to relate the indexes in the input Serial
	data to flip-flops, allowing the flag to be reconstructed
