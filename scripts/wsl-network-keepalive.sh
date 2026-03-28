#!/bin/bash
# WSL2 网络保活脚本 v3
# 网络恢复时自动重启 Gateway，修复飞书 WebSocket 断连

LOG="$HOME/.openclaw/workspace/logs/network-keepalive.log"
RESTART_LOCK="/tmp/wsl-keepalive-gw-restart"
RESTART_COOLDOWN=60  # 重启冷却时间（秒）
NETWORK_WAS_DOWN=false
CONSECUTIVE_DOWN=0
RESTART_THRESHOLD=3  # 连续失败N次才算"网络断开"，避免抖动误判

mkdir -p "$(dirname "$LOG")"

get_gateway() {
    ip route | awk '/default/ {print $3}' | head -1
}

check_network() {
    local gw=$(get_gateway)
    if [ -z "$gw" ]; then
        return 1
    fi

    # 先 ping 网关
    if ping -c 1 -W 2 "$gw" > /dev/null 2>&1; then
        return 0
    fi

    # 网关不通，试 ping 公网 DNS
    if ping -c 1 -W 2 223.5.5.5 > /dev/null 2>&1; then
        return 0
    fi

    # 再试 114 DNS
    if ping -c 1 -W 2 114.114.114.114 > /dev/null 2>&1; then
        return 0
    fi

    return 1
}

restart_gateway() {
    local now=$(date +%s)
    local lock_time=0

    # 检查冷却期
    if [ -f "$RESTART_LOCK" ]; then
        lock_time=$(cat "$RESTART_LOCK")
        local elapsed=$((now - lock_time))
        if [ "$elapsed" -lt "$RESTART_COOLDOWN" ]; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] SKIP - gateway restart cooldown (${elapsed}s < ${RESTART_COOLDOWN}s)" >> "$LOG"
            return 1
        fi
    fi

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ACTION - network recovered, restarting OpenClaw gateway..." >> "$LOG"
    echo "$now" > "$RESTART_LOCK"

    # 重启 Gateway
    openclaw gateway restart >> "$LOG" 2>&1 &
    # 不阻塞主循环，后台执行

    return 0
}

while true; do
    if check_network; then
        if $NETWORK_WAS_DOWN && [ "$CONSECUTIVE_DOWN" -ge "$RESTART_THRESHOLD" ]; then
            # 网络恢复了！重启 Gateway
            restart_gateway
        fi
        NETWORK_WAS_DOWN=false
        CONSECUTIVE_DOWN=0
    else
        CONSECUTIVE_DOWN=$((CONSECUTIVE_DOWN + 1))
        if [ "$CONSECUTIVE_DOWN" -eq "$RESTART_THRESHOLD" ]; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARN - network down (consecutive failures: $CONSECUTIVE_DOWN)" >> "$LOG"
            NETWORK_WAS_DOWN=true
        elif [ "$CONSECUTIVE_DOWN" -gt "$RESTART_THRESHOLD" ]; then
            # 每30次（~7.5分钟）记一次日志
            if [ $((CONSECUTIVE_DOWN % 30)) -eq 0 ]; then
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] WAIT - still down ($CONSECUTIVE_DOWN consecutive failures)" >> "$LOG"
            fi
        fi
    fi
    sleep 15
done
