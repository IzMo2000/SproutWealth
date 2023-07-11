# SproutWealth
CREATE TABLE cryptocurrency_data (
 timestamp DATETIME,
 open_cny DECIMAL(20, 8),
 high_cny DECIMAL(20, 8),
 low_cny DECIMAL(20, 8),
 close_cny DECIMAL(20, 8),
 open_usd DECIMAL(20, 8),
 high_usd DECIMAL(20, 8),
 low_usd DECIMAL(20, 8),
 close_usd DECIMAL(20, 8),
 volume DECIMAL(20, 8),
 market_cap_usd DECIMAL(20, 8)
);

INSERT INTO cryptocurrency_data (timestamp, open_cny, high_cny, low_cny, close_cny, open_usd, high_usd, low_usd, close_usd, volume, market_cap_usd)
VALUES ('2023-07-11', 219915.186141, 220612.861965, 219777.719128, 220062.704661, 30411.57, 30508.05, 30392.56, 30431.97, 1114.80704, 1114.80704);


