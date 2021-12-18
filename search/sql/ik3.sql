SELECT City,COUNT(*)
FROM Publishing_office
WHERE City = '$city'
GROUP BY City