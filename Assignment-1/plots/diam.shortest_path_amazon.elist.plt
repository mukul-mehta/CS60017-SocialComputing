#
# shortest_path_amazon.elist. G(57168, 57378). Diam: avg:36.05  eff:54.20  max:116 (Thu Oct 22 16:09:24 2020)
#

set title "shortest_path_amazon.elist. G(57168, 57378). Diam: avg:36.05  eff:54.20  max:116"
set key bottom right
set logscale y 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "Number of hops"
set ylabel "Number of shortest paths"
set tics scale 2
set terminal png font arial 10 size 1000,800
set output 'diam.shortest_path_amazon.elist.png'
plot 	"diam.shortest_path_amazon.elist.tab" using 1:2 title "" with linespoints pt 6
