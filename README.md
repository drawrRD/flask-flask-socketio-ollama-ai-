1. 数据库基于flask_sqlalchemy，需要用flask_migrate命令迁移数据库
2. 注册账号 需要用自己的邮箱作为发送邮箱，要开启POP3/SMTP/IMAP。登录邮箱–设置–账户–开启POP3/SMTP/IMAP
3. 验证码基于redis存储，需要下载redis，并启动redis-server
4. ai问答 基于本地大模型部署服务ollama，github上直接下载ollama启动后监听11434端口，本项目ai问答模块基于qwen2:7b模型，若需使用需提前下载 https://github.com/ollama/ollama
5. settings.py文件中的配置需改为本机的配置
6. 本项目成功在centos中 基于nginx+uwsgi部署，能在公网访问， 部署参考： https://www.bilibili.com/read/cv27195598/?from=search
7. 前后端不分离，部分前端代码以及flask学习的网络课程为：https://www.bilibili.com/video/BV17r4y1y7jJ/?spm_id_from=333.999.0.0
8. socketio的实现源于：https://github.com/cgynb/a-flask-project/tree/chat 和 flask-socketio的官方文档
9. 添加celery异步任务队列的生产实现与部署，参考 https://www.cnblogs.com/gdbd/p/17367220.html
10. 边学边写的项目，覆盖了在学习flask过程中的大多数知识点，功能并不完善，健壮性未考虑，仅作为个人学习记录用



<img width="739" alt="Snipaste_2024-09-06_20-28-39" src="https://github.com/user-attachments/assets/97cac5c5-8f43-43c0-bc51-2d50d4518b4c">
<img width="1020" alt="Snipaste_2024-09-06_20-28-56" src="https://github.com/user-attachments/assets/19bd27a5-7d2e-4f78-acda-9264e2d9fb1c">
<img width="378" alt="Snipaste_2024-09-06_20-29-04" src="https://github.com/user-attachments/assets/a8ba018f-1315-4038-9ee4-749ff6917616">
<img width="997" alt="Snipaste_2024-09-06_20-29-52" src="https://github.com/user-attachments/assets/59b6d8be-758d-46ad-8d44-1ed5acfc8b31">
<img width="1083" alt="Snipaste_2024-09-06_20-29-59" src="https://github.com/user-attachments/assets/1d25f711-12b7-44c6-9b44-39bcc099074f">
<img width="1219" alt="Snipaste_2024-09-06_20-30-31" src="https://github.com/user-attachments/assets/2e6de0a2-19e3-4428-bf0e-7d49acb30027">
