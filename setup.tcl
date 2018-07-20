###################################################################
#
#  This TCL script is for setting up axi-huffman-encoder-core
#  Including synthesis, simulation, co-simulation, export-rtl
#  Copyright (c) 2018 Xing GUO
#
###################################################################

# Global settings
set project_name     huffman_encoding_core_build
set device           "xc7z020clg400-1"
set clock_period     10
set solution_dir     solution

# Open project
open_project $project_name -reset

# add files for synthesis
add_files {
  ./hls-src/huffman_canonize_tree.cpp 
  ./hls-src/huffman_create_tree.cpp 
  ./hls-src/huffman_filter.cpp 
  ./hls-src/huffman_compute_bit_length.cpp 
  ./hls-src/huffman_encoding.cpp 
  ./hls-src/huffman_sort.cpp 
  ./hls-src/huffman_create_codeword.cpp 
  ./hls-src/huffman_truncate_tree.cpp
}

# set top module
set_top huffman_encoding

# open solution
open_solution $solution_dir -reset

# set device part
set_part $device

# create clock
create_clock -period $clock_period

# C-simulation
# csim_design -compiler clang

# C-synthesis
csynth_design

# export_design 
# [Options]
#  -description  <string> 
#  -flow         <syn|impl> 
#  -format       <sysgen|ip_catalog|syn_dcp>
#  -library      <string>
#  -rtl          <verilog|vhdl>
#  -vendor       <string>
#  -version      <string>
export_design -flow syn -format ip_catalog -rtl verilog -vendor "com.xilinx.hls" -version "0.0.1"

# exit
exit

