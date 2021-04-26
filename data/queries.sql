-- Duplicate addresses
SELECT COUNT(id)
     , address_formatted 
     , city_id
  FROM address
 GROUP BY address_formatted, city_id 
HAVING COUNT(id) > 1
;

-- Duplicate addresses with missing zip_code_ext
SELECT ad1.id 
  FROM address ad1 
 WHERE LENGTH(ad1.zip_code_ext) = 0
   AND EXISTS (
   SELECT 1
     FROM address ad2
    WHERE LENGTH(ad2.zip_code_ext) = 4
      AND ad1.city_id           =  ad2.city_id
      AND ad1.street_number     =  ad2.street_number 
      AND ad1.street            =  ad2.street 
      AND ad1.suffix            =  ad2.suffix
      AND ad1.address_formatted =  ad2.address_formatted 
 ) ;

-- Duplicate addresses with superflous suffix
SELECT ad1.id
  FROM address ad1
     , address ad2
 WHERE ad1.suffix               <> ''
   AND LENGTH(ad2.suffix)       = ''
   AND ad1.city_id              = ad2.city_id
   AND ad1.address_formatted    = ad2.address_formatted
   AND ad1.zip_code             = ad2.zip_code
;

SELECT COUNT(id)
     , GROUP_CONCAT(id SEPARATOR ', ') 
     , address_formatted
--     , zip_code 
     , city_id
  FROM address
 WHERE address_formatted NOT LIKE 'PO Box%'
 GROUP BY address_formatted
--        , zip_code
        , city_id
HAVING COUNT(id) > 1
;

SELECT * FROM address WHERE address_formatted IN (SELECT address_formatted FROM address WHERE id = 326);

SELECT ad.*
     , ct.name 
  FROM 	address ad
     , city ct
 WHERE ad.city_id = ct.id 
   AND ad.address_formatted LIKE '765 Westminster St' 
   AND ct.id = 42
ORDER BY ad.address_formatted ;


UPDATE address SET address_formatted = '27 Sims Ave, Unit 104' WHERE id = 324;
DELETE FROM address WHERE id IN (28542);

