#include <vector>
extern "C" {

    void computePnLSeries(double* strategy, int n, double* result) {
        result[0] = 1.0;
        for (int i = 1; i < n; i++) {
            result[i] = result[i-1] * (1.0 + strategy[i]);
        }
    }

}
