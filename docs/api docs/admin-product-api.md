# Mall Admin Service — 商品相关 API Reference

> **Base URL:** `http://localhost:8080`
> **Swagger UI:** `http://localhost:8080/swagger-ui.html`

---

## 1. `PmsProductController` — 商品管理
**Base path:** `/product`

### `POST /product/create` — 创建商品
**涉及表：** `pms_product`, `pms_member_price`, `pms_product_ladder`, `pms_product_full_reduction`, `pms_sku_stock`, `pms_product_attribute_value`, `cms_subject_product_relation`, `cms_prefrence_area_product_relation`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `productParam` | `PmsProductParam` | `@RequestBody` | 商品创建参数（见下方 DTO） |

### `GET /product/updateInfo/{id}` — 获取商品编辑信息
**涉及表：** `pms_product`, `pms_member_price`, `pms_product_ladder`, `pms_product_full_reduction`, `pms_sku_stock`, `pms_product_attribute_value`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 商品 ID |

### `POST /product/update/{id}` — 更新商品
**涉及表：** `pms_product`, `pms_member_price`, `pms_product_ladder`, `pms_product_full_reduction`, `pms_sku_stock`, `pms_product_attribute_value`, `cms_subject_product_relation`, `cms_prefrence_area_product_relation`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 商品 ID |
| `productParam` | `PmsProductParam` | `@RequestBody` | 商品更新参数 |

### `GET /product/list` — 分页查询商品
**涉及表：** `pms_product`

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `keyword` | `String` | Model Attribute | — | 商品名称模糊关键字 |
| `productSn` | `String` | Model Attribute | — | 商品货号 |
| `productCategoryId` | `Long` | Model Attribute | — | 商品分类编号 |
| `brandId` | `Long` | Model Attribute | — | 商品品牌编号 |
| `publishStatus` | `Integer` | Model Attribute | — | 上架状态 |
| `verifyStatus` | `Integer` | Model Attribute | — | 审核状态 |
| `pageSize` | `Integer` | `@RequestParam` | `5` | 每页数量 |
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |

### `GET /product/simpleList` — 按名称/货号模糊查询
**涉及表：** `pms_product`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `keyword` | `String` | Model Attribute | 搜索关键字（商品名称或货号） |

### `POST /product/update/verifyStatus` — 批量修改审核状态
**涉及表：** `pms_product`, `pms_product_vertify_record`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `ids` | `List<Long>` | `@RequestParam` | 商品 ID 列表 |
| `verifyStatus` | `Integer` | `@RequestParam` | 0=未审核, 1=审核通过 |
| `detail` | `String` | `@RequestParam` | 审核备注 |

### `POST /product/update/publishStatus` — 批量上下架商品
**涉及表：** `pms_product`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `ids` | `List<Long>` | `@RequestParam` | 商品 ID 列表 |
| `publishStatus` | `Integer` | `@RequestParam` | 0=下架, 1=上架 |

### `POST /product/update/recommendStatus` — 批量推荐商品
**涉及表：** `pms_product`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `ids` | `List<Long>` | `@RequestParam` | 商品 ID 列表 |
| `recommendStatus` | `Integer` | `@RequestParam` | 0=不推荐, 1=推荐 |

### `POST /product/update/newStatus` — 批量设为新品
**涉及表：** `pms_product`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `ids` | `List<Long>` | `@RequestParam` | 商品 ID 列表 |
| `newStatus` | `Integer` | `@RequestParam` | 0=非新品, 1=新品 |

### `POST /product/update/deleteStatus` — 批量软删除商品
**涉及表：** `pms_product`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `ids` | `List<Long>` | `@RequestParam` | 商品 ID 列表 |
| `deleteStatus` | `Integer` | `@RequestParam` | 0=未删除, 1=已删除 |

#### DTO: `PmsProductParam`（创建/更新商品的请求体）

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `brandId` | `Long` | | 品牌 ID |
| `productCategoryId` | `Long` | | 商品分类 ID |
| `name` | `String` | | 商品名称 |
| `productSn` | `String` | | 货号 |
| `price` | `BigDecimal` | | 价格 |
| `originalPrice` | `BigDecimal` | | 市场价 |
| `stock` | `Integer` | | 库存 |
| `lowStock` | `Integer` | | 库存预警值 |
| `subTitle` | `String` | | 副标题 |
| `pic` | `String` | | 主图 |
| `albumPics` | `String` | | 图册（逗号分隔，最多5张） |
| `unit` | `String` | | 单位 |
| `weight` | `BigDecimal` | | 重量（克） |
| `sort` | `Integer` | | 排序 |
| `publishStatus` | `Integer` | | 0=下架, 1=上架 |
| `newStatus` | `Integer` | | 0=非新品, 1=新品 |
| `recommandStatus` | `Integer` | | 0=不推荐, 1=推荐 |
| `verifyStatus` | `Integer` | | 0=未审核, 1=已审核 |
| `promotionType` | `Integer` | | 0=无促销, 1=促销, 2=会员, 3=阶梯, 4=满减, 5=秒杀 |
| `promotionPrice` | `BigDecimal` | | 促销价格 |
| `promotionStartTime` | `Date` | | 促销开始时间 |
| `promotionEndTime` | `Date` | | 促销结束时间 |
| `promotionPerLimit` | `Integer` | | 限购数量 |
| `giftGrowth` | `Integer` | | 赠送成长值 |
| `giftPoint` | `Integer` | | 赠送积分 |
| `usePointLimit` | `Integer` | | 最大可用积分 |
| `serviceIds` | `String` | | 服务（逗号分隔：1=退换, 2=极速退款, 3=包邮） |
| `keywords` | `String` | | 关键字 |
| `note` | `String` | | 备注 |
| `detailTitle` | `String` | | 详情标题 |
| `detailDesc` | `String` | | 详情描述 |
| `detailHtml` | `String` | | 详情 HTML（PC端） |
| `detailMobileHtml` | `String` | | 详情 HTML（移动端） |
| `feightTemplateId` | `Long` | | 运费模板 ID |
| `productAttributeCategoryId` | `Long` | | 属性分类 ID |
| `brandName` | `String` | | 品牌名称（冗余） |
| `productCategoryName` | `String` | | 分类名称（冗余） |
| `productLadderList` | `List<PmsProductLadder>` | | 阶梯价格列表 |
| `productFullReductionList` | `List<PmsProductFullReduction>` | | 满减列表 |
| `memberPriceList` | `List<PmsMemberPrice>` | | 会员价格列表 |
| `skuStockList` | `List<PmsSkuStock>` | | SKU 库存列表 |
| `productAttributeValueList` | `List<PmsProductAttributeValue>` | | 属性值列表 |
| `subjectProductRelationList` | `List<CmsSubjectProductRelation>` | | 专题关联列表 |
| `prefrenceAreaProductRelationList` | `List<CmsPrefrenceAreaProductRelation>` | | 优选专区关联列表 |

---

## 2. `PmsBrandController` — 品牌管理
**Base path:** `/brand`

### `GET /brand/listAll` — 获取全部品牌列表
**涉及表：** `pms_brand`

无参数

### `GET /brand/list` — 分页查询品牌列表
**涉及表：** `pms_brand`

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `keyword` | `String` | `@RequestParam` | — | 品牌名称关键字 |
| `showStatus` | `Integer` | `@RequestParam` | — | 显示状态筛选 |
| `pageSize` | `Integer` | `@RequestParam` | `5` | 每页数量 |
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |

### `GET /brand/{id}` — 根据 ID 查询品牌详情
**涉及表：** `pms_brand`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 品牌 ID |

### `POST /brand/create` — 添加品牌
**涉及表：** `pms_brand`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `pmsBrand` | `PmsBrandParam` | `@Validated @RequestBody` | 品牌参数（见下方 DTO） |

### `POST /brand/update/{id}` — 更新品牌
**涉及表：** `pms_brand`, `pms_product`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 品牌 ID |
| `pmsBrandParam` | `PmsBrandParam` | `@Validated @RequestBody` | 品牌参数 |

### `GET /brand/delete/{id}` — 删除品牌
**涉及表：** `pms_brand`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 品牌 ID |

### `POST /brand/delete/batch` — 批量删除品牌
**涉及表：** `pms_brand`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `ids` | `List<Long>` | `@RequestParam` | 品牌 ID 列表 |

### `POST /brand/update/showStatus` — 批量更新显示状态
**涉及表：** `pms_brand`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `ids` | `List<Long>` | `@RequestParam` | 品牌 ID 列表 |
| `showStatus` | `Integer` | `@RequestParam` | 0=隐藏, 1=显示 |

### `POST /brand/update/factoryStatus` — 批量更新厂家制造商状态
**涉及表：** `pms_brand`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `ids` | `List<Long>` | `@RequestParam` | 品牌 ID 列表 |
| `factoryStatus` | `Integer` | `@RequestParam` | 0=否, 1=是 |

