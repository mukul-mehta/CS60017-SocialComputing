#
# shortest_path_facebook.elist. G(3213, 57832). Diam: avg:4.28  eff:6.35  max:17 (Thu Oct 22 16:07:08 2020)
#

set title "shortest_path_facebook.elist. G(3213, 57832). Diam: avg:4.28  eff:6.35  max:17"
set key bottom right
set logscale y 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "Number of hops"
set ylabel "Number of shortest paths"
set tics scale 2
set terminal png font arial 10 size 1000,800
set output 'diam.shortest_path_facebook.elist.png'
plot 	"diam.shortest_path_facebook.elist.tab" using 1:2 title "" with linespoints pt 6
