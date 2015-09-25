-- Available events and their frequency in the data

SELECT count(1) AS frequency,
       TYPE
FROM github
GROUP BY TYPE
ORDER BY frequency DESC;
