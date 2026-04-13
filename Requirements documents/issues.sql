-- Output exhaustive list of story style issues using total effort
SELECT 
    COALESCE(Project_ID, 0), 
    COALESCE(Issue_Key, 'N/A'), 
    COALESCE(Title, 'No Title'), 
    COALESCE(Description, 'No Description'), 
    COALESCE(Total_Effort_Minutes, 0)
FROM Issue 
WHERE Type = 'Story'
  AND (Description LIKE 'As a%' OR Description LIKE '"As a%')
  AND Description NOT LIKE '%http%'
  AND Total_Effort_Minutes > 0
ORDER BY Creation_Date ASC
INTO OUTFILE 'C:/Users/tjqsc/Desktop/total_effort.csv'
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
ESCAPED BY '"'
LINES TERMINATED BY '\n';