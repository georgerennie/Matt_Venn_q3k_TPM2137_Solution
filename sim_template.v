module bench;

localparam TIME = 870;

reg clk_10 = 0;
always #5 clk_10 = !clk_10;

reg uart;
wire led_green, led_red;

challenge_top top(.*);

// initial begin
//         $dumpfile("bench.vcd");
//         $dumpvars(0);
// end

initial begin
    uart = 1;
    #TIME;
    #TIME;

    {% for byte in bits|batch(8) %}
    #TIME uart = 0;

    {% for bit in byte -%}
    #TIME uart = 1'b{{bit}};
    {% endfor %}

    #TIME uart = 1;
    {% endfor %}

    #TIME;

    {% for out in outputs -%}
    $write(top.\{{out}} );
    {% endfor -%}

    $finish;
end

endmodule
