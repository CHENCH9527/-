# 杭州每日天气微信提醒

每天北京时间 06:30 获取杭州当天的天气，并通过 PushPlus 推送到个人微信。

## 配置步骤

1. 注册并登录 [PushPlus](https://www.pushplus.plus/)，绑定个人微信，获取用户 Token。
2. 新建一个 GitHub 仓库，把本目录中的 `weather.py` 和 `.github/workflows/daily-weather.yml` 上传到仓库根目录。
3. 打开仓库的 `Settings -> Secrets and variables -> Actions`。
4. 新建 Repository secret：

   ```text
   Name: PUSHPLUS_TOKEN
   Secret: 你的 PushPlus Token
   ```

5. 进入仓库的 `Actions` 页面，选择 `Daily Hangzhou Weather`，点击 `Run workflow` 手动测试一次。

## 时间说明

定时表达式是 `30 22 * * *`，GitHub 按 UTC 执行，对应北京时间每天 06:30。

GitHub Actions 的定时任务可能因为平台负载延迟几分钟。如果必须严格在 06:30 发送，建议把同一个脚本放到云服务器、腾讯云函数或阿里云函数计算中运行。

## 天气数据

天气来自 Open-Meteo，位置固定为杭州：

- 纬度：30.2741
- 经度：120.1551
- 时区：Asia/Shanghai

脚本发送当天的天气、最高/最低温度、降水概率、降水量、最大风速、紫外线指数、日出和日落时间。
