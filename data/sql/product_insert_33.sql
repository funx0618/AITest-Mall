-- 小米（MI）小米电视4A (id=33)

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
(6, 35, 0, 12,
 '小米（MI）小米电视4A ',
 'http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180615/5b02804dN66004d73.jpg',
 '4609652', 0, 1, 0, 0,
 0, 0, 0, 2499.00, NULL, 0, 0,
 0, '小米（MI）小米电视4A 55英寸 L55M5-AZ/L55M5-AD 2GB+8GB HDR 4K超高清 人工智能网络液晶平板电视',
 '', 2499.00, 100, 0,
 '', '0.00', 0, '', '', '',
 '', '', '', '', '',
 NULL, NULL, 0, 0,
 '小米', '电视');

INSERT INTO pms_sku_stock (product_id, sku_code, price, stock, low_stock, pic, sale, promotion_price, lock_stock, sp_data)
VALUES (33, '202004190033001', 2499.00, 414, 10, NULL, NULL, NULL, 0, '[{"key":"尺寸","value":"50英寸"},{"key":"内存","value":"8G"}]');
INSERT INTO pms_sku_stock (product_id, sku_code, price, stock, low_stock, pic, sale, promotion_price, lock_stock, sp_data)
VALUES (33, '202004190033002', 2499.00, 500, 10, NULL, NULL, NULL, 0, '[{"key":"尺寸","value":"50英寸"},{"key":"内存","value":"16G"}]');
INSERT INTO pms_sku_stock (product_id, sku_code, price, stock, low_stock, pic, sale, promotion_price, lock_stock, sp_data)
VALUES (33, '202004190033003', 2499.00, 500, 10, NULL, NULL, NULL, 0, '[{"key":"尺寸","value":"65英寸"},{"key":"内存","value":"8G"}]');
INSERT INTO pms_sku_stock (product_id, sku_code, price, stock, low_stock, pic, sale, promotion_price, lock_stock, sp_data)
VALUES (33, '202004190033004', 2499.00, 500, 10, NULL, NULL, NULL, 0, '[{"key":"尺寸","value":"65英寸"},{"key":"内存","value":"16G"}]');

INSERT INTO pms_member_price (product_id, member_level_id, member_price, member_level_name) VALUES (33, 1, NULL, '黄金会员');
INSERT INTO pms_member_price (product_id, member_level_id, member_price, member_level_name) VALUES (33, 2, NULL, '白金会员');
INSERT INTO pms_member_price (product_id, member_level_id, member_price, member_level_name) VALUES (33, 3, NULL, '钻石会员');

INSERT INTO pms_product_ladder (product_id, count, discount, price) VALUES (33, 0, 0.00, 0.00);

INSERT INTO pms_product_full_reduction (product_id, full_price, reduce_price) VALUES (33, 0.00, 0.00);

INSERT INTO pms_product_attribute_value (product_id, product_attribute_id, value) VALUES (33, 54, '4609652');
INSERT INTO pms_product_attribute_value (product_id, product_attribute_id, value) VALUES (33, 55, '28.6kg');
INSERT INTO pms_product_attribute_value (product_id, product_attribute_id, value) VALUES (33, 56, '中国大陆');
INSERT INTO pms_product_attribute_value (product_id, product_attribute_id, value) VALUES (33, 57, '大屏');
