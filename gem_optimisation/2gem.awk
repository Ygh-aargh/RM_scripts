#!/usr/bin/awk -f
BEGIN {
  t[1]=0; g[1]=0;
  t[2]=1; g[2]=1;
  t[3]=2; g[3]=2;
  t[4]=3; g[4]=4;
  t[5]=4; g[5]=8;
  t[6]=6; g[6]=16;
  t[7]=8; g[7]=32;
  t[8]=11; g[8]=64;
  t[9]=15; g[9]=128;
  t[10]=21; g[10]=256;
  t[11]=30; g[11]=512;
  t[12]=45; g[12]=1024;
  t[13]=60; g[13]=2048;
  t[14]=80; g[14]=4096;
  t[15]=100; g[15]=8192;
  t[16]=120; g[16]=16384;
  t[17]=125; g[17]=16884;
  t[18]=130; g[18]=17484;
  t[19]=135; g[19]=18284;
  t[20]=140; g[20]=19284;
  t[21]=145; g[21]=20484;
  t[22]=150; g[22]=21984;
  t[23]=155; g[23]=23784;
  t[24]=160; g[24]=25984;
  t[25]=165; g[25]=28584;
  t[26]=170; g[26]=31684;
  t[27]=175; g[27]=35384;
  t[28]=180; g[28]=39784;
  t[29]=185; g[29]=44984;
  t[30]=200; g[30]=51084;
  max=30;
  for (i=1; i<=max; i++)
    for (j=i; j<=max; j++)
      print t[i]+t[j], g[i]+g[j], i-1, j-1;
  # ./2gem.awk | sort -n -k 2 | awk 'BEGIN {o=-1} {if ($1>o) { print ; o=$1}}'| column -t | grep -C 100 -E '{|15|19|24|29|}' > __
  # gnuplot
  # p "__" u 2:1, "" u 2:($3*10), "" u 2:($4*10)
}
