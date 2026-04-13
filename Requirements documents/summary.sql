-- Generate summary of each project in the dataset
SELECT
    Project_Name,
    Project_Description,
    Issue_Key,
    Issue_Title,
    Creation_Date

FROM (
    SELECT
        p.Name AS Project_Name,
        p.Description AS Project_Description,
        i.Issue_Key,
        COALESCE(i.Title, 'No Title') AS Issue_Title,
        DATE_FORMAT(i.Creation_Date, '%Y-%m-%d') AS Creation_Date,
        ROW_NUMBER() OVER (PARTITION BY p.ID ORDER BY i.Creation_Date ASC) AS rn
    FROM project p
    JOIN issue i ON p.ID = i.Project_ID
) ranked
WHERE rn <= 50
ORDER BY Project_Name, Creation_Date ASC
INTO OUTFILE 'C:/Users/tjqsc/Desktop/out.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';