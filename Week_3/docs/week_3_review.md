![Week 3 Review Image](Chinook_data_model.jpg)

> I used Duckdb for my database and not the traditional databases as MySQL/PostgreSQl hence did not include Indexing since its columnar
> I know the trade-offs in indexing: They speed up reads(selects) but slow down writes(UPDATE/INSERT) because the data updates the index when it changes

## Chinook Database Analysis — Key Insights

### Note on execution

Statement 1 (`USE chinook`) throws a harmless `NoneType` error in the loop — this is expected. `USE` doesn't return a result set the way `SELECT` does, so `.df()` has nothing to convert. The statement still executes correctly; the error can be ignored or the loop can be adjusted to skip `.df()` for non-SELECT statements.

### 1. Customer Base Composition

The customer base spans 24 countries, but is heavily concentrated: the **USA (13 customers)** and **Canada (8 customers)** together make up roughly 36% of all customers. Only two other countries — France and Brazil — have 5 customers each; every other country has 1–4. This is a classic long-tail distribution, meaning marketing or support efforts concentrated on North America would reach the largest single share of the customer base, but a large portion of revenue potential is scattered thinly across Europe and South America.

### 2. Revenue Is Driven by Volume, Not Standout Products

The top-performing track by revenue is "The Trooper" at $4.95, but nearly every other top track sits at exactly $3.98 — the result of the $0.99-per-track pricing being uniform across the catalog. **This tells us product-level revenue in Chinook is driven almost entirely by units sold, not price variation.** There's no premium-pricing strategy at play, so any "top product" analysis here is really a popularity ranking, not a margin ranking.

### 3. Customer Spend Is Tightly Clustered

The top spender (Customer 6, Helena Holý) spent $49.62; the tenth-highest spent $42.62 — a gap of only $7 across the entire top 10. Compare that to the overall average invoice of **$5.65** — even top customers aren't dramatically outspending the average customer, they're just ordering slightly more consistently. **There's no clear "whale" customer** who dominates revenue; the spending is fairly evenly distributed among engaged customers, which the "Repeat vs One-time" query confirms directly.

### 4. Every Customer Is a Repeat Customer

The repeat-vs-one-time breakdown returned a striking result: **all 59 customers are classified as repeat customers, 0 are one-time.** This is a strong signal of good historical retention — but it's also worth flagging as a possible data-completeness artifact of the Chinook sample dataset (it's a demo database, not real transactional data), so this finding shouldn't be treated as a realistic real-world retention rate without a caveat noting the dataset's synthetic nature.

### 5. Revenue Trends Are Remarkably Stable, With Occasional Spikes

Monthly revenue holds almost perfectly steady at **$37.62/month** for most of the 2021–2025 range, which strongly suggests this is a simulated/generated dataset with a near-fixed number of invoices per month (consistently 6–7), rather than organic, naturally fluctuating business activity. The few real spikes worth highlighting:

- **Jan 2022: +39.87%** month-over-month — the largest single jump
- **Nov 2023: −36.84%**, immediately followed by **Dec 2023: +58.33%** — the sharpest single-month swing in the dataset
- **Nov 2025: +31.90%**, the most recent notable spike

If this were a real production dataset, these would be the specific months to investigate first — for a demo dataset, they're most useful as a demonstration that your `LAG()`/growth-rate query correctly detects volatility.

### 6. Genre Popularity Is Broad, Not Concentrated

The genre-partitioned ranking (top 3 tracks per genre) returned **277 rows** across all genres, and nearly every top track within its genre sits at the same $0.99 floor price with no clear runaway genre leader. Combined with the customer-genre breakdown (**440 rows**) showing customers typically engage with **4–5 different genres each**, the catalog data suggests customer taste is broad rather than niche — most customers aren't loyal to a single genre, they sample across several.

### 7. Query Optimization Findings

`EXPLAIN` on the `CustomerId = 5` filter confirmed DuckDB executing a scan-based physical plan rather than an index lookup — expected, since DuckDB is a **columnar OLAP engine** that optimizes scans via zone maps rather than traditional B-tree indexes. This is the core takeaway for the documentation's optimization section: **the indexing concepts (CREATE INDEX, B-tree lookups) are correct for row-store databases like Postgres/MySQL, but DuckDB's performance model is fundamentally different** — worth stating explicitly so a reviewer doesn't think the indexing knowledge is missing, just correctly adapted to the tool being used.

---

### Summary takeaway for your documentation

This SQL portfolio piece demonstrates the full range of required skills — filtering, aggregation, joins, subqueries, window functions with partitioning, and time-series analysis — against a dataset whose business "story" is thin (synthetic, evenly distributed data) but whose **query correctness and technique coverage is strong**. The most defensible, real insight is the country concentration finding (#1) and the genre-breadth finding (#6), since those reflect actual structural properties of the data rather than artifacts of how Chinook was generated.

---
