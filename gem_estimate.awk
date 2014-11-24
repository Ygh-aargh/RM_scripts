#!/usr/bin/awk -f
BEGIN {
    n = 0;
    p = 100000;
    s = 0;
    r[1]   = "Lv. 1 gem +100k for socket"
    r[2]   = "Lv. 2 gem +100k for socket"
    r[4]   = "Lv. 3 gem +100k for socket OR 2 * Lv. 2 gems + 200k for sockets"
    r[6]   = "3 * Lv. 2 gems + 300k for 3 sockets"
    r[8]   = "Lv. 4 gem +100k for socket OR 2 * Lv. 3 gems + 200k for sockets"
    r[12]  = "3 * Lv. 3 gems + 300k for sockets"
    r[16]  = "Lv. 5 gem +100k for socket OR 4 * Lv. 3 gems + 400k for sockets"
    r[20]  = "5 * Lv. 3 gems + 500k for sockets"
    r[24]  = "3 * Lv. 4 gems + 300k for sockets"
    r[32]  = "Lv. 6 gem +100k for socket OR 4 * Lv. 4 gems + 400k for sockets"
    r[40]  = "5 * Lv. 4 gems + 500k for sockets"
    r[48]  = "6 * Lv. 4 gems + 600k for sockets"
    r[64]  = "Lv. 7 gem +100k for socket"
    r[96]  = "6 * Lv. 5 gems + 600k for sockets"
    r[128] = "Lv. 8 gem +100k for socket"
    r[256] = "2 * Lv. 8 gem +200k for 2 sockets"
    r[384] = "3 * Lv. 8 gem +300k for 3 sockets"
    r[512] = "4 * Lv. 8 gem +400k for 4 sockets"
    r[640] = "5 * Lv. 8 gem +500k for 5 sockets"
    r[768] = "6 * Lv. 8 gem +600k for 6 sockets"
    printf("#%4s %6s %12s %10s %s\n", "gem#", "price", "total cost", "source", "remarks");
} {
    if ($1>n+1)
	for (i=n+1;i<$1;i++) {
	    e = $2**(log(i/n)/log($1/n)) * p**(log($1/i)/log($1/n))
	    s += e
	    printf("%5i %6.0f %12.0f %10s %s\n", i, e, s, "~", r[i]);
	}
    n = $1;
    p = $2;
    s += p
    printf("%5i %6.0f %12.0f %10s %s\n", n, p, s, $3, r[n]);
}
