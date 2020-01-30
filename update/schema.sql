-- phpMyAdmin SQL Dump
-- version 3.2.0.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Aug 10, 2013 at 03:33 PM
-- Server version: 5.1.50
-- PHP Version: 5.3.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Database: `abqride_8_10_13`
--

-- --------------------------------------------------------

--
-- Table structure for table `calendar`
--

CREATE TABLE IF NOT EXISTS `calendar` (
  `service_id` varchar(255) NOT NULL,
  `monday` int(11) NOT NULL,
  `tuesday` int(11) NOT NULL,
  `wednesday` int(11) NOT NULL,
  `thursday` int(11) NOT NULL,
  `friday` int(11) NOT NULL,
  `saturday` int(11) NOT NULL,
  `sunday` int(11) NOT NULL,
  `start_date` varchar(255) NOT NULL,
  `end_date` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `routes`
--

CREATE TABLE IF NOT EXISTS `routes` (
  `route_id` int(40) NOT NULL,
  `agency_id` int(11) NOT NULL,
  `route_short_name` varchar(255) NOT NULL,
  `route_long_name` varchar(255) NOT NULL,
  `route_desc` varchar(255) NOT NULL,
  `route_type` int(11) NOT NULL,
  `route_url` text NOT NULL,
  `route_color` text NOT NULL,
  `route_text_color` text NOT NULL,
  PRIMARY KEY (`route_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `route_stop_map`
--

CREATE TABLE IF NOT EXISTS `route_stop_map` (
  `route` smallint(6) NOT NULL,
  `stop` int(9) NOT NULL,
  `stop_code` int(9) NOT NULL,
  KEY `route` (`route`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `shapes`
--

CREATE TABLE IF NOT EXISTS `shapes` (
  `shape_id` smallint(4) unsigned NOT NULL,
  `shape_pt_lat` decimal(8,6) NOT NULL,
  `shape_pt_lon` decimal(9,6) NOT NULL,
  `shape_pt_sequence` smallint(3) unsigned NOT NULL,
  `shape_dist_traveled` decimal(6,4) NOT NULL,
  KEY `shape_id_2` (`shape_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `stops`
--

CREATE TABLE IF NOT EXISTS `stops` (
  `stop_id` int(11) NOT NULL,
  `stop_code` int(11) NOT NULL,
  `stop_name` text NOT NULL,
  `stop_desc` text NOT NULL,
  `stop_lat` double NOT NULL,
  `stop_lon` double NOT NULL,
  `zone_id` text NOT NULL,
  `stop_url` text NOT NULL,
  `parent_station` text NOT NULL,
  `location_type` int(11) NOT NULL,
  PRIMARY KEY (`stop_id`),
  KEY `stop_code` (`stop_code`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `stops_local`
--

CREATE TABLE IF NOT EXISTS `stops_local` (
  `stop_lat` double NOT NULL,
  `stop_code` int(11) NOT NULL,
  `stop_lon` double NOT NULL,
  `stop_id` int(11) NOT NULL,
  `stop_name` text NOT NULL,
  `direction` varchar(1) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `times`
--

CREATE TABLE IF NOT EXISTS `times` (
  `trip_id` mediumint(6) unsigned NOT NULL,
  `arrival_time` char(8) NOT NULL,
  `departure_time` char(8) NOT NULL,
  `stop_id` int(9) unsigned NOT NULL,
  `stop_sequence` tinyint(2) unsigned NOT NULL,
  `stop_headsign` varchar(1) NOT NULL,
  `pickup_type` varchar(1) NOT NULL,
  `drop_off_type` varchar(1) NOT NULL,
  `shape_dist_traveled` float NOT NULL,
  `timepoint` varchar(10) NOT NULL,
  KEY `trip_id` (`trip_id`),
  KEY `arrival_time` (`arrival_time`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `times_simple`
--

CREATE TABLE IF NOT EXISTS `times_simple` (
  `arrival_time` char(8) NOT NULL,
  `stop_id` int(9) unsigned NOT NULL,
  `active_wkd` tinyint(1) NOT NULL,
  `active_sat` tinyint(1) NOT NULL,
  `active_sun` tinyint(1) NOT NULL,
  `route` int(4) unsigned NOT NULL,
  KEY `stop_id` (`stop_id`),
  KEY `arrival_time` (`arrival_time`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `trips`
--

CREATE TABLE IF NOT EXISTS `trips` (
  `route_id` smallint(5) unsigned NOT NULL,
  `service_id` varchar(255) NOT NULL,
  `trip_id` mediumint(6) unsigned NOT NULL,
  `trip_headsign` varchar(255) NOT NULL,
  `direction_id` tinyint(1) NOT NULL,
  `block_id` smallint(5) unsigned NOT NULL,
  `shape_id` mediumint(6) unsigned NOT NULL,
  KEY `trip_id` (`trip_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `trip_map`
--

CREATE TABLE IF NOT EXISTS `trip_map` (
  `trip_id` int(40) NOT NULL,
  `arrival_time` varchar(255) NOT NULL,
  `stop_id` int(40) NOT NULL,
  `stop_code` int(11) NOT NULL,
  `stop_sequence` int(40) NOT NULL,
  `shape_dist_traveled` float NOT NULL,
  `active_wkd` tinyint(1) NOT NULL,
  `active_sat` tinyint(1) NOT NULL,
  `active_sun` tinyint(1) NOT NULL,
  `route` smallint(5) NOT NULL,
  KEY `trip_id` (`trip_id`),
  KEY `stop_id` (`stop_id`),
  KEY `stop_code` (`stop_code`),
  KEY `arrival_time` (`arrival_time`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

