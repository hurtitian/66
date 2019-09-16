DROP TABLE IF EXISTS `china`;
CREATE TABLE `china` (
  `id` INT(11) NOT NULL,
  `name` VARCHAR(40) DEFAULT NULL,
  `pid` INT(11) DEFAULT NULL,
  PRIMARY KEY  (`id`),
  KEY `FK_CHINA_REFERENCE_CHINA` (`pid`),
  CONSTRAINT `FK_CHINA_REFERENCE_CHINA` FOREIGN KEY (`pid`) REFERENCES `china` (`id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8;