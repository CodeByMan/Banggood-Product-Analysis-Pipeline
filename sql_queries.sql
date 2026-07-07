-- Banggood Product Analysis SQL Queries
-- Table used by Python upload script: BanggoodProducts
-- Clean numeric columns used:
-- price_clean, old_price_clean, rating_clean, reviews_clean, discount_clean, discount_pct, value_score, price_bucket

-- 1. Preview all records
SELECT TOP 20 *
FROM BanggoodProducts;

-- 2. Total product count
SELECT COUNT(*) AS total_products
FROM BanggoodProducts;

-- 3. Product count per category
SELECT
    category,
    COUNT(*) AS total_products
FROM BanggoodProducts
GROUP BY category
ORDER BY total_products DESC;

-- 4. Average price per category
SELECT
    category,
    ROUND(AVG(price_clean), 2) AS average_price
FROM BanggoodProducts
WHERE price_clean IS NOT NULL
GROUP BY category
ORDER BY average_price DESC;

-- 5. Average rating per category
SELECT
    category,
    ROUND(AVG(rating_clean), 2) AS average_rating
FROM BanggoodProducts
WHERE rating_clean IS NOT NULL
GROUP BY category
ORDER BY average_rating DESC;

-- 6. Top 10 most reviewed products
SELECT TOP 10
    category,
    product_name,
    price_clean,
    rating_clean,
    reviews_clean,
    product_url
FROM BanggoodProducts
WHERE reviews_clean IS NOT NULL
ORDER BY reviews_clean DESC;

-- 7. Highest discount products
SELECT TOP 10
    category,
    product_name,
    price_clean,
    old_price_clean,
    discount_clean,
    discount_pct,
    product_url
FROM BanggoodProducts
WHERE discount_pct IS NOT NULL
ORDER BY discount_pct DESC;

-- 8. Best value products
SELECT TOP 10
    category,
    product_name,
    price_clean,
    rating_clean,
    reviews_clean,
    value_score,
    product_url
FROM BanggoodProducts
WHERE value_score IS NOT NULL
ORDER BY value_score DESC;

-- 9. Price bucket distribution
SELECT
    price_bucket,
    COUNT(*) AS total_products
FROM BanggoodProducts
WHERE price_bucket IS NOT NULL
GROUP BY price_bucket
ORDER BY total_products DESC;

-- 10. Average value score per category
SELECT
    category,
    ROUND(AVG(value_score), 2) AS average_value_score
FROM BanggoodProducts
WHERE value_score IS NOT NULL
GROUP BY category
ORDER BY average_value_score DESC;

-- 11. Category discount summary
SELECT
    category,
    ROUND(AVG(discount_pct), 2) AS average_discount_percentage,
    MAX(discount_pct) AS maximum_discount_percentage,
    MIN(discount_pct) AS minimum_discount_percentage
FROM BanggoodProducts
WHERE discount_pct IS NOT NULL
GROUP BY category
ORDER BY average_discount_percentage DESC;

-- 12. High-rated and highly-reviewed products
SELECT TOP 20
    category,
    product_name,
    price_clean,
    rating_clean,
    reviews_clean,
    value_score,
    product_url
FROM BanggoodProducts
WHERE rating_clean >= 4.5
  AND reviews_clean >= 100
ORDER BY reviews_clean DESC;

-- 13. Category price range analysis
SELECT
    category,
    MIN(price_clean) AS minimum_price,
    MAX(price_clean) AS maximum_price,
    ROUND(AVG(price_clean), 2) AS average_price
FROM BanggoodProducts
WHERE price_clean IS NOT NULL
GROUP BY category
ORDER BY average_price DESC;
