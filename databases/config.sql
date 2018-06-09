/*
Navicat MySQL Data Transfer

Source Server         : *
Source Server Version : 50640
Source Host           : *
Source Database       : config

Target Server Type    : MYSQL
Target Server Version : 50640
File Encoding         : 65001

Date: 2018-06-09 16:48:32
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for config_routing_table
-- ----------------------------
DROP TABLE IF EXISTS `config_routing_table`;
CREATE TABLE `config_routing_table` (
  `id` int(11) NOT NULL DEFAULT '0',
  `ip` varchar(15) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for config_svr
-- ----------------------------
DROP TABLE IF EXISTS `config_svr`;
CREATE TABLE `config_svr` (
  `id` int(11) NOT NULL DEFAULT '0',
  `svrtype` int(11) NOT NULL DEFAULT '0',
  `subtype` int(11) NOT NULL DEFAULT '0',
  `svrid` int(11) NOT NULL DEFAULT '0',
  `port` int(11) NOT NULL DEFAULT '0',
  `config` varchar(512) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `hide` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
