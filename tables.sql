CREATE TABLE `films` (
  `id` int(11) NOT NULL,
  `original_title` varchar(100) DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `overview` text,
  `video` text,
  `backdrop_path` text,
  `poster_path` text,
  `release_date` text,
  `original_language` varchar(10) DEFAULT NULL,
  `adult` varchar(10) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;



CREATE TABLE `tv` (
  `id` int(11) NOT NULL,
  `original_name` varchar(200) NOT NULL,
  `name` varchar(200) NOT NULL,
  `overview` text NOT NULL,
  `first_air_date` text NOT NULL,
  `backdrop_path` text,
  `poster_path` text,
  `original_language` varchar(100) NOT NULL,
  `origin_country` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


ALTER TABLE `films`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `tv`
  ADD PRIMARY KEY (`id`);

