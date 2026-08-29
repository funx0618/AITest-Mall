-- HLA海澜之家简约动物印花短袖T恤 (id=30)

INSERT INTO pms_product
(brand_id, product_category_id, feight_template_id, product_attribute_category_id,
 name, pic, product_sn, delete_status, publish_status, new_status, recommand_status,
 verify_status, sort, sale, price, promotion_price, gift_growth, gift_point,
 use_point_limit, sub_title, description, original_price, stock, low_stock,
 unit, weight, preview_status, service_ids, keywords, note, album_pics,
 detail_title, detail_desc, detail_html, detail_mobile_html,
 promotion_start_time, promotion_end_time, promotion_per_limit, promotion_type,
 brand_name, product_category_name)
VALUES
(50, 8, 0, 1,
 'HLA海澜之家简约动物印花短袖T恤',
 'http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180615/5ad83a4fN6ff67ecd.jpg!cc_350x449.jpg',
 'HNTBJ2E042A', 0, 1, 1, 1,
 0, 0, 0, 98.00, NULL, 0, 0,
 0, '2018夏季新品微弹舒适新款短T男生 6月6日-6月20日，满300减30，参与互动赢百元礼券，立即分享赢大奖',
 '', 98.00, 100, 0,
 '', '0.00', 0, '', '', '',
 '', '', '', '', '',
 NULL, NULL, 0, 0,
 '海澜之家', 'T恤');

INSERT INTO pms_sku_stock (product_id, sku_code, price, stock, low_stock, pic, sale, promotion_price, lock_stock, sp_data)
VALUES (30, '202004190030001', 88.00, 98, NULL, NULL, NULL, NULL, 0, '[{"key":"颜色","value":"蓝色"},{"key":"尺寸","value":"X"}]');
INSERT INTO pms_sku_stock (product_id, sku_code, price, stock, low_stock, pic, sale, promotion_price, lock_stock, sp_data)
VALUES (30, '202004190030002', 88.00, 100, NULL, NULL, NULL, NULL, 0, '[{"key":"颜色","value":"蓝色"},{"key":"尺寸","value":"XL"}]');
INSERT INTO pms_sku_stock (product_id, sku_code, price, stock, low_stock, pic, sale, promotion_price, lock_stock, sp_data)
VALUES (30, '202004190030003', 88.00, 66, NULL, NULL, NULL, NULL, 0, '[{"key":"颜色","value":"蓝色"},{"key":"尺寸","value":"M"}]');
INSERT INTO pms_sku_stock (product_id, sku_code, price, stock, low_stock, pic, sale, promotion_price, lock_stock, sp_data)
VALUES (30, '202004190030004', 88.00, 100, NULL, NULL, NULL, NULL, 0, '[{"key":"颜色","value":"白色"},{"key":"尺寸","value":"X"}]');
INSERT INTO pms_sku_stock (product_id, sku_code, price, stock, low_stock, pic, sale, promotion_price, lock_stock, sp_data)
VALUES (30, '202004190030005', 88.00, 100, NULL, NULL, NULL, NULL, 0, '[{"key":"颜色","value":"白色"},{"key":"尺寸","value":"XL"}]');
INSERT INTO pms_sku_stock (product_id, sku_code, price, stock, low_stock, pic, sale, promotion_price, lock_stock, sp_data)
VALUES (30, '202004190030006', 88.00, 100, NULL, NULL, NULL, NULL, 0, '[{"key":"颜色","value":"白色"},{"key":"尺寸","value":"M"}]');

INSERT INTO pms_member_price (product_id, member_level_id, member_price, member_level_name) VALUES (30, 1, NULL, '黄金会员');
INSERT INTO pms_member_price (product_id, member_level_id, member_price, member_level_name) VALUES (30, 2, NULL, '白金会员');
INSERT INTO pms_member_price (product_id, member_level_id, member_price, member_level_name) VALUES (30, 3, NULL, '钻石会员');

INSERT INTO pms_product_ladder (product_id, count, discount, price) VALUES (30, 0, 0.00, 0.00);

INSERT INTO pms_product_full_reduction (product_id, full_price, reduce_price) VALUES (30, 0.00, 0.00);

INSERT INTO pms_product_attribute_value (product_id, product_attribute_id, value) VALUES (30, 7, '蓝色,白色');
INSERT INTO pms_product_attribute_value (product_id, product_attribute_id, value) VALUES (30, 24, 'HNTBJ2E042A');
INSERT INTO pms_product_attribute_value (product_id, product_attribute_id, value) VALUES (30, 25, '夏季');
INSERT INTO pms_product_attribute_value (product_id, product_attribute_id, value) VALUES (30, 37, '青年');
INSERT INTO pms_product_attribute_value (product_id, product_attribute_id, value) VALUES (30, 38, '2018年夏');
INSERT INTO pms_product_attribute_value (product_id, product_attribute_id, value) VALUES (30, 39, '短袖');
