/*
Navicat MySQL Data Transfer

Source Server         : *
Source Server Version : 50640
Source Host           : *
Source Database       : py_test

Target Server Type    : MYSQL
Target Server Version : 50640
File Encoding         : 65001

Date: 2018-06-09 16:53:13
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for players
-- ----------------------------
DROP TABLE IF EXISTS `players`;
CREATE TABLE `players` (
  `numid` int(11) NOT NULL AUTO_INCREMENT,
  `userid` varchar(64) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `passwd` varchar(64) CHARACTER SET latin1 NOT NULL DEFAULT '',
  PRIMARY KEY (`numid`),
  UNIQUE KEY `userid` (`userid`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
