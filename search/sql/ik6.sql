SELECT `book`.`Name`, `price_list`.`price`, `Publishing_office`.`PO_title`
FROM `Publishing_office` JOIN `price_list` USING (PO_id) JOIN `book` USING(idbook)
WHERE `book`.`Name` = '$name1'
ORDER BY price ASC
LIMIT 1