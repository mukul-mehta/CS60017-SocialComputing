#
# clustering_coeff_amazon.elist. G(57168, 57378). Average clustering: 0.1906  OpenTriads: 120274 (0.9212)  ClosedTriads: 10294 (0.0788) (Thu Oct 22 16:09:24 2020)
#

set title "clustering_coeff_amazon.elist. G(57168, 57378). Average clustering: 0.1906  OpenTriads: 120274 (0.9212)  ClosedTriads: 10294 (0.0788)"
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
set output 'ccf.clustering_coeff_amazon.elist.png'
plot 	"ccf.clustering_coeff_amazon.elist.tab" using 1:2 title "" with linespoints pt 6
