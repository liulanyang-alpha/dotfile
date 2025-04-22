#!/bin/bash

# 容器SSH隧道代理脚本
# 用法: ./docker-ssh-tunnel.sh 服务器名 容器名 容器端口

set -e

# 参数检查
if [ $# -lt 3 ]; then
  echo "用法: $0 服务器名 容器名 容器端口"
  echo "示例: $0 4090 container 8080"
  exit 1
fi

CONTAINER_NAME=$1
CONTAINER_PORT=$2
LOCAL_PORT=$2
SERVER=$3

ssh -t $SERVER "docker exec -it $CONTAINER_NAME  bash -c 'service ssh restart'"

echo $CONTAINER_NAME $CONTAINER_PORT $SERVER
echo "🔍 正在查找容器 $CONTAINER_NAME 的IP地址..."
CONTAINER_IP=$(ssh $SERVER "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $CONTAINER_NAME" 2>/dev/null)

if [ -z "$CONTAINER_IP" ]; then
  echo "❌ 无法获取容器IP，请检查:"
  echo "1. 容器名称是否正确"
  echo "2. 容器是否正在运行"
  echo "3. 是否有权限访问该容器"
  exit 1
fi

echo "✅ 容器IP: $CONTAINER_IP"
echo "🚀 正在建立SSH隧道: 本地端口 $LOCAL_PORT -> $CONTAINER_IP:$CONTAINER_PORT"

# 建立隧道
ssh -L $LOCAL_PORT:$CONTAINER_IP:$CONTAINER_PORT $SERVER
