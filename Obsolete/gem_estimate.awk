#!/usr/bin/awk -f
BEGIN {
    n = 0
    p = 100000
    s = 0
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
    r[208] = "Lv. 8 + 5 * Lv. 5 gems + 600k for sockets"
    r[256] = "2 * Lv. 8 gem +200k for 2 sockets"
    r[320] = "2 * Lv. 8 + 4 * Lv. 5 gems + 600k for sockets"
    r[384] = "3 * Lv. 8 gems +300k for 3 sockets"
    r[432] = "3 * Lv. 8 + 3 * Lv. 5 gems + 600k for sockets"
    r[512] = "4 * Lv. 8 gems +400k for 4 sockets, Lv. 10 gem +100k for socket"
    r[544] = "4 * Lv. 8 + 2 * Lv. 5 gems + 600k for sockets"
    r[640] = "5 * Lv. 8 gems +500k for 5 sockets"
    r[656] = "5 * Lv. 8 + Lv. 5 gems + 600k for sockets"
    r[768] = "6 * Lv. 8 gems +600k for 6 sockets"
    r[1024] = "2 * Lv. 10 gems +200k for 2 sockets"
    r[1152] = "Lv. 10 + 5 * Lv. 8 gems + 600k for sockets"
    r[1536] = "3 * Lv. 10 gems +300k for 3 sockets, 2 * Lv. 10 + 4 * Lv. 8 gems + 600k for sockets"
    r[1920] = "3 * Lv. 10 + 3 * Lv. 8 gems + 600k for sockets"
    r[2048] = "4 * Lv. 10 gems +400k for 4 sockets"
    r[2304] = "4 * Lv. 10 + 2 * Lv. 8 gems + 600k for sockets"
    r[2560] = "5 * Lv. 10 gems +500k for 5 sockets"
    r[2688] = "5 * Lv. 10 + Lv. 8 gem + 600k for sockets"
    r[3072] = "6 * Lv. 10 gems +600k for 6 sockets"
    maxn = 3072
} {
    if ($1 !~ "#" && NF>=3) {
	if ($1 == 1) printf("#%4s %6s %12s %12s %s\n", "gem#", "price", "total cost", "reduction", "remarks");
        if ($1 > n+1)
            for (i=n+1; i<$1; i++) {
                #e = $2**(log(i/n)/log($1/n)) * p**(log($1/i)/log($1/n))
                e = p + ($2-p)*(i-n)/($1-n)
                s += e
                printf("%5i %6.0f %12.0f %12s %s\n", i, e, s, "~", r[i]);
            }
        n = $1
        p = $2
        s += p
        printf("%5i %6.0f %12.0f %12s %s\n", n, p, s, $3" "$4, r[n]);
    } else print
}
END {
    e = 3000
    for (i=n+1; i<=maxn; i++) {
	s += e
	if (length(r[i]) > 0) printf("%5i %6.0f %12.0f %12s %s\n", i, e, s, "~", r[i]);
    }
}
