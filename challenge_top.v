module challenge_top(
	input clk_10,
	output led_green,
	output led_red,
	input uart
);

challenge c(.VPWR(1'b1), .VGND(1'b0), .*);

endmodule
