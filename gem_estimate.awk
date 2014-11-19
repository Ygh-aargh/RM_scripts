#!/usr/bin/awk -f
BEGIN {
    n = 0;
    p = 100000;
    s = 0;
    printf("%4s %6s %12s %s\n", "gem#", "price", "total cost", "source");
} {
    if ($1>n+1)
	for (i=n+1;i<$1;i++) {
	    e = $2**(log(i/n)/log($1/n)) * p**(log($1/i)/log($1/n))
	    s += e
	    printf("%4i %6.0f %12.0f %s\n", i, e, s, "est.");
	}
    n = $1;
    p = $2;
    s += p
    printf("%4i %6.0f %12.0f %s\n", n, p, s, $3);
}
