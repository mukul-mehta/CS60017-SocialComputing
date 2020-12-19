#
# clustering_coeff_facebook.elist. G(3213, 57832). Average clustering: 0.6000  OpenTriads: 2501793 (0.7434)  ClosedTriads: 863556 (0.2566) (Thu Oct 22 16:07:08 2020)
#

set title "clustering_coeff_facebook.elist. G(3213, 57832). Average clustering: 0.6000  OpenTriads: 2501793 (0.7434)  ClosedTriads: 863556 (0.2566)"
set key bottom right
set logscale xy 10
set format x "10^{%L}"
set mxtics 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "Node degree"
set ylabel "Average clustering coefficient"
set tics scale 2
set terminal png font arial 10 size 1000,800
set output 'ccf.clustering_coeff_facebook.elist.png'
plot 	"ccf.clustering_coeff_facebook.elist.tab" using 1:2 title "" with linespoints pt 6
