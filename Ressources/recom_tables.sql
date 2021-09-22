CREATE DATABASE  IF NOT EXISTS `recom` /*!40100 DEFAULT CHARACTER SET utf8mb4 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `recom`;

-- ----------------------------
-- Table structure for rating
-- ----------------------------
CREATE TABLE IF NOT EXISTS `ratings` (
  `rating_id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `book_id` bigint NOT NULL,
  `rating` smallint NOT NULL,
  KEY `ID` (`rating_id`)
);

-- ----------------------------
-- Table structure for toread
-- ----------------------------
CREATE TABLE IF NOT EXISTS `toread` (
  `toread_id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `book_id` bigint NOT NULL,
  KEY `ID` (`toread_id`)
);

-- ----------------------------
-- Table structure for books
-- ----------------------------
CREATE TABLE IF NOT EXISTS `books` (
  `books_id` bigint NOT NULL AUTO_INCREMENT,
  `book_id` bigint NOT NULL,
  `goodreads_book_id` bigint NOT NULL,
  `best_book_id` bigint DEFAULT NULL,
  `work_id` bigint DEFAULT NULL,
  `books_count` bigint DEFAULT NULL,
  `isbn` varchar(10) DEFAULT NULL,
  `isbn13` varchar(13) NOT NULL,
  `authors` varchar(750) NOT NULL, -- 300
  `original_publication_year` int DEFAULT NULL,
  `original_title` varchar(200) DEFAULT NULL,
  `title` varchar(200) NOT NULL,
  `language_code` varchar(10) DEFAULT NULL,
  `average_rating` float4 NOT NULL,
  `ratings_count` bigint NOT NULL,
  `work_ratings_count` bigint DEFAULT NULL,
  `work_text_reviews_count` bigint DEFAULT NULL,
  `ratings_1` bigint DEFAULT NULL,
  `ratings_2` bigint DEFAULT NULL,
  `ratings_3` bigint NOT NULL,
  `ratings_4` bigint NOT NULL,
  `ratings_5` bigint NOT NULL,
  `image_url` varchar(150) NOT NULL,
  `small_image_url` varchar(150) NOT NULL,
  `author` varchar(50) DEFAULT NULL,
  KEY `ID` (`books_id`)
);

-- ----------------------------
-- Table structure for booktags
-- ----------------------------
CREATE TABLE IF NOT EXISTS `booktags` (
  `booktags_id` bigint NOT NULL AUTO_INCREMENT,
  `goodreads_book_id` bigint NOT NULL,
  `tag_id` bigint NOT NULL,
  `count` bigint NOT NULL,
  KEY `ID` (`booktags_id`)
);

-- ----------------------------
-- Table structure for tags
-- ----------------------------
CREATE TABLE IF NOT EXISTS `tags` (
  `tags_id` bigint NOT NULL AUTO_INCREMENT,
  `tag_id` bigint NOT NULL,
  `tag_name` varchar(50) NOT NULL,
  KEY `ID` (`tags_id`)
);


-- END
