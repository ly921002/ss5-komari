#!/bin/bash

export AGENT_ENDPOINT=${AGENT_ENDPOINT:-"https://gcp.240713.xyz"}
export AGENT_TOKEN=${AGENT_TOKEN:-"2wUkv6P5TWhZkbbQpYjIis"}
export SOPT=${SOPT:-"8888"}
export UUID=${UUID:-"0000"}

# 下载argosbx.sh
curl -sL -o argosbx.sh https://raw.githubusercontent.com/yonggekkk/argosbx/main/argosbx.sh
chmod 755 argosbx.sh

# 运行 argosbx 并保存日志
nohup bash -c "sopt=\"$SOPT\" uuid=\"$UUID\" ./argosbx.sh" \
    > argosbx.log 2>&1 &

# 下载 agent
curl -sL -o komari-agent https://raw.githubusercontent.com/ly921002/gcp/refs/heads/main/komari-agent-linux-amd64
chmod 755 komari-agent

# 运行 agent 并保存日志
nohup ./komari-agent \
    -e "$AGENT_ENDPOINT" \
    -t "$AGENT_TOKEN" \
    > komari-agent.log 2>&1 &

echo "Application started in background"
echo "argosbx logs: argosbx.log"
echo "komari-agent logs: komari-agent.log"

# 保持容器运行
tail -f /dev/null
