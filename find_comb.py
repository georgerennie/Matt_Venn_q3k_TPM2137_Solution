#! /usr/bin/env python3

from jinja2 import Template
import json
from prodict import Prodict
from collections import defaultdict
from pysmt.shortcuts import FreshSymbol, Not, And, Or, Iff, get_model, TRUE
import subprocess

with open("synth/challenge.json") as f:
    m = Prodict.from_dict(json.load(f)).modules.challenge_top

net_map = {}
for (name, net) in m.netnames.items():
    assert len(net.bits) == 1
    assert not net.bits[0] in net_map
    net_map[net.bits[0]] = name

# lists of drivers connected to each net
conn_map = dict()
for (cell_name, cell) in m.cells.items():
    for (conn_name, conn) in cell.connections.items():
        assert len(conn) == 1
        assert cell.port_directions[conn_name] in ["input", "output"]

        if cell.port_directions[conn_name] == "output":
            assert not conn[0] in conn_map
            conn_map[conn[0]] = cell_name

# Get the list of driver nets, as well as constructing a symbolic model in the
# process
symb_map = defaultdict(FreshSymbol)
clauses = []
def get_driver_ffs(net):
    driver = m.cells[conn_map[net]]

    if driver.type == "$dff":
        return {net}

    elif driver.type == "$logic_and":
        a = symb_map[driver.connections.A[0]]
        b = symb_map[driver.connections.B[0]]
        y = symb_map[driver.connections.Y[0]]
        clauses.append(y.Iff(a.And(b)))

    elif driver.type == "$logic_or":
        a = symb_map[driver.connections.A[0]]
        b = symb_map[driver.connections.B[0]]
        y = symb_map[driver.connections.Y[0]]
        clauses.append(y.Iff(a.Or(b)))

    elif driver.type == "$logic_not":
        a = symb_map[driver.connections.A[0]]
        y = symb_map[driver.connections.Y[0]]
        clauses.append(y.Iff(Not(a)))

    else:
        assert False

    ffs = set()
    for (conn_name, conn) in driver.connections.items():
        if driver.port_directions[conn_name] == "input":
            ffs.update(get_driver_ffs(conn[0]))

    return ffs

# Find FF outputs that are combinationally reachable from led_green
exit_net = m.netnames.led_green.bits[0]
drivers = list(get_driver_ffs(exit_net))
assert len(drivers) == 64

# Find assignments that make the model true
formula = And(*clauses, Not(symb_map[exit_net]))
model = get_model(formula)

target = [int(model.get_py_value(symb_map[net])) for net in drivers]

def hamming_distance(a, b):
    assert len(a) == len(b)
    s = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            s += 1
    return s

with open("sim_template.v") as f:
    t = Template(f.read())

def sim(bits):
    tb = t.render(bits=bits, outputs=map(net_map.get, drivers))
    subprocess.run(["mkdir", "-p", "sim"])
    with open("sim/tb.v", "w+") as f:
        f.write(tb)
    subprocess.run(["iverilog", "-g2012", "sim/tb.v", "synth/challenge_synth.v", "-o", "sim/tb.vvp"])
    output = subprocess.Popen("vvp sim/tb.vvp", shell=True, stdout=subprocess.PIPE).stdout.read()

    assert len(output) == 64
    return [int(c == ord('1')) for c in output]

result_bin = []
for i in range(64):
    bits = [0 for _ in range(64)]
    bits[i] = 1

    res = sim(bits)
    assert sum(res) == 1

    output_idx = res.index(1)
    result_bin.append(target[output_idx])

result = ""
for idx in range(0, len(result_bin), 8):
    byte_list = result_bin[idx:idx+8]
    byte_list.reverse()
    byte_int = int("".join(map(str, byte_list)), 2)
    char = chr(byte_int)
    # print(byte_list, byte_int, char)
    result += char

print(result)
