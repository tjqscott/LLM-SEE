-- Output exhaustive list of story style issues using resolution time
SELECT 
    COALESCE(Project_ID, 0), 
    COALESCE(Issue_Key, 'N/A'), 
    COALESCE(Title, 'No Title'), 
    COALESCE(Description, 'No Description'), 
    COALESCE(Resolution_Time_Minutes, 0)
FROM Issue 
WHERE Type = 'Story'
  AND (Description LIKE 'As a%' OR Description LIKE '"As a%')
  AND Description NOT LIKE '%http%'
  AND Resolution_Time_Minutes > 0
ORDER BY Creation_Date ASC
INTO OUTFILE 'C:/Users/tjqsc/Desktop/resolution_time.csv'
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
ESCAPED BY '"'
LINES TERMINATED BY '\n';
