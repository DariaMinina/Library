SELECT Genre,COUNT(*)
FROM book
WHERE Genre = '$genre'
GROUP BY Genre