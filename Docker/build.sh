img_name=17806707983/asr  # 镜像名，即项目名
img_tag=`date '+%Y%m%d_%H%M%S'`  # 声明镜像tag为 日期+时间（实践中需要关联上git的commit-id）

docker build -f Docker/Dockerfile -t ${img_name}:${img_tag} .