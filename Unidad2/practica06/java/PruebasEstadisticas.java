import java.util.Arrays;

/** Pruebas de bondad de ajuste frente a U(0,1): Chi-cuadrado y Kolmogorov-Smirnov. */
public final class PruebasEstadisticas {
    public static final double ALPHA = 0.05;

    private PruebasEstadisticas() {
    }

    public record ChiCuadrado(int[] observadas, double esperada, double estadistico, int gl, double p) {
        public boolean rechaza() {
            return p < ALPHA;
        }
    }

    public record KolmogorovSmirnov(double dMas, double dMenos, double estadistico, double p) {
        public boolean rechaza() {
            return p < ALPHA;
        }
    }

    public static ChiCuadrado chiCuadrado(double[] values, int k) {
        int[] observed = new int[k];
        for (double u : values) {
            observed[Math.min((int) (u * k), k - 1)]++;
        }
        double expected = (double) values.length / k;
        double statistic = 0;
        for (int o : observed) {
            statistic += (o - expected) * (o - expected) / expected;
        }
        int df = k - 1;
        return new ChiCuadrado(observed, expected, statistic, df, chi2Sf(statistic, df));
    }

    public static KolmogorovSmirnov kolmogorovSmirnov(double[] values) {
        double[] ordered = values.clone();
        Arrays.sort(ordered);
        int n = ordered.length;
        double dPlus = 0;
        double dMinus = 0;
        for (int i = 0; i < n; i++) {
            dPlus = Math.max(dPlus, (i + 1.0) / n - ordered[i]);
            dMinus = Math.max(dMinus, ordered[i] - (double) i / n);
        }
        double d = Math.max(dPlus, dMinus);
        double sqrtN = Math.sqrt(n);
        double p = ksSf((sqrtN + 0.12 + 0.11 / sqrtN) * d);   // corrección de Stephens
        return new KolmogorovSmirnov(dPlus, dMinus, d, p);
    }

    /** P(χ²_df > x) mediante la función gamma incompleta regularizada Q(df/2, x/2). */
    public static double chi2Sf(double x, int df) {
        return regularizedGammaQ(df / 2.0, x / 2.0);
    }

    /** Distribución de Kolmogorov: P(K > λ) = 2 Σ (-1)^(j-1) e^(-2 j² λ²). */
    public static double ksSf(double lambda) {
        if (lambda < 0.2) {
            return 1.0;
        }
        double total = 0;
        for (int j = 1; j <= 100; j++) {
            double term = (j % 2 == 1 ? 1 : -1) * Math.exp(-2.0 * j * j * lambda * lambda);
            total += term;
            if (Math.abs(term) < 1e-16) {
                break;
            }
        }
        return Math.max(0, Math.min(1, 2 * total));
    }

    private static double regularizedGammaQ(double s, double x) {
        if (x <= 0) {
            return 1.0;
        }
        double logPrefix = -x + s * Math.log(x) - logGamma(s);
        if (x < s + 1) {
            double term = 1.0 / s;
            double total = term;
            double k = s;
            while (Math.abs(term) > Math.abs(total) * 1e-15) {
                k += 1;
                term *= x / k;
                total += term;
            }
            return 1.0 - total * Math.exp(logPrefix);
        }
        double tiny = 1e-300;
        double b = x + 1 - s;
        double c = 1 / tiny;
        double d = 1 / b;
        double h = d;
        for (int i = 1; i < 300; i++) {
            double an = -i * (i - s);
            b += 2;
            d = an * d + b;
            if (Math.abs(d) < tiny) {
                d = tiny;
            }
            c = b + an / c;
            if (Math.abs(c) < tiny) {
                c = tiny;
            }
            d = 1 / d;
            double delta = d * c;
            h *= delta;
            if (Math.abs(delta - 1) < 1e-15) {
                break;
            }
        }
        return h * Math.exp(logPrefix);
    }

    /** ln Γ(x) con la aproximación de Lanczos (g = 7, 9 coeficientes); Java no la trae en Math. */
    static double logGamma(double x) {
        double[] coef = {0.99999999999980993, 676.5203681218851, -1259.1392167224028,
            771.32342877765313, -176.61502916214059, 12.507343278686905,
            -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7};
        if (x < 0.5) {
            return Math.log(Math.PI / Math.abs(Math.sin(Math.PI * x))) - logGamma(1 - x);
        }
        x -= 1;
        double sum = coef[0];
        for (int i = 1; i < coef.length; i++) {
            sum += coef[i] / (x + i);
        }
        double t = x + 7.5;
        return 0.5 * Math.log(2 * Math.PI) + (x + 0.5) * Math.log(t) - t + Math.log(sum);
    }
}
