# 06 ML PIPELINE

**PRD Version:** 2.1.1
**Last Updated:** February 1, 2026
**Related:** [Index](00_INDEX.md)

---

## 9. MACHINE LEARNING PIPELINE

### Feature Engineering

**Raw YouTube Features:**

- views (integer)
- likes (integer)
- comments (integer)
- subscriber_count (integer)
- upload_date (timestamp)

**Calculated Features:**

```python
# Primary viral indicator
v_score = views / subscriber_count

# Engagement metrics
like_view_ratio = likes / views
comment_view_ratio = comments / views
engagement_rate = (likes + comments) / views

# Temporal features
upload_age_days = (today - upload_date).days
viral_velocity = views / upload_age_days
```

**Feature Importance Ranking:**


| Feature | Weight | Justification |
| :-- | :-- | :-- |
| v_score | 50% | Primary indicator of organic virality (high views despite low subs) |
| engagement_rate | 30% | Measures audience interaction quality |
| viral_velocity | 20% | Indicates momentum (fast growth = trending content) |


---

### Isolation Forest (Stage 3)

**Algorithm:** Anomaly detection via isolation

**How It Works:**

- Build ensemble of random decision trees
- Anomalies (outliers) are isolated faster (require fewer splits)
- Videos with abnormally high V-Scores are classified as outliers

**Hyperparameters:**

```python
contamination=0.1      # Expect 10% of data to be outliers (~50 from 500)
random_state=42        # Reproducible results (same input = same output)
n_estimators=100       # Number of trees in ensemble
max_features=1.0       # Use all features
bootstrap=False        # Use full dataset per tree
```

**Input Features:** `[v_score, views, upload_age_days]`

**Output:** Binary classification (1 = inlier, -1 = outlier)

**Expected Result:** 500 videos → ~50 outlier candidates

---

### DBSCAN (Stage 4)

**Algorithm:** Density-based clustering

**How It Works:**

- Identify high-density clusters (normal viral videos with similar patterns)
- Points that don't belong to any cluster = NOISE (true outliers)
- Noise points have unique engagement patterns (organic viral, not paid promotion)

**Hyperparameters:**

```python
eps=0.5                # Neighborhood radius (distance threshold)
min_samples=3          # Minimum points to form cluster
metric='euclidean'     # Distance metric
```

**Input Features:** `[like_view_ratio, comment_view_ratio, v_score]` (StandardScaled)

**Output:** Cluster labels (0, 1, 2... = cluster ID, -1 = noise/outlier)

**Expected Result:** 50 candidates → ~10-15 true outliers

---

### Adaptive Thresholding (Per-Niche Calibration)

Different niches have different "normal" V-Score distributions:

```python
def calculate_adaptive_contamination(videos_df):
    """
    Adjust Isolation Forest contamination based on niche variance.
    
    Logic:
    - High variance niche → More outliers expected → Higher contamination
    - Low variance niche → Fewer outliers expected → Lower contamination
    """
    v_scores = videos_df['v_score']
    
    median = v_scores.median()
    p90 = v_scores.quantile(0.90)
    variance_ratio = p90 / median
    
    if variance_ratio > 5:
        # High variance (e.g., Tech reviews, Gaming)
        contamination = 0.15
    elif variance_ratio > 3:
        # Medium variance (e.g., Education, Finance)
        contamination = 0.10
    else:
        # Low variance (e.g., Music covers, ASMR)
        contamination = 0.08
    
    return contamination
```

**Example Niche Profiles:**


| Niche | Median V-Score | P90 V-Score | Variance Ratio | Contamination |
| :-- | :-- | :-- | :-- | :-- |
| History Docs | 3.5 | 18.2 | 5.2 | 0.15 (high variance) |
| Tech Reviews | 2.8 | 9.4 | 3.4 | 0.10 (medium variance) |
| ASMR | 4.2 | 8.1 | 1.9 | 0.08 (low variance) |


---

### Hard Filter Rules (Updated)

**Criteria:**

| Rule | Value | Purpose |
| :-- | :-- | :-- |
| subscriber_count | <= 30,000 | Small channels only (viral potential) |
| views | >= 50,000 | Minimum viral threshold |
| views | <= subscriber_count × 50 | Anti-paid promotion (organic viral only) |
| upload_age_days | >= 7 | Exclude brand new videos |
| upload_age_days | <= 21 | Recent viral only (max 3 weeks) |

**Views/Subs Ratio Examples:**

| Subscribers | Views | Ratio (views/subs) | Status |
| :-- | :-- | :-- | :-- |
| 1,000 | 50,000 | 50x | ✅ Valid (at threshold) |
| 1,000 | 200,000 | 200x | ❌ Paid promotion (exceeds 50x) |
| 5,000 | 50,000 | 10x | ✅ Valid |
| 5,000 | 500,000 | 100x | ❌ Paid promotion |
| 10,000 | 100,000 | 10x | ✅ Valid |
| 10,000 | 2,000,000 | 200x | ❌ Paid promotion |


---

