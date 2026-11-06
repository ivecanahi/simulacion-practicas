/** Generador Congruencial Lineal: X(n+1) = (a·X(n) + c) mod m, con m potencia de 2 (m <= 2^32). */
public final class Lcg {
    private final long a;
    private final long c;
    private final long m;
    private final long mask;
    private long state;

    public Lcg(long a, long c, long m, long seed) {
        boolean powerOfTwo = m > 0 && (m & (m - 1)) == 0;
        if (!powerOfTwo || m > (1L << 32) || a < 0 || a >= m || c < 0 || c >= m || seed < 0 || seed >= m) {
            throw new IllegalArgumentException("m debe ser potencia de 2 (<= 2^32) y a, c, semilla en [0, m)");
        }
        this.a = a;
        this.c = c;
        this.m = m;
        this.mask = m - 1;
        this.state = seed;
    }

    public Lcg(long seed) {
        this(1664525L, 1013904223L, 1L << 32, seed);
    }

    public long nextInt() {
        // a·X + c puede pasar de 2^63 y desbordarse, pero Java calcula módulo 2^64.
        // Como m divide a 2^64, aplicar la máscara (x mod m) da el resultado exacto.
        state = (a * state + c) & mask;
        return state;
    }

    public double nextUniform() {
        return (double) nextInt() / m;
    }

    public double[] uniforms(int n) {
        double[] values = new double[n];
        for (int i = 0; i < n; i++) {
            values[i] = nextUniform();
        }
        return values;
    }
}
