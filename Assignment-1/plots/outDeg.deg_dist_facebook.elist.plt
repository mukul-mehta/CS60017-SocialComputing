#
# deg_dist_facebook.elist. G(3213, 57832). 1056 (0.3287) nodes with out-deg > avg deg (36.0), 489 (0.1522) with >2*avg.deg (Thu Oct 22 16:06:55 2020)
#

set title "deg_dist_facebook.elist. G(3213, 57832). 1056 (0.3287) nodes with out-deg > avg deg (36.0), 489 (0.1522) with >2*avg.deg"
set key bottom right
set logscale xy 10
set format x "10^{%L}"
set mxtics 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "Out-degree"
set ylabel "Count"
set tics scale 2
set terminal png font arial 10 size 1000,800
set output 'outDeg.deg_dist_facebook.elist.png'
plot 	"outDeg.deg_dist_facebook.elist.tab" using 1:2 title "" with linespoints pt 6
