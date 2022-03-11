-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 11, 2022 at 06:23 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `test`
--

-- --------------------------------------------------------

--
-- Table structure for table `vimeo_video_stats`
--

CREATE TABLE `vimeo_video_stats` (
  `id` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `video_id` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `plays` bigint(8) DEFAULT NULL,
  `loads` bigint(8) DEFAULT NULL,
  `downloads` bigint(8) DEFAULT NULL,
  `finishes` bigint(8) DEFAULT NULL,
  `likes` bigint(8) DEFAULT NULL,
  `comments` bigint(8) DEFAULT NULL,
  `unique_loads` bigint(8) DEFAULT NULL,
  `mean_seconds` bigint(8) DEFAULT NULL,
  `mean_percent` bigint(8) DEFAULT NULL,
  `sum_seconds` bigint(8) DEFAULT NULL,
  `unique_viewers` bigint(8) DEFAULT NULL,
  `video_created_at` timestamp(6) NULL DEFAULT NULL,
  `created_at` timestamp(6) NULL DEFAULT NULL,
  `updated_at` timestamp(6) NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Triggers `vimeo_video_stats`
--
DELIMITER $$
CREATE TRIGGER `vimeo_video_stats_create` BEFORE INSERT ON `vimeo_video_stats` FOR EACH ROW SET NEW.created_at = NOW(), NEW.updated_at = NOW()
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `vimeo_video_stats_update` BEFORE UPDATE ON `vimeo_video_stats` FOR EACH ROW SET NEW.updated_at = NOW(), NEW.created_at = OLD.created_at
$$
DELIMITER ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `vimeo_video_stats`
--
ALTER TABLE `vimeo_video_stats`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `vimeo_video_stats`
--
ALTER TABLE `vimeo_video_stats`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;