import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;

/**
 * Uso:
 *   java Main generar n semilla archivo.csv      guarda n valores del LCG de la guía
 *   java Main pruebas a c m semilla n            aplica Chi-cuadrado (k = 10) y KS
 *   java Main pi n semilla                       estima π con n puntos y mide el tiempo
 */
public final class Main {
    public static void main(String[] args) throws IOException {
        String mode = args.length > 0 ? args[0] : "pruebas";
        switch (mode) {
            case "generar" -> generate(Integer.parseInt(args[1]), Long.parseLong(args[2]), Path.of(args[3]));
            case "pruebas" -> tests(args);
            case "pi" -> pi(Integer.parseInt(args[1]), Long.parseLong(args[2]));
            default -> throw new IllegalArgumentException("modo desconocido: " + mode);
        }
    }

    private static void generate(int n, long seed, Path output) throws IOException {
        Lcg lcg = new Lcg(seed);
        try (PrintWriter out = new PrintWriter(Files.newBufferedWriter(output, StandardCharsets.UTF_8))) {
            out.println("n,x,u");
            for (int i = 1; i <= n; i++) {
                long x = lcg.nextInt();
                out.printf(Locale.ROOT, "%d,%d,%.10f%n", i, x, (double) x / (1L << 32));
            }
        }
    }

    private static void tests(String[] args) {
        long a = args.length > 1 ? Long.parseLong(args[1]) : 1664525L;
        long c = args.length > 2 ? Long.parseLong(args[2]) : 1013904223L;
        long m = args.length > 3 ? Long.parseLong(args[3]) : 1L << 32;
        long seed = args.length > 4 ? Long.parseLong(args[4]) : 12345L;
        int n = args.length > 5 ? Integer.parseInt(args[5]) : 10_000;

        double[] values = new Lcg(a, c, m, seed).uniforms(n);
        PruebasEstadisticas.ChiCuadrado chi = PruebasEstadisticas.chiCuadrado(values, 10);
        PruebasEstadisticas.KolmogorovSmirnov ks = PruebasEstadisticas.kolmogorovSmirnov(values);
        System.out.printf(Locale.ROOT, "chi2=%.6f gl=%d p_chi2=%.6e d_mas=%.8f d_menos=%.8f d=%.8f p_ks=%.6e%n",
                chi.estadistico(), chi.gl(), chi.p(), ks.dMas(), ks.dMenos(), ks.estadistico(), ks.p());
    }

    private static void pi(int n, long seed) {
        long start = System.nanoTime();
        Lcg lcg = new Lcg(seed);
        long inside = 0;
        for (int i = 0; i < n; i++) {
            double x = lcg.nextUniform();
            double y = lcg.nextUniform();
            if (x * x + y * y <= 1.0) {
                inside++;
            }
        }
        double estimate = 4.0 * inside / n;
        double seconds = (System.nanoTime() - start) / 1e9;
        System.out.printf(Locale.ROOT, "pi=%.10f segundos=%.9f%n", estimate, seconds);
    }
}
