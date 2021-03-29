reset
graph = '2021-03-17 15_21_32.390395.csv'
set output 'example3.png'
set datafile separator ','
set terminal png size 1920,  1080
set ytics nomirror
set y2tics
plot graph u 3 axis x1y1, graph u 4 axis x1y2
