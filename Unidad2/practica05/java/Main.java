import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;

/**
 * Uso:
 *   java Main generar [n] [semilla] [archivo.csv]   genera n valores y los guarda en CSV
 *   java Main periodo [semilla]                    recorre el ciclo completo y mide el período
 */
public final class Main {
    public static void main(String[] args) throws IOException {
        String mode = args.length > 0 ? args[0] : "generar";
        if (mode.equals("periodo")) {
            long seed = args.length > 1 ? Long.parseLong(args[1]) : Lcg.SEED;
            long start = System.nanoTime();
            long period = Lcg.period(seed);
            double seconds = (System.nanoTime() - start) / 1e9;
            System.out.printf(Locale.ROOT, "periodo=%d segundos=%.2f%n", period, seconds);
            return;
        }
        int n = args.length > 1 ? Integer.parseInt(args[1]) : 10_000;
        long seed = args.length > 2 ? Long.parseLong(args[2]) : Lcg.SEED;
        Path output = Path.of(args.length > 3 ? args[3] : "lcg_java.csv");

        Lcg lcg = new Lcg(seed);
        try (PrintWriter out = new PrintWriter(Files.newBufferedWriter(output, StandardCharsets.UTF_8))) {
            out.println("n,x,u");
            for (int i = 1; i <= n; i++) {
                long x = lcg.nextInt();
                out.printf(Locale.ROOT, "%d,%d,%.10f%n", i, x, (double) x / Lcg.M);
            }
        }
        System.out.printf("Java: %d valores con semilla %d guardados en %s%n", n, seed, output);
    }
}
