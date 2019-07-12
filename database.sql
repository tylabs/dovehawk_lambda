-- phpMyAdmin SQL Dump
-- version 4.6.5.2
-- https://www.phpmyadmin.net/
--
-- Generation Time: Jul 12, 2019 at 12:58 PM
-- Server version: 5.6.10
-- PHP Version: 5.6.37

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `automata`
--

-- --------------------------------------------------------

--
-- Table structure for table `Auth`
--

CREATE TABLE `Auth` (
  `local_id` int(10) UNSIGNED NOT NULL,
  `authkey` varchar(64) DEFAULT NULL,
  `toolkey` varchar(64) NOT NULL,
  `created` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `misp_id` int(10) UNSIGNED DEFAULT NULL,
  `org_id` int(10) UNSIGNED DEFAULT NULL,
  `email` varchar(127) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `recorder_domain`
--

CREATE TABLE `recorder_domain` (
  `domain_id` int(11) UNSIGNED NOT NULL,
  `name` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `recorder_fetch`
--

CREATE TABLE `recorder_fetch` (
  `fetch_id` int(10) UNSIGNED NOT NULL,
  `submit_ip_id` int(10) UNSIGNED NOT NULL,
  `toolkey_id` int(10) UNSIGNED NOT NULL,
  `reported_on` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `record_type` enum('pdns','flow') NOT NULL,
  `records_added` int(11) NOT NULL DEFAULT '0',
  `node` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- Table structure for table `recorder_flow`
--

CREATE TABLE `recorder_flow` (
  `flow_id` int(10) UNSIGNED NOT NULL,
  `bytes_out` int(11) NOT NULL,
  `ip_id` int(11) NOT NULL,
  `toolkey_id` int(11) NOT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `recorder_ip`
--

CREATE TABLE `recorder_ip` (
  `ip_id` int(11) UNSIGNED NOT NULL,
  `address` char(29) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `recorder_pdns`
--

CREATE TABLE `recorder_pdns` (
  `pdns_id` int(11) UNSIGNED NOT NULL,
  `domain_id` int(11) NOT NULL,
  `ip_id` int(11) NOT NULL,
  `toolkey_id` int(11) NOT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `recorder_pdns_cname`
--

CREATE TABLE `recorder_pdns_cname` (
  `cname_id` int(11) UNSIGNED NOT NULL,
  `domain_id` int(11) NOT NULL,
  `domain2_id` int(11) NOT NULL,
  `toolkey_id` int(11) NOT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `recorder_pdns_seen`
--

CREATE TABLE `recorder_pdns_seen` (
  `seen_id` int(11) UNSIGNED NOT NULL,
  `domain_id` int(11) NOT NULL,
  `toolkey_id` int(11) NOT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Auth`
--
ALTER TABLE `Auth`
  ADD PRIMARY KEY (`local_id`);

--
-- Indexes for table `recorder_domain`
--
ALTER TABLE `recorder_domain`
  ADD PRIMARY KEY (`domain_id`);

--
-- Indexes for table `recorder_fetch`
--
ALTER TABLE `recorder_fetch`
  ADD PRIMARY KEY (`fetch_id`);

--
-- Indexes for table `recorder_flow`
--
ALTER TABLE `recorder_flow`
  ADD PRIMARY KEY (`flow_id`);

--
-- Indexes for table `recorder_ip`
--
ALTER TABLE `recorder_ip`
  ADD PRIMARY KEY (`ip_id`);

--
-- Indexes for table `recorder_pdns`
--
ALTER TABLE `recorder_pdns`
  ADD PRIMARY KEY (`pdns_id`);

--
-- Indexes for table `recorder_pdns_cname`
--
ALTER TABLE `recorder_pdns_cname`
  ADD PRIMARY KEY (`cname_id`);

--
-- Indexes for table `recorder_pdns_seen`
--
ALTER TABLE `recorder_pdns_seen`
  ADD PRIMARY KEY (`seen_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Auth`
--
ALTER TABLE `Auth`
  MODIFY `local_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
--
-- AUTO_INCREMENT for table `recorder_domain`
--
ALTER TABLE `recorder_domain`
  MODIFY `domain_id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
--
-- AUTO_INCREMENT for table `recorder_fetch`
--
ALTER TABLE `recorder_fetch`
  MODIFY `fetch_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
--
-- AUTO_INCREMENT for table `recorder_flow`
--
ALTER TABLE `recorder_flow`
  MODIFY `flow_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
--
-- AUTO_INCREMENT for table `recorder_ip`
--
ALTER TABLE `recorder_ip`
  MODIFY `ip_id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
--
-- AUTO_INCREMENT for table `recorder_pdns`
--
ALTER TABLE `recorder_pdns`
  MODIFY `pdns_id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
--
-- AUTO_INCREMENT for table `recorder_pdns_cname`
--
ALTER TABLE `recorder_pdns_cname`
  MODIFY `cname_id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
--
-- AUTO_INCREMENT for table `recorder_pdns_seen`
--
ALTER TABLE `recorder_pdns_seen`
  MODIFY `seen_id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=760;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
