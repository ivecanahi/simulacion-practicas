/** Generador Congruencial Lineal: X(n+1) = (a·X(n) + c) mod m, con m = 2^32. */
public final class Lcg {
    public static final long A = 1664525L;
    public static final long C = 1013904223L;
    public static final long M = 1L << 32;
    public static final long SEED = 12345L;
    private static final long MASK = M - 1;   // x mod 2^32 == x & (2^32 - 1)

    private long state;

    public Lcg(long seed) {
        if (seed < 0 || seed >= M) {
            throw new IllegalArgumentException("la semilla debe estar en [0, 2^32)");
        }
        this.state = seed;
    }

    public long nextInt() {
        // a·X < 2^21 · 2^32 = 2^53, cabe en un long sin desbordamiento.
        state = (A * state + C) & MASK;
        return state;
    }

    public double nextFloat() {
        return (double) nextInt() / M;
    }

    /** Pasos hasta volver a la semilla. Como a es impar, la función es biyectiva y la secuencia es puramente periódica. */
    public static long period(long seed) {
        long x = seed;
        long steps = 0;
        do {
            x = (A * x + C) & MASK;
            steps++;
        } while (x != seed);
        return steps;
    }
}
