#
# connected_comp_facebook.elist. G(3213, 57832). Largest component has 0.993464 nodes (Thu Oct 22 16:07:08 2020)
#

set title "connected_comp_facebook.elist. G(3213, 57832). Largest component has 0.993464 nodes"
set key bottom right
set logscale xy 10
set format x "10^{%L}"
set mxtics 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "Size of strongly connected component"
set ylabel "Number of components"
set tics scale 2
set terminal png font arial 10 size 1000,800
set output 'scc.connected_comp_facebook.elist.png'
plot 	"scc.connected_comp_facebook.elist.tab" using 1:2 title "" with linespoints pt 6
