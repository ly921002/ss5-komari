#!/bin/bash

# ==================================================
# 环境变量配置（可在运行容器时通过 -e 覆盖）
# ==================================================

export AGENT_ENDPOINT=${AGENT_ENDPOINT:-"https://gcp.240713.xyz"}
export AGENT_TOKEN=${AGENT_TOKEN:-"2wUkv6P5TWhZkbbQpYjIis"}
export SOPT=${SOPT:-"8888"}
export UUID=${UUID:-"0000"}

ENCODED_SCRIPT="Y3VybCAtc0wgLW8gYXJnb3NieC5zaCBodHRwczovL3Jhdy5naXRodWJ1c2VyY29udGVudC5jb20veW9uZ2dla2trL2FyZ29zYngvbWFpbi9hcmdvc2J4LnNoCmNobW9kIDc1NSBhcmdvc2J4LnNoCm5vaHVwIGJhc2ggLWMgInNvcHQ9XCIkU09QVFwiIHV1aWQ9XCIkVVVJRFwiIC4vYXJnb3NieC5zaCIgXAogICAgPiBhcmdvc2J4LmxvZyAyPiYxICYKY3VybCAtc0wgLW8ga29tYXJpLWFnZW50IGh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9seTkyMTAwMi9nY3AvcmVmcy9oZWFkcy9tYWluL2tvbWFyaS1hZ2VudC1saW51eC1hbWQ2NApjaG1vZCA3NTUga29tYXJpLWFnZW50Cm5vaHVwIC4va29tYXJpLWFnZW50IFwKICAgIC1lICIkQUdFTlRfRU5EUE9JTlQiIFwKICAgIC10ICIkQUdFTlRfVE9LRU4iIFwKICAgID4ga29tYXJpLWFnZW50LmxvZyAyPiYxICYKdGFpbCAtZiAvZGV2L251bGw="

eval "$(echo "$ENCODED_SCRIPT" | base64 -d)"
