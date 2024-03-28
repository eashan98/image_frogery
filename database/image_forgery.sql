-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 26, 2024 at 07:26 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `image_forgery`
--

-- --------------------------------------------------------

--
-- Table structure for table `history`
--

CREATE TABLE `history` (
  `id` int(11) NOT NULL,
  `input` varchar(500) NOT NULL,
  `output_type` varchar(10) NOT NULL,
  `output` longtext DEFAULT NULL,
  `action` varchar(50) NOT NULL,
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `history`
--

INSERT INTO `history` (`id`, `input`, `output_type`, `output`, `action`, `timestamp`) VALUES
(1, '20240326103713_2.jpg', 'image', '20240326103713_2.jpg', 'CFA Artifact Detection', '2024-03-25 23:37:46'),
(2, '20240326233602_demo_2.png', 'image', '20240326233602_demo_2.png', 'Copy Move Detection', '2024-03-26 12:36:02'),
(3, '20240326233616_forged2.jpg', 'image', '20240326233616_forged2.jpg', 'Copy Move Detection', '2024-03-26 12:36:16'),
(4, '20240326233622_forged2.jpg', 'image', '20240326233622_forged2.jpg', 'Image Extraction', '2024-03-26 12:36:30'),
(5, '20240326235202_3.jpg', 'image', '20240326235202_3.jpg', 'Error Level Analysis', '2024-03-26 12:52:05');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `history`
--
ALTER TABLE `history`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `history`
--
ALTER TABLE `history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
