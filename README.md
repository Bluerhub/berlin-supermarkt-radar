# 柏林折扣雷达 · Berlin Angebote Radar

自用静态网页：11家商家、中文和德文商品名、食品/日用品/饮品/其他、商家筛选、本周/下周/未来预告、搜索和排序。支持手机浏览。

## 部署

1. 解压 ZIP，将整个文件夹（包括 `.github`）上传到新的 GitHub 仓库根目录。
2. 在 Netlify 选择 Import from Git → 连接该仓库。Publish directory 使用 `.`，无需构建命令。
3. GitHub Actions 的 `Weekly Berlin deals refresh` 每天检查已有优惠是否过期；也可手动运行。**这不是11家超市的完整自动抓取器**，不会自动凭空增加商品。要完成全自动采集，必须逐店开发、测试、维护适配器。
4. 新促销信息应核实后写入 `deals.json` 并提交 GitHub，Netlify 自动部署。可在网页导入 JSON 本地查看，但本地导入不会同步到 GitHub。

## 数据格式

`deals.json` 里 `deals` 数组每项：`store`（penny/rewe/kaufland/lidl/edeka/netto/dognetto/aldi/rossmann/mueller/dm）、`category`（food/household/drinks/other）、`zh`、`de`、`price`、`oldPrice`、`unit`、`start`、`end`、`url`、`verified`、`notes`。

`verified:true` 必须有真实来源链接和开始结束日期。未来优惠会在“下周/未来”标签显示。网站默认空数据，不造假。

## 官方页面参考

REWE 的门店页包含文字商品信息；Lidl、Aldi Nord 官方页面可找到下周宣传单入口；Rossmann 网店优惠不一定等于门店优惠。每个来源均需按柏林门店、活动资格和日期核实。