#### DTO: `PmsBrandParam`（创建/更新品牌的请求体）

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `name` | `String` | ✅ | 品牌名称 |
| `logo` | `String` | ✅ | 品牌 Logo |
| `firstLetter` | `String` | | 首字母 |
| `sort` | `Integer` | | 排序（≥0） |
| `factoryStatus` | `Integer` | | 是否厂家制造商（0/1） |
| `showStatus` | `Integer` | | 是否显示（0/1） |
| `bigPic` | `String` | | 品牌大图 |
| `brandStory` | `String` | | 品牌故事 |

---

## 3. `PmsProductCategoryController` — 商品分类管理
**Base path:** `/productCategory`

### `GET /productCategory/list/{parentId}` — 分页查询商品分类
**涉及表：** `pms_product_category`

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `parentId` | `Long` | `@PathVariable` | — | 父分类 ID |
| `pageSize` | `Integer` | `@RequestParam` | `5` | 每页数量 |
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |

### `GET /productCategory/{id}` — 根据 ID 获取商品分类
**涉及表：** `pms_product_category`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 分类 ID |

### `GET /productCategory/list/withChildren` — 查询所有一级分类及子分类
**涉及表：** `pms_product_category`

无参数

### `POST /productCategory/create` — 添加商品分类
**涉及表：** `pms_product_category`, `pms_product_category_attribute_relation`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `productCategoryParam` | `PmsProductCategoryParam` | `@Validated @RequestBody` | 分类参数（见下方 DTO） |

### `POST /productCategory/update/{id}` — 修改商品分类
**涉及表：** `pms_product_category`, `pms_product_category_attribute_relation`, `pms_product`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 分类 ID |
| `productCategoryParam` | `PmsProductCategoryParam` | `@Validated @RequestBody` | 分类参数 |

### `POST /productCategory/delete/{id}` — 删除商品分类
**涉及表：** `pms_product_category`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 分类 ID |

### `POST /productCategory/update/navStatus` — 修改导航栏显示状态
**涉及表：** `pms_product_category`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `ids` | `List<Long>` | `@RequestParam` | 分类 ID 列表 |
| `navStatus` | `Integer` | `@RequestParam` | 0=不显示, 1=显示 |

### `POST /productCategory/update/showStatus` — 修改显示状态
**涉及表：** `pms_product_category`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `ids` | `List<Long>` | `@RequestParam` | 分类 ID 列表 |
| `showStatus` | `Integer` | `@RequestParam` | 0=不显示, 1=显示 |

#### DTO: `PmsProductCategoryParam`（创建/更新分类的请求体）

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `parentId` | `Long` | | 父分类 ID |
| `name` | `String` | ✅ | 分类名称 |
| `productUnit` | `String` | | 分类单位 |
| `navStatus` | `Integer` | | 导航栏显示（0/1） |
| `showStatus` | `Integer` | | 是否显示（0/1） |
| `sort` | `Integer` | | 排序（≥0） |
| `icon` | `String` | | 图标 |
| `keywords` | `String` | | 关键字 |
| `description` | `String` | | 描述 |
| `productAttributeIdList` | `List<Long>` | | 关联筛选属性 ID 列表 |

---

## 4. `PmsProductAttributeController` — 商品属性管理
**Base path:** `/productAttribute`

### `GET /productAttribute/list/{cid}` — 按分类查询属性/参数列表
**涉及表：** `pms_product_attribute`

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `cid` | `Long` | `@PathVariable` | — | 属性分类 ID |
| `type` | `Integer` | `@RequestParam` | — | **必填。** 0=属性, 1=参数 |
| `pageSize` | `Integer` | `@RequestParam` | `5` | 每页数量 |
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |

### `GET /productAttribute/{id}` — 查询单个商品属性
**涉及表：** `pms_product_attribute`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 属性 ID |

### `GET /productAttribute/attrInfo/{productCategoryId}` — 获取分类下的属性及属性分类
**涉及表：** `pms_product_attribute`, `pms_product_attribute_category`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `productCategoryId` | `Long` | `@PathVariable` | 商品分类 ID |

### `POST /productAttribute/create` — 添加商品属性
**涉及表：** `pms_product_attribute`, `pms_product_attribute_category`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `productAttributeParam` | `PmsProductAttributeParam` | `@RequestBody` | 属性参数（见下方 DTO） |

### `POST /productAttribute/update/{id}` — 修改商品属性
**涉及表：** `pms_product_attribute`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 属性 ID |
| `productAttributeParam` | `PmsProductAttributeParam` | `@RequestBody` | 属性参数 |

### `POST /productAttribute/delete` — 批量删除商品属性
**涉及表：** `pms_product_attribute`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `ids` | `List<Long>` | `@RequestParam` | 属性 ID 列表 |

