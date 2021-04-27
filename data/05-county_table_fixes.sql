-- Alabama, Georgia, Indiana, Missouri all have a 'DeKalb' county which needs correcting
UPDATE county SET name = 'DeKalb' WHERE name = 'De Kalb';
-- In Illinois, 'LaSalle County' has no space (unlike Texas and Louisiana)
UPDATE county SET name = 'LaSalle' WHERE name = 'La Salle' AND id = 634;
-- In Florida, 'DeSoto County' has no space (unlike Louisiana)
UPDATE county SET name = 'DeSoto' WHERE name = 'De Soto' AND id = 325;
-- In Indiana, 'LaPorte County' has no space
UPDATE county SET name = 'LaPorte' WHERE name = 'La Porte' AND id = 730;
-- In Nevada, 'Carson City' has typo, 'Carson City city'
UPDATE county SET name = 'Carson City' WHERE name = 'Carson City city' AND id = 1709;
-- In Texas, 'DeWitt County' has no space
UPDATE county SET name = 'DeWitt' WHERE name = 'De Witt' AND id = 2524;
-- Fix other city problems to avoid confusion
UPDATE county SET name = 'Baltimore City' WHERE name = 'Baltimore city' AND id = 1176;
UPDATE county SET name = 'St. Louis City' WHERE name = 'St. Louis city' AND id = 1562;
-- Virginia is odd
UPDATE county SET name = 'Alexandria City' WHERE name = 'Alexandria' AND id = 2763;
-- There is a Bedford County
-- UPDATE county SET name = 'Bedford City' WHERE name = 'Bedford' AND id = 2771;
UPDATE county SET name = 'Bristol City' WHERE name = 'Bristol' AND id = 2774;
UPDATE county SET name = 'Buena Vista City' WHERE name = 'Buena Vista' AND id = 2778;
UPDATE county SET name = 'Charlottesville City' WHERE name = 'Charlottesville' AND id = 2784;
UPDATE county SET name = 'Chesapeake City' WHERE name = 'Chesapeake' AND id = 2785;
UPDATE county SET name = 'Colonial Heights City' WHERE name = 'Colonial Heights' AND id = 2789;
UPDATE county SET name = 'Covington City' WHERE name = 'Covington' AND id = 2790;
UPDATE county SET name = 'Danville City' WHERE name = 'Danville' AND id = 2794;
UPDATE county SET name = 'Emporia City' WHERE name = 'Emporia' AND id = 2797;
-- There is a Fairfax County
-- UPDATE county SET name = 'Fairfax City' WHERE name = 'Fairfax' AND id = 2799;
UPDATE county SET name = 'Falls Church City' WHERE name = 'Falls Church' AND id = 2800;
-- There is a Franklin County
-- UPDATE county SET name = 'Franklin City' WHERE name = 'Franklin' AND id = 2804;
UPDATE county SET name = 'Fredericksburg City' WHERE name = 'Fredericksburg' AND id = 2806;
UPDATE county SET name = 'Galax City' WHERE name = 'Galax' AND id = 2807;
UPDATE county SET name = 'Hampton City' WHERE name = 'Hampton' AND id = 2815;
UPDATE county SET name = 'Harrisonburg City' WHERE name = 'Harrisonburg' AND id = 2817;
UPDATE county SET name = 'Hopewell City' WHERE name = 'Hopewell' AND id = 2821;
UPDATE county SET name = 'Lexington City' WHERE name = 'Lexington' AND id = 2829;
UPDATE county SET name = 'Lynchburg City' WHERE name = 'Lynchburg' AND id = 2833;
UPDATE county SET name = 'Manassas City' WHERE name = 'Manassas' AND id = 2836;
UPDATE county SET name = 'Manassas Park City' WHERE name = 'Manassas Park' AND id = 2835;
UPDATE county SET name = 'Martinsville City' WHERE name = 'Martinsville' AND id = 2837;
UPDATE county SET name = 'Newport News City' WHERE name = 'Newport News' AND id = 2844;
UPDATE county SET name = 'Norfolk City' WHERE name = 'Norfolk' AND id = 2845;
UPDATE county SET name = 'Norton City' WHERE name = 'Norton' AND id = 2848;
UPDATE county SET name = 'Petersburg City' WHERE name = 'Petersburg' AND id = 2853;
UPDATE county SET name = 'Poquoson City' WHERE name = 'Poquoson' AND id = 2855;
UPDATE county SET name = 'Portsmouth City' WHERE name = 'Portsmouth' AND id = 2856;
UPDATE county SET name = 'Radford City' WHERE name = 'Radford' AND id = 2862;
-- There is a Richmond County
-- UPDATE county SET name = 'Richmond City' WHERE name = 'Richmond' AND id = 2864;
-- There is a Roanoke County
-- UPDATE county SET name = 'Roanoke City' WHERE name = 'Roanoke' AND id = 2865;
UPDATE county SET name = 'Salem City' WHERE name = 'Salem' AND id = 2869;
UPDATE county SET name = 'Staunton City' WHERE name = 'Staunton' AND id = 2876;
UPDATE county SET name = 'Suffolk City' WHERE name = 'Suffolk' AND id = 2877;
UPDATE county SET name = 'Virginia Beach City' WHERE name = 'Virginia Beach' AND id = 2881;
UPDATE county SET name = 'Waynesboro City' WHERE name = 'Waynesboro' AND id = 2884;
UPDATE county SET name = 'Williamsburg City' WHERE name = 'Williamsburg' AND id = 2886;
UPDATE county SET name = 'Winchester City' WHERE name = 'Winchester' AND id = 2887;

COMMIT;
