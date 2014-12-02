#!/usr/bin/gnuplot

unset key
set xlabel "number of gems"
set ylabel "gem price" offset 5,5
se log

se te png
se ou "gem_price.png"
p [:2000][2000:] "gem_price" w l lw 2
se ou

! display gem_price.png &
