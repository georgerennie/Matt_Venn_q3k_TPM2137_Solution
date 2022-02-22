#!/usr/bin/env python3

mapping = {
    "sky130_fd_sc_hd__decap_8": "",
    "sky130_fd_sc_hd__decap_3": "",
    "sky130_fd_sc_hd__inv_2": "assign Y = !A;",
    "sky130_fd_sc_hd__or2_4": "assign X = A || B;",
    "sky130_fd_sc_hd__diode_2": "",
    "sky130_fd_sc_hd__decap_6": "",
    "sky130_fd_sc_hd__decap_12": "",
    "sky130_fd_sc_hd__dfxtp_4": "reg Q;\nalways @(posedge CLK)\n\tQ <= D;""",
    "sky130_fd_sc_hd__and3_4": "assign X = A && B && C;",
    "sky130_fd_sc_hd__decap_4": "",
    "sky130_fd_sc_hd__buf_2": "assign X = A;",
    "sky130_fd_sc_hd__o21a_4": "assign X = ((A1 || A2) && B1);",
    "sky130_fd_sc_hd__a211o_4": "assign X = ((A1 && A2) || B1 || C1);",
    "sky130_fd_sc_hd__nor2_4": "assign Y = !(A || B);",
    "sky130_fd_sc_hd__or4_4": "assign X = A || B || C || D;",
    "sky130_fd_sc_hd__and4_4": "assign X = A && B && C && D;",
    "sky130_fd_sc_hd__o32a_4": "assign X = ((A1 || A2 || A3) && (B1 || B2));",
    "sky130_fd_sc_hd__clkbuf_1": "assign X = A;",
    "sky130_fd_sc_hd__and2_4": "assign X = A && B;",
    "sky130_fd_sc_hd__o22a_4": "assign X = ((A1 || A2) && (B1 || B2));",
    "sky130_fd_sc_hd__a21o_4": "assign X = ((A1 && A2) || B1);",
    "sky130_fd_sc_hd__or3_4": "assign X = A || B || C;",
    "sky130_fd_sc_hd__a2bb2o_4": "assign X = ((!A1_N && !A2_N) || (B1 && B2));",
    "sky130_fd_sc_hd__clkbuf_16": "assign X = A;",
    "sky130_fd_sc_hd__a32o_4": "assign X = ((A1 && A2 && A3) || (B1 && B2));"
}

def is_output(arg):
    return arg in ["Y", "X", "Q"]

with open("ext/challenge.spice") as f:
    lines = f.readlines()

for line in lines:
    line = line.split()

    if not line or not line[0].lower() == ".subckt" or line[1] == "challenge":
        continue

    name = line[1]
    args = line[2:]
    print("module", name + "(" + ", ".join(args) + ");")

    for arg in args:
        if is_output(arg):
            print("output", arg + ";")
        else:
            print("input", arg + ";")

    print(mapping[name])

    print("endmodule\n")
