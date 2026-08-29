-- 华为 HUAWEI P20 (id=26)

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
(3, 19, 0, 3,
 '华为 HUAWEI P20 ',
 'http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180607/5ac1bf58Ndefaac16.jpg',
 '6946605', 0, 1, 1, 1,
 0, 100, 100, 3788.00, 3659.00, 3788, 3788,
 0, 'AI智慧全面屏 6GB +64GB 亮黑色 全网通版  移动联通电信4G手机 双卡双待手机 双卡双待',
 '', 4288.00, 1000, 0,
 '件', '0.00', 1, '2,3,1', '', '',
 'http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180607/5ab46a3cN616bdc41.jpg,http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180607/5ac1bf5fN2522b9dc.jpg',
 '', '', '<p><img class="wscnph" src="http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180607/5ad44f1cNf51f3bb0.jpg" /><img class="wscnph" src="http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180607/5ad44fa8Nfcf71c10.jpg" /><img class="wscnph" src="http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180607/5ad44fa9N40e78ee0.jpg" /><img class="wscnph" src="http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180607/5ad457f4N1c94bdda.jpg" /><img class="wscnph" src="http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180607/5ad457f5Nd30de41d.jpg" /><img class="wscnph" src="http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180607/5b10fb0eN0eb053fb.jpg" /></p>',
 '<p><img src="//img20.360buyimg.com/vc/jfs/t1/81293/35/5822/369414/5d3fe77cE619c5487/6e775a52850feea5.jpg!q70.dpg.webp" alt="" width="750" height="776" /></p>',
 NULL, NULL, 0, 0,
 NULL, NULL);

INSERT INTO pms_sku_stock (product_id, sku_code, price, stock, low_stock, pic, sale, promotion_price, lock_stock, sp_data)
VALUES (26, '201806070026001', 3788.00, 487, NULL, NULL, NULL, 3699.00, 4, '[{"key":"颜色","value":"金色"},{"key":"容量","value":"16G"}]');
INSERT INTO pms_sku_stock (product_id, sku_code, price, stock, low_stock, pic, sale, promotion_price, lock_stock, sp_data)
VALUES (26, '201806070026002', 3999.00, 499, NULL, NULL, NULL, 3899.00, 0, '[{"key":"颜色","value":"金色"},{"key":"容量","value":"32G"}]');
INSERT INTO pms_sku_stock (product_id, sku_code, price, stock, low_stock, pic, sale, promotion_price, lock_stock, sp_data)
VALUES (26, '201806070026003', 3788.00, 500, NULL, NULL, NULL, 3699.00, 0, '[{"key":"颜色","value":"银色"},{"key":"容量","value":"16G"}]');
INSERT INTO pms_sku_stock (product_id, sku_code, price, stock, low_stock, pic, sale, promotion_price, lock_stock, sp_data)
VALUES (26, '201806070026004', 3999.00, 500, NULL, NULL, NULL, 3899.00, 0, '[{"key":"颜色","value":"银色"},{"key":"容量","value":"32G"}]');

INSERT INTO pms_member_price (product_id, member_level_id, member_price, member_level_name) VALUES (26, 1, NULL, '黄金会员');
INSERT INTO pms_member_price (product_id, member_level_id, member_price, member_level_name) VALUES (26, 2, NULL, '白金会员');
INSERT INTO pms_member_price (product_id, member_level_id, member_price, member_level_name) VALUES (26, 3, NULL, '钻石会员');

INSERT INTO pms_product_ladder (product_id, count, discount, price) VALUES (26, 0, 0.00, 0.00);

INSERT INTO pms_product_full_reduction (product_id, full_price, reduce_price) VALUES (26, 3000.00, 300.00);
INSERT INTO pms_product_full_reduction (product_id, full_price, reduce_price) VALUES (26, 5000.00, 500.00);

INSERT INTO pms_product_attribute_value (product_id, product_attribute_id, value) VALUES (26, 43, '金色,银色');
INSERT INTO pms_product_attribute_value (product_id, product_attribute_id, value) VALUES (26, 45, '5.0');
INSERT INTO pms_product_attribute_value (product_id, product_attribute_id, value) VALUES (26, 46, '4G');
INSERT INTO pms_product_attribute_value (product_id, product_attribute_id, value) VALUES (26, 47, 'Android');
INSERT INTO pms_product_attribute_value (product_id, product_attribute_id, value) VALUES (26, 48, '3000');

INSERT INTO cms_subject_product_relation (subject_id, product_id) VALUES (2, 26);
INSERT INTO cms_subject_product_relation (subject_id, product_id) VALUES (3, 26);
INSERT INTO cms_subject_product_relation (subject_id, product_id) VALUES (6, 26);
