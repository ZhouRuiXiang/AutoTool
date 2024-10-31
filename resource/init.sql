# ************************************************************
# Sequel Ace SQL dump
# 版本号： 20064
#
# https://sequel-ace.com/
# https://github.com/Sequel-Ace/Sequel-Ace
#
# 主机: 8.137.14.45 (MySQL 5.7.36)
# 数据库: fishsale
# 生成时间: 2024-09-14 02:37:09 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
SET NAMES utf8mb4;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE='NO_AUTO_VALUE_ON_ZERO', SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# 转储表 order_info
# ------------------------------------------------------------

DROP TABLE IF EXISTS `order_info`;

CREATE TABLE `order_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `store_name` varchar(20) DEFAULT NULL COMMENT '店铺名称',
  `month` varchar(10) DEFAULT NULL COMMENT '订单月份',
  `cost_price` decimal(10,2) DEFAULT NULL COMMENT '商品成本价',
  `sale_price` decimal(10,2) DEFAULT NULL COMMENT '商品总售价',
  `order_id` varchar(50) DEFAULT NULL COMMENT '订单编号',
  `alipay_trans_id` varchar(50) DEFAULT NULL COMMENT '支付宝交易号',
  `nickname` varchar(20) DEFAULT NULL COMMENT '用户昵称',
  `product_name` varchar(100) DEFAULT NULL COMMENT '商品名称',
  `product_count` int(11) DEFAULT NULL COMMENT '商品数量',
  `product_size` varchar(20) DEFAULT NULL COMMENT '商品尺寸',
  `deliver_user` varchar(10) DEFAULT NULL COMMENT '收货人',
  `deliver_phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '收货人手机号',
  `deliver_full_address` varchar(200) DEFAULT NULL COMMENT '收货人地址',
  `deliver_province` varchar(10) DEFAULT NULL COMMENT '收货省份',
  `deliver_city` varchar(20) DEFAULT NULL COMMENT '收货地级市',
  `deliver_district` varchar(50) DEFAULT NULL COMMENT '收货区县',
  `deliver_detail` varchar(100) DEFAULT NULL COMMENT '收货详细地址',
  `track_num` varchar(50) DEFAULT NULL COMMENT '快递单号',
  `order_status` int(11) DEFAULT NULL COMMENT '订单状态(1-待发货 2-已下单 3-已发货 4-已完成 5-已退货)',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_alipay_trans_id` (`alipay_trans_id`),
  UNIQUE KEY `idx_order_id` (`order_id`),
  KEY `idx_nickname` (`nickname`),
  KEY `idx_product_name` (`product_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `order_info` WRITE;
/*!40000 ALTER TABLE `order_info` DISABLE KEYS */;

INSERT INTO `order_info` (`id`, `store_name`, `month`, `cost_price`, `sale_price`, `order_id`, `alipay_trans_id`, `nickname`, `product_name`, `product_count`, `product_size`, `deliver_user`, `deliver_phone`, `deliver_full_address`, `deliver_province`, `deliver_city`, `deliver_district`, `deliver_detail`, `track_num`, `order_status`, `create_time`, `update_time`)
VALUES
	(2,'星辰优选','202409',NULL,6.80,'4040368922882506610','2024091122001111311447213851','狮子1900','磁力工具架强磁条吸铁强磁吸收纳（6.8元包邮到家）',1,'20厘米','周修竹',X'3138383732373230323037','湖北省武汉市洪山区关东街道虎泉街299号保利华都1栋',NULL,NULL,NULL,NULL,NULL,2,'2024-09-12 17:07:33','2024-09-13 17:56:35'),
	(3,'星辰优选','202409',NULL,6.80,'4029546205522020644','2024090322001197971459729563','星辰家居','磁力工具架强磁条吸铁强磁吸收纳（6.8元包邮到家）',1,'20厘米','星辰',X'3137333734313538373534','湖北省武汉市汉阳区江堤街道蔷薇路华中中交城',NULL,NULL,NULL,NULL,NULL,2,'2024-09-13 15:16:23','2024-09-13 17:56:41'),
	(4,'星辰优选','202409',3.93,6.80,'4029835575610506610','2024090322001111311445605514','狮子1900','磁力工具架强磁条吸铁强磁吸收纳（6.8元包邮到家）',1,'20厘米','周修竹',X'3138383732373230323037','湖北省武汉市洪山区关东街道虎泉街299号保利华都1栋','湖北省','武汉市','洪山区','关东街道虎泉街299号保利华都1栋',NULL,2,'2024-09-13 00:00:00','2024-09-13 00:00:00'),
	(5,'星辰优选','202409',10.99,12.80,'4043039041111020644','2024091322001197971424768798','星辰家居','束口包膝泡脚养生桶折叠过小腿便携式足浴宿舍家庭用洗脚盆熏蒸保',1,'默认','星辰',X'3137333734313538373534','湖北省武汉市汉阳区江堤街道蔷薇路华中中交城','湖北省','武汉市','汉阳区','江堤街道蔷薇路华中中交城',NULL,2,'2024-09-13 00:00:00','2024-09-13 00:00:00');

/*!40000 ALTER TABLE `order_info` ENABLE KEYS */;
UNLOCK TABLES;


# 转储表 product
# ------------------------------------------------------------

DROP TABLE IF EXISTS `product`;

CREATE TABLE `product` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL COMMENT '商品名称',
  `pdd_search_name` varchar(50) DEFAULT NULL COMMENT 'pdd 搜素名称',
  `is_no_size` int(1) DEFAULT NULL COMMENT '尺寸配置 1 -有 0-无',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;

INSERT INTO `product` (`id`, `name`, `pdd_search_name`, `is_no_size`, `create_time`, `update_time`)
VALUES
	(1,'泡脚养生桶','泡脚桶',0,'2024-09-13 16:30:44','2024-09-13 16:32:27'),
	(2,'磁力工具架','磁力工具架',1,'2024-09-13 16:31:35','2024-09-13 16:32:33');

/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;


# 转储表 product_config
# ------------------------------------------------------------

DROP TABLE IF EXISTS `product_config`;

CREATE TABLE `product_config` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int(11) DEFAULT NULL COMMENT '商品ID',
  `pdd_search_name` varchar(100) DEFAULT NULL COMMENT 'pdd搜索商品名称',
  `fish_config` varchar(50) DEFAULT NULL COMMENT 'fish商品配置',
  `pdd_search_config` varchar(50) DEFAULT NULL COMMENT 'pdd商品配置',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `product_config` WRITE;
/*!40000 ALTER TABLE `product_config` DISABLE KEYS */;

INSERT INTO `product_config` (`id`, `product_id`, `pdd_search_name`, `fish_config`, `pdd_search_config`, `create_time`, `update_time`)
VALUES
	(1,1,'泡脚桶','默认','五层特厚蓝','2024-09-13 16:33:01','2024-09-13 16:34:17'),
	(2,2,'磁力工具架','20厘米','总长20厘米','2024-09-13 16:34:45','2024-09-13 16:34:58'),
	(3,2,'磁力工具架','30厘米','总长31厘米','2024-09-13 16:35:07','2024-09-13 16:35:16'),
	(4,2,'磁力工具架','46厘米','总长50厘米','2024-09-13 16:35:25','2024-09-13 16:36:00'),
	(5,2,'磁力工具架','61厘米','总长66厘米','2024-09-13 16:35:35','2024-09-13 16:36:04'),
	(6,2,'磁力工具架','85厘米','总长90厘米','2024-09-13 16:35:43','2024-09-13 16:36:07');

/*!40000 ALTER TABLE `product_config` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
