1. 数据库基于flask_sqlalchemy，需要用flask_migrate命令迁移数据库
2. 注册账号 需要用自己的邮箱作为发送邮箱，要开启POP3/SMTP/IMAP。登录邮箱–设置–账户–开启POP3/SMTP/IMAP
3. 验证码基于redis存储，需要下载redis，并启动redis-server
4. ai问答 基本本地的ollama服务，github上直接下载ollama启动后监听11434端口，本项目ai问答模块基于qwen2:7b模型，若需使用需提前下载
5. settings.py文件中的配置需改为本机的配置
6. 本项目成功在centos中 基于nginx+uwsgi部署，能在公网访问
7. 边学边写的项目，覆盖了在学习flask过程中的大多数知识点，功能并不完善，健壮性未考虑，仅作为学习记录用
8. 前后端不分离，部分前端代码来源于：https://www.bilibili.com/video/BV17r4y1y7jJ/?spm_id_from=333.999.0.0
9. socketio的实现源于：https://github.com/cgynb/a-flask-project/tree/chat
