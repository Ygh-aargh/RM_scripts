#!/usr/bin/gnuplot

unset key
set xlabel "number of gems"
set ylabel "gem price" offset 5,5
se log

se te png
se ou "gem_price.png"
p [:1200][2900:] "gem_price" w lp
se ou

! display gem_price.png &
