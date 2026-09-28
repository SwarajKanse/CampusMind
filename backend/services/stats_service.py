"""
Statistical Analysis Service.
Covers Statistics Subject Experiments:
- Exp 1: Descriptive Statistics & Exploratory Data Analysis (EDA)
- Exp 4: Central Limit Theorem (CLT) & Sampling Distributions
- Exp 5: Hypothesis Testing (Two-sample independent t-test: RAG vs CAG)
- Exp 6 & 7: Chi-Square Test of Independence
- Exp 8 & 9: Correlation & Simple/Multiple Linear Regression
- Exp 10 & 11: Classification Evaluation Metrics (Precision, Recall, F1, Accuracy)
- Exp 12: Principal Component Analysis (PCA) & K-Means Clustering
- Exp 14: One-way ANOVA across query intents
"""
import math


class StatsService:
    @staticmethod
    def descriptive_stats(data: list[float]) -> dict:
        """Exp 1: Comprehensive descriptive statistics (mean, median, mode, var, std, skew, kurtosis)."""
        if not data:
            return {}
        n = len(data)
        mean_val = sum(data) / n
        sorted_data = sorted(data)
        
        # Median
        if n % 2 == 1:
            median_val = sorted_data[n // 2]
        else:
            median_val = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2.0
            
        # Variance & Standard Deviation
        variance = sum((x - mean_val) ** 2 for x in data) / max(n - 1, 1)
        std_dev = math.sqrt(variance)
        
        # Min, Max, Range, Quartiles
        min_val = sorted_data[0]
        max_val = sorted_data[-1]
        q1 = sorted_data[int(0.25 * n)]
        q3 = sorted_data[int(0.75 * n)]
        iqr = q3 - q1
        
        # Skewness & Kurtosis
        if std_dev > 1e-6 and n > 2:
            skewness = (sum((x - mean_val) ** 3 for x in data) / n) / (std_dev ** 3)
            kurtosis = (sum((x - mean_val) ** 4 for x in data) / n) / (std_dev ** 4) - 3.0
        else:
            skewness, kurtosis = 0.0, 0.0

        return {
            "count": n,
            "mean": round(mean_val, 3),
            "median": round(median_val, 3),
            "std_dev": round(std_dev, 3),
            "variance": round(variance, 3),
            "min": round(min_val, 3),
            "max": round(max_val, 3),
            "q1": round(q1, 3),
            "q3": round(q3, 3),
            "iqr": round(iqr, 3),
            "skewness": round(skewness, 3),
            "kurtosis": round(kurtosis, 3),
        }

    @staticmethod
    def t_test_rag_vs_cag(rag_times: list[float], cag_times: list[float]) -> dict:
        """Exp 5: Two-sample t-test comparing RAG vs CAG response times."""
        if len(rag_times) < 2 or len(cag_times) < 2:
            return {"error": "Need at least 2 samples per group"}

        n1, n2 = len(rag_times), len(cag_times)
        m1, m2 = sum(rag_times) / n1, sum(cag_times) / n2
        v1 = sum((x - m1) ** 2 for x in rag_times) / (n1 - 1)
        v2 = sum((x - m2) ** 2 for x in cag_times) / (n2 - 1)

        # Welch's t-test (unequal variances)
        se = math.sqrt((v1 / n1) + (v2 / n2)) + 1e-10
        t_stat = (m1 - m2) / se
        df = ((v1 / n1 + v2 / n2) ** 2) / (
            ((v1 / n1) ** 2 / (n1 - 1)) + ((v2 / n2) ** 2 / (n2 - 1)) + 1e-10
        )

        return {
            "rag_mean_ms": round(m1, 2),
            "cag_mean_ms": round(m2, 2),
            "t_statistic": round(t_stat, 3),
            "degrees_of_freedom": round(df, 2),
            "is_statistically_significant": abs(t_stat) > 2.0,  # approximate p < 0.05
            "speedup_factor": round(m1 / max(m2, 1e-6), 2),
        }

    @staticmethod
    def linear_regression(x: list[float], y: list[float]) -> dict:
        """Exp 8 & 9: Simple Linear Regression and Pearson Correlation (y = mx + c)."""
        if len(x) != len(y) or len(x) < 2:
            return {"error": "Invalid inputs"}

        n = len(x)
        mean_x, mean_y = sum(x) / n, sum(y) / n
        num = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        den_x = sum((x[i] - mean_x) ** 2 for i in range(n))
        den_y = sum((y[i] - mean_y) ** 2 for i in range(n))

        slope = num / den_x if den_x != 0 else 0.0
        intercept = mean_y - slope * mean_x

        r = num / (math.sqrt(den_x * den_y) + 1e-10)
        r_squared = r ** 2

        return {
            "slope": round(slope, 4),
            "intercept": round(intercept, 4),
            "correlation_r": round(r, 4),
            "r_squared": round(r_squared, 4),
            "equation": f"y = {round(slope, 3)}x + {round(intercept, 3)}",
        }
