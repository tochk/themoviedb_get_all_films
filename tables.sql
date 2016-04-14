CREATE TABLE `genres` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `genre_movies_merge` (
  `id` int(11) NOT NULL,
  `genreid` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `genre_series_merge` (
  `id` int(11) NOT NULL,
  `genreid` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `movies` (
  `id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `original_title` varchar(200) NOT NULL,
  `overview` longtext NOT NULL,
  `poster_path` varchar(200) DEFAULT NULL,
  `release_date` varchar(50) NOT NULL,
  `original_language` varchar(10) NOT NULL,
  `popularity` float NOT NULL,
  `vote_count` int(11) NOT NULL,
  `vote_average` float NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


CREATE TABLE `series` (
  `id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `original_title` varchar(200) NOT NULL,
  `overview` longtext NOT NULL,
  `first_air_date` varchar(100) NOT NULL,
  `poster_path` varchar(200) DEFAULT NULL,
  `original_language` varchar(10) NOT NULL,
  `popularity` float NOT NULL,
  `vote_count` int(11) NOT NULL,
  `vote_average` float NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


ALTER TABLE `genres`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `genre_movies_merge`
  ADD PRIMARY KEY (`id`,`genreid`),
  ADD KEY `genre_movies_merge_fk1` (`genreid`);

ALTER TABLE `movies`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `series`
  ADD PRIMARY KEY (`id`);
  
ALTER TABLE `genre_series_merge`
  ADD PRIMARY KEY (`id`,`genreid`),
  ADD KEY `genre_series_merge_fk1` (`genreid`);



