#! /usr/bin/env python3

from more_itertools import peekable

class Netlist():
    def __init__(self):
        self.cells = set()
        self.wires = set()
        self.instances = []
        self.args = None

    def to_escaped_id(self, name):
        if name in self.args:
            return name
        return "\\" + name + " "

    def parse_instantiation(self, line):
        name = line[-1]
        ident = line[0]
        args = line[1:-1]

        assert line[1] in ["VGND", "VPWR"]
        assert line[2] in ["VGND", "VPWR"]
        assert name in self.cells

        for signal in args:
            self.wires.add(signal)

        if not ("decap" in name or "diode" in name):
            self.instances.append((name, ident, args))

    def parse_subckt(self):
        try:
            self.s.peek()
        except StopIteration:
            return True

        subckt = next(self.s).split()
        if len(subckt) == 0 or subckt[0].startswith("*"):
            return
        assert subckt[0].lower() == ".subckt"

        cell_name = subckt[1]
        if cell_name != "challenge":
            assert subckt[2] in ["VGND", "VPWR"]
            assert subckt[3] in ["VGND", "VPWR"]
            self.cells.add(cell_name)
            while not next(self.s).lower().startswith(".ends"): pass
            return

        self.args = subckt[2:]
        while (line := next(self.s).split())[0].lower() != ".ends":
            self.parse_instantiation(line)

    def parse_spice(self, fn):
        with open(fn) as f:
            self.s = peekable(iter(f.readlines()))

        while not self.parse_subckt():
            pass

    def to_verilog(self):
        v = "module challenge(" + ", ".join(self.args) + ");\n"
        v += "".join(
            ("output " if "led" in a else "input ") +
            "wire " + a + ";\n"
            for a in self.args
        )
        v += "\n"

        v += "".join(
            "wire " + self.to_escaped_id(w) + ";\n"
            for w in self.wires
            if not w in self.args
        )

        v += "".join(
            name + " " + ident + "(" + ", ".join(map(self.to_escaped_id, args)) + ");\n"
            for (name, ident, args) in self.instances
        )

        v += "endmodule\n"
        return v

n = Netlist()
n.parse_spice("ext/challenge.spice")
print(n.to_verilog())
