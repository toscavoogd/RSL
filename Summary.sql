/*Create a table with all the variables of the csv file moviesfrommetacritics*/
CREATE TABLE movies ( url text, title text, ReleaseDate text, Distributor text, Starring text, Summary text, Director text, Genre text, Rating text, Runtime text, Userscore text, Metascore text, scoreCounts text );

/* Copy the table into the csv file*/
\copy movies FROM '/home/pi/RSL/moviesFromMetacritic (1).csv' delimiter ';' csv header;

/*Check if my favorite movie (mean girls) is in the dataset*/
SELECT url FROM movies WHERE url LIKE '%mean%';
SELECT * FROM movies where url='mean-girls'; 

/*Add the lexemes starring vector, in order to create the top 50*/
ALTER TABLE movies ADD lexemesSummary tsvector;
UPDATE movies SET lexemesSummary = to_tsvector(Summary);

/*Choosing school, because the movie takes place at school*/
SELECT url FROM movies WHERE lexemesSummary @@ to_tsquery('school');
ALTER TABLE movies ADD rank float4;
UPDATE movies SET rank = ts_rank(lexemesSummary,plainto_tsquery((SELECT Summary FROM movies WHERE url='mean-girls')));

/*Create a top 50 recommendation movies based on the starring field (Jonathan)
The treshold is set at 0.01, to be able to create a top 50*/
CREATE TABLE recommendationsBasedOnSummaryField AS SELECT url, rank FROM movies WHERE rank > 0.01 ORDER BY rank DESC LIMIT 50;

/*Copy the table to a csv file*/
\copy (SELECT * FROM recommendationsBasedOnSummaryField) to '/home/pi/RSL/top50recommendationssummary.csv' WITH csv;
