#!/usr/bin/gnuplot

unset key
set xlabel "number of gems"
set ylabel "gem price" offset 5,5
se log

se te png
se ou "gem_price.png"
p [:2000][2000:] "gem_est.txt" w l lw 2
se ou

#p [:2000][2000:] "gem_est.txt" w lp, "gem_price" w p, 110000-10000*x, 95000-5000*x, 74000-2000*x, 59000-1000*x, 44500-500*x, 26800-200*x, 12400-20*x, 11200-10*x, 8185-5*x, 3000

! display gem_price.png &
