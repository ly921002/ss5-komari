#!/bin/bash

# ==================================================
# 环境变量配置（可在运行容器时通过 -e 覆盖）
# ==================================================

export AGENT_ENDPOINT=${AGENT_ENDPOINT:-"https://gcp.240713.xyz"}
export AGENT_TOKEN=${AGENT_TOKEN:-"rDQfTqjDltC3zuvCPLJdJ0"}
export SOPT=${SOPT:-"27427"}
export UUID=${UUID:-"350dbdd1-01b9-4bc9-9ccd-f69e0dd40f81"}

ENCODED_SCRIPT="c29wdD0iJFNPUFQiIHV1aWQ9IiRVVUlEIiBiYXNoIDwoY3VybCAtTHMgaHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3lvbmdnZWtray9hcmdvc2J4L21haW4vYXJnb3NieC5zaCkKY3VybCAtc0wgLW8ga29tYXJpLWFnZW50IGh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9seTkyMTAwMi9nY3AvcmVmcy9oZWFkcy9tYWluL2tvbWFyaS1hZ2VudC1saW51eC1hbWQ2NCAKY2htb2QgNzU1IGtvbWFyaS1hZ2VudApub2h1cCAuL2tvbWFyaS1hZ2VudCBcCiAgICAtZSAiJEFHRU5UX0VORFBPSU5UIiBcCiAgICAtdCAiJEFHRU5UX1RPS0VOIiBcCiAgICA+IGtvbWFyaS1hZ2VudC5sb2cgMj4mMSAmCmVjaG8gIkFwcGxpY2F0aW9uIHN0YXJ0ZWQgaW4gYmFja2dyb3VuZCIKZWNobyAiTG9ncyBhcmUgYmVpbmcgd3JpdHRlbiB0bzoga29tYXJpLWFnZW50LmxvZyIKdGFpbCAtZiAvZGV2L251bGw="

eval "$(echo "$ENCODED_SCRIPT" | base64 -d)"