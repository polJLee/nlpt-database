--FUNCTIONS / VIEWS--
create or replace view most_frequent(title)
as
SELECT Songs.title, Artists.name, count(songid) as num 
FROM Sunday_songs, Songs, Artists 
WHERE Sunday_songs.songid = Songs.id 
AND Artists.id = Songs.artistid
GROUP BY Songs.title, Artists.name 
HAVING count(songid) = (SELECT count(*) 
						FROM Sunday_songs 
						GROUP BY songid 
						ORDER BY count(*) 
						DESC LIMIT 1) 
ORDER BY title ASC;

create or replace view least_frequent(title)
as
SELECT Songs.title, Artists.name, count(songid) as num 
FROM Sunday_songs, Songs, Artists
WHERE Sunday_songs.songid = songs.id 
AND Artists.id = Songs.artistid
GROUP BY Songs.title, Artists.name 
HAVING count(songid) = (SELECT count(*) 
						FROM Sunday_songs 
						GROUP BY songid 
						ORDER BY count(*) 
						ASC LIMIT 1) 
ORDER BY title ASC;


create or replace view phil_wickham(title)
as
SELECT title
FROM Songs
WHERE ArtistID = 'PW';

create or replace view cityalight(title)
as
SELECT title
FROM Songs
WHERE ArtistID = 'CA';

create or replace view hillsong(title)
as
SELECT title
FROM Songs
WHERE ArtistID = 'H';

create or replace view elevation_worship(title)
as
SELECT title
FROM Songs
WHERE ArtistID = 'EW';

create or replace view shane_shane(title)
as
SELECT title
FROM Songs
WHERE ArtistID = 'SS';

create or replace view passion(title)
as
SELECT title
FROM Songs
WHERE ArtistID = 'P';

create or replace view worship_initiative(title)
as
SELECT title
FROM Songs
WHERE ArtistID = 'WI';

create or replace view starfield(title)
as
SELECT title
FROM Songs
WHERE ArtistID = 'SF';

create or replace view vertical_worship(title)
as
SELECT title
FROM Songs
WHERE ArtistID = 'VW';


--TABLES--
CREATE TABLE Sundays (
	ID int,
	Date character(8),
	Title TEXT,
	Passage character(50)
);


CREATE TABLE Songs (
	ID int,
	Title character(50),
	ArtistID character(4)
);


CREATE TABLE Sunday_Songs(
	songID int,
	sundayID int
);

CREATE TABLE Artists (
	ID character(4),
	Name character(30)
);

CREATE TABLE Members (
	ID int,
	Name character(30),
	Role character(30)
);

CREATE TABLE Roster(
	ID int,
	Month character(9),
	Song_Leader1 character(15),
	Song_Leader2 character(15),
	Vocal character(15),
	Guitar_1 character(15),
	Guitar_2 character(15),
	Keys character(15),
	Drum character(15),
	Pads character(15)
);

-- loading roster.csv into roster table -- 
	-- \COPY roster FROM /Users/paullee/Desktop/roster.csv HEADER CSV

--BASE SONGS--
-- INSERT INTO Sundays (ID, Date, Title, Passage)
-- VALUES (, '.0.22', '', '');



--JANUARY--
INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (1, '02.01.22', 'Eyes to See', 'Matthew 13:1-17');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (2, '09.01.22', 'The Gospe of Grace', 'Galatians 4:4-5');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (3, '16.01.22', 'Renewal of Culture, Culture of Renewal', 'Acts 2');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (4, '23.01.22', 'A Prayer for Discipleship', '1 Thessalonians 5:11');


--FEBRUARY--
INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (5, '30.01.22', 'The Phillippian Jailer Converted', 'Acts 16:25-34');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (6, '06.02.22', 'A Vision for Church Planting', 'Matthew 13:1-9');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (7, '13.02.22', 'Kairos: A Sense of God''s Timing', 'Matthew 13:24-30; Galatians 6:10');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (8, '20.02.22', 'The King of Glory', 'Psalm 24');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (9, '27.02.22', 'The Time for Discipleship is Now', '1 Thessalonians 5:1-22');


--MARCH--
INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (10, '06.03.22', 'Begin Investing into Families Today', 'Psalm 127');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (11, '13.03.22', 'We''ll Get There When We Get There: Cultivating Love for the City', 'Jonah 3');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (12, '20.03.22', 'It was the Worst of Times', 'Ruth 1:1-5');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (13, '27.03.22', 'A History of Bitterness', 'Ruth 1:6-22');


--APRIL--
INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (14, '03.04.22', 'The House of Bread Has Bread Again', 'Ruth 2:1-3');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (15, '10.04.22', 'Time Keeps on Ticking', 'Ruth 2:4-23');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (16, '15.04.22', 'Solace in Your Suffering', 'Luke 22:39-46');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (17, '17.04.22', 'Building Faith With the Breaking of Bread', 'Luke 24:13-35');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (18, '24.04.22', 'A Good () is Hard to Find', 'Ruth 3:1-15');

--MAY--
INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (19, '01.05.22', 'Love and Marriage', 'Ruth 3:16-18');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (20, '08.05.22', 'Mr. What''s-His-Name', 'Ruth 4:1-12');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (21, '15.05.22', 'Outside In', 'Ruth 4:13-22');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (22, '22.05.22', 'Compassion Sunday', '');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (23, '29.05.22', 'You Should Read teh Old Testament!', 'Colossians 2:11-12');


--JUNE--
INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (24, '05.06.22', 'Seeing is Believing', 'Romans 6:4-6');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (25, '12.06.22', 'Through the Waters', 'Matthew 28:19-20');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (26, '19.06.22', 'Fingers Crossed', 'Romans 4:9-12; Colossians 2:11-15');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (27, '26.06.22', 'Need Each Other', 'Matthew 3:13-17');


--JULY--
INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (28, '03.07.22', 'Water the Seed', 'Deuteronomy 11:18-21');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (29, '10.07.22', 'Keep Your Words', 'Acts 22:6-21');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (30, '17.07.22', 'Wintercon Sunday Service - James Fong', '');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (31, '24.07.22', 'The Church and God''s Multifaceted Wisdom', 'Ephisians 3:1-13');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (32, '31.07.22', 'It''s a Camp Thing', 'Acts 2');

--AUGUST--
INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (33, '07.08.22', 'You Only Break Bread with Those at Your Table', 'Hebrews 10:19-25');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (34, '14.08.22', 'Letters from the Past', '1 Corinthians 1:1-9');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (35, '21.08.22', 'Sibling Rivalry', '1 Corinthians 1:10-17');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (36, '28.08.22', '', '');	--PRAISE TEAM ROAD TRIP--

--SEPTEMBER--
INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (37, '04.09.22', 'Foolish Wisdom', '1 Corinthians 2:6-3:4');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (38, '11.09.22', 'God''s Garden Temple', '1 Corinthians 3:5-23');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (39, '18.09.22', 'Ministers and Minstrels', '1 Corinthians 4:1-17');

INSERT INTO Sundays (ID, Date, Title, Passage)
VALUES (40, '25.09.22', 'Follow', 'Colossians 3:5-12');







--BASE ARTISTS--
-- INSERT INTO Artists (ID, Name)
-- VALUES ('','');


INSERT INTO Artists (ID, Name)
VALUES ('PW','Phil Wickham');

INSERT INTO Artists (ID, Name)
VALUES ('CA','CityAlight');

INSERT INTO Artists (ID, Name)
VALUES ('AtH','Ascend the Hills');

INSERT INTO Artists (ID, Name)
VALUES ('H','Hillsong');

INSERT INTO Artists (ID, Name)
VALUES ('EW','Elevation Worship');

INSERT INTO Artists (ID, Name)
VALUES ('SS','Shane & Shane');

INSERT INTO Artists (ID, Name)
VALUES ('VW','Vertical Worship');

INSERT INTO Artists (ID, Name)
VALUES ('P','Passion');

INSERT INTO Artists (ID, Name)
VALUES ('PB','Pat Barrett');

INSERT INTO Artists (ID, Name)
VALUES ('CC','Cody Carnes');

INSERT INTO Artists (ID, Name)
VALUES ('CT','Chris Tomlin');

INSERT INTO Artists (ID, Name)
VALUES ('KK','Kings Kaleidoscope');

INSERT INTO Artists (ID, Name)
VALUES ('PS','Planetshakers');

INSERT INTO Artists (ID, Name)
VALUES ('KKG','Keith and Kristyn Getty');

INSERT INTO Artists (ID, Name)
VALUES ('WI','The Worship Initiative');

INSERT INTO Artists (ID, Name)
VALUES ('SF','Starfield');

INSERT INTO Artists (ID, Name)
VALUES ('ASW','Austin Stone Worship');

INSERT INTO Artists (ID, Name)
VALUES ('CW','Citipointe Worship');

INSERT INTO Artists (ID, Name)
VALUES ('SGM','Soveriegn Grace Music');

--BASE SONGS--
INSERT INTO Songs (ID, Title, ArtistID)
VALUES (, '', '');


INSERT INTO Songs (ID, Title, ArtistID)
VALUES (1, 'This is Amazing Grace', 'PW');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (2, 'Anthem', 'PW');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (3, 'Living Hope', 'PW');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (4, 'I Want to Know You', 'CA');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (5, 'Ancient of Days', 'CA');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (6, 'The Love of the Father', 'CA');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (7, 'Yet Not I But Through Christ in Me', 'CA');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (8, 'Christ is Mine Forevermore', 'CA');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (9, 'Once for All', 'CA');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (10, 'Your Will Be Done', 'CA');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (11, 'Pride of a Father', 'CA');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (12, 'Blessed Assurance', 'CA');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (13, 'Be Thou My Vision', 'AtH');


INSERT INTO Songs (ID, Title, ArtistID)
VALUES (14, 'The Passion', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (15, 'Scandal of Grace', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (16, 'What a Beautiful Name it is', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (17, 'Another in the Fire', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (18, 'Cornerstone', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (19, 'It is Well with My Soul', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (20, 'This I Believe (The Creed)', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (21, 'Stronger', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (22, 'Who You Say I Am', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (23, 'Anchor', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (24, 'Saviour King', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (25, 'Man of Sorrows', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (26, 'There is a King', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (27, 'King of Kings', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (28, 'God is Able', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (29, 'Crowns', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (30, 'Hosanna', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (31, 'Resurrender', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (32, 'O Praise the Name (Anástasis)', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (33, 'Broken Vessels', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (34, 'Beneath the Waters', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (35, 'Let it Be Jesus', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (36, 'Christ is Enough', 'H');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (37, 'Grace So Glorious', 'EW');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (38, 'Never Lost', 'EW');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (39, 'Graves into Gardens', 'EW');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (40, 'Hallelujah Here Below', 'EW');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (41, 'Give us Clean Hands', 'SS');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (42, 'Come Thou Fount (Above All Else)', 'SS');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (43, 'The Lord is My Salvation', 'SS');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (44, 'This We Know', 'SS');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (45, 'Trust You', 'SS');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (46, 'All the Poor and Powerless', 'SS');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (47, 'Let it Be Jesus', 'SS');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (48, 'Oceans', 'SS');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (49, 'In Christ Alone', 'SS');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (50, 'My Worth is Not in What I Own', 'SS');



INSERT INTO Songs (ID, Title, ArtistID)
VALUES (51, 'The Lamb of God', 'VW');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (52, 'Strong God', 'VW');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (53, 'In Christ Alone', 'P');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (54, 'Lord I Need You', 'P');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (55, 'Way Maker', 'P');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (56, 'More Like Jesus', 'P');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (57, 'Behold the Lamb', 'P');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (58, 'Build My Life', 'PB');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (59, 'Run to the Father', 'CC');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (60, 'Good Good Father', 'CT');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (61, 'All Glory Be to Christ', 'KK');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (62, 'Beautiful Saviour', 'PS');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (63, 'The Power of the Cross', 'KKG');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (64, 'Trust You', 'WI');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (65, 'All the Poor and Powerless', 'WI');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (66, 'Reign in Us', 'SF');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (67, 'Unashamed', 'SF');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (68, 'How Deep the Father''s Love for Us', 'ASW');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (69, 'Presence Power Glory', 'CW');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (70, 'Jesus, Thank You', 'SGM');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (71, 'Draw Me Close', 'SS');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (72, 'I Give You My Heart', 'SS');

INSERT INTO Songs (ID, Title, ArtistID)
VALUES (73, 'From the Inside Out', 'H');



--BASE SUNDAY_SONGS--
-- INSERT INTO Sunday_Songs (songID, SundayID)
-- VALUES (, );


INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (1, 1);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (2, 4);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (3, 33);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (4, 1);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (4, 31);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (4, 37);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (5, 2);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (6, 4);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (6, 27);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (6, 30);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (7, 8);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (7, 19);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (7, 29);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (7, 33);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (8, 11);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (9, 16);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (10, 20);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (10, 28);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (11, 27);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (11, 30);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (12, 28);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (12, 31);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (13, 1);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (13, 6);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (14, 2);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (14, 17);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (15, 3);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (15, 19);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (16, 5);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (17, 5);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (18, 6);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (18, 38);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (19, 7);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (20, 8);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (20, 9);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (20, 24);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (20, 27);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (21, 10);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (22, 13);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (22, 15);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (23, 15);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (23, 31);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (24, 16);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (24, 34);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (25, 16);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (26, 17);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (27, 12);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (27, 17);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (27, 22);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (28, 21);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (29, 22);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (30, 23);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (31, 23);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (31, 24);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (31, 34);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (31, 38);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (32, 26);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (32, 39);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (33, 29);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (34, 32);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (35, 35);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (36, 35);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (37, 2);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (37, 13);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (38, 9);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (39, 14);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (40, 39);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (41, 3);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (42, 3);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (43, 5);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (43, 12);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (43, 25);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (43, 32);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (44, 7);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (45, 7);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (46, 11);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (46, 12);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (47, 13);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (48, 14);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (48, 21);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (49, 21);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (50, 22);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (50, 35);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (51 , 4);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (51, 24);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (52, 37);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (53, 6);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (54, 14);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (55, 18);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (56, 18);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (56, 19);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (57, 25);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (58, 8);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (58, 26);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (58, 38);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (59, );

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (59, 9);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (59, 28);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (59, 30);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (60, 10);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (61, 10);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (62, 11);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (62, 15);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (62, 37);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (63, 17);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (64, 18);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (64, 20);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (64, 39);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (65, 32);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (66, 20);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (67, 33);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (68, 23);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (69, 25);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (69, 26);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (69, 29);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (70, 34);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (71, 40);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (72, 40);

INSERT INTO Sunday_Songs (songID, SundayID)
VALUES (73, 40);

-- BASE MEMBERS --
-- INSERT INTO Members (ID, Name, Role)
-- VALUES (, '', '');



INSERT INTO Members (ID, Name, Role)
VALUES (1, 'Calvin', 'Drum');

INSERT INTO Members (ID, Name, Role)
VALUES (2, 'David', 'Vocal + Guitar');

INSERT INTO Members (ID, Name, Role)
VALUES (3, 'Emily', 'Keys');

INSERT INTO Members (ID, Name, Role)
VALUES (4, 'Jackie', 'Vocal');

INSERT INTO Members (ID, Name, Role)
VALUES (5, 'Jake', 'Keys');

INSERT INTO Members (ID, Name, Role)
VALUES (6, 'Minhee', 'Vocal + Keys');

INSERT INTO Members (ID, Name, Role)
VALUES (7, 'Paul', 'Vocal + Guitar');

INSERT INTO Members (ID, Name, Role)
VALUES (8, 'Stella C', 'Vocal + Guitar');

INSERT INTO Members (ID, Name, Role)
VALUES (9, 'Stella K', 'Keys');

INSERT INTO Members (ID, Name, Role)
VALUES (10, 'Una', 'Vocal');

INSERT INTO MEMBERS (ID, Name, Role)
VALUES (11, 'Salang', 'Vocal + Guitar');

INSERT INTO MEMBERS (ID, Name, Role)
VALUES (12, 'Josh', 'Vocal + Guitar');