#### DTO: `PmsProductAttributeParam`（创建/更新属性的请求体）

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `productAttributeCategoryId` | `Long` | ✅ | 属性分类 ID |
| `name` | `String` | ✅ | 属性名称 |
| `selectType` | `Integer` | | 0=唯一, 1=单选, 2=多选 |
| `inputType` | `Integer` | | 0=手工录入, 1=从列表选取 |
| `inputList` | `String` | | 可选值列表（逗号分隔） |
| `sort` | `Integer` | | 排序 |
| `filterType` | `Integer` | | 0=普通, 1=颜色 |
| `searchType` | `Integer` | | 0=不检索, 1=关键字检索, 2=范围检索 |
| `relatedStatus` | `Integer` | | 0=不关联, 1=关联 |
| `handAddStatus` | `Integer` | | 0=不支持手动新增, 1=支持 |
| `type` | `Integer` | | 0=规格, 1=参数 |

---

## 5. `PmsProductAttributeCategoryController` — 属性分类管理
**Base path:** `/productAttribute/category`

### `GET /productAttribute/category/list` — 分页获取所有属性分类
**涉及表：** `pms_product_attribute_category`

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `pageSize` | `Integer` | `@RequestParam` | `5` | 每页数量 |
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |

### `GET /productAttribute/category/{id}` — 获取单个属性分类详情
**涉及表：** `pms_product_attribute_category`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 属性分类 ID |

### `GET /productAttribute/category/list/withAttr` — 获取所有属性分类及其下属性
**涉及表：** `pms_product_attribute_category`

无参数

### `POST /productAttribute/category/create` — 添加属性分类
**涉及表：** `pms_product_attribute_category`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `name` | `String` | `@RequestParam` | 属性分类名称 |

### `POST /productAttribute/category/update/{id}` — 修改属性分类
**涉及表：** `pms_product_attribute_category`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 属性分类 ID |
| `name` | `String` | `@RequestParam` | 新名称 |

### `GET /productAttribute/category/delete/{id}` — 删除属性分类
**涉及表：** `pms_product_attribute_category`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 属性分类 ID |

---

## 6. `PmsSkuStockController` — SKU 库存管理
**Base path:** `/sku`

### `GET /sku/{pid}` — 按商品 ID 搜索 SKU 库存
**涉及表：** `pms_sku_stock`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `pid` | `Long` | `@PathVariable` | 商品 ID |
| `keyword` | `String` | `@RequestParam(required=false)` | SKU 编码关键字（可选） |

### `POST /sku/update/{pid}` — 批量更新 SKU 库存
**涉及表：** `pms_sku_stock`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `pid` | `Long` | `@PathVariable` | 商品 ID |
| `skuStockList` | `List<PmsSkuStock>` | `@RequestBody` | SKU 库存列表 |

`PmsSkuStock` 字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `Long` | ID |
| `productId` | `Long` | 商品 ID |
| `skuCode` | `String` | SKU 编码 |
| `price` | `BigDecimal` | 价格 |
| `stock` | `Integer` | 库存 |
| `lowStock` | `Integer` | 预警库存 |
| `pic` | `String` | 展示图片 |
| `sale` | `Integer` | 销量 |
| `promotionPrice` | `BigDecimal` | 促销价格 |
| `lockStock` | `Integer` | 锁定库存 |
| `spData` | `String` | 销售属性 JSON |

---

## 涉及表汇总

| 表名 | 说明 |
|------|------|
| `pms_product` | 商品主表 |
| `pms_brand` | 品牌表 |
| `pms_product_category` | 商品分类表 |
| `pms_product_attribute` | 商品属性表 |
| `pms_product_attribute_category` | 属性分类表 |
| `pms_product_attribute_value` | 商品属性值表 |
| `pms_product_category_attribute_relation` | 分类-属性关联表 |
| `pms_sku_stock` | SKU 库存表 |
| `pms_member_price` | 会员价格表 |
| `pms_product_ladder` | 商品阶梯价格表 |
| `pms_product_full_reduction` | 商品满减表 |
| `pms_product_vertify_record` | 商品审核记录表 |
| `cms_subject_product_relation` | 专题-商品关联表 |
| `cms_prefrence_area_product_relation` | 优选专区-商品关联表 |

---

## 汇总

| Controller | 接口数 |
|------------|:---:|
| `PmsProductController` | 10 |
| `PmsBrandController` | 9 |
| `PmsProductCategoryController` | 8 |
| `PmsProductAttributeController` | 6 |
| `PmsProductAttributeCategoryController` | 6 |
| `PmsSkuStockController` | 2 |
| **合计** | **41** |
