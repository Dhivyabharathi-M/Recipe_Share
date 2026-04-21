import { useEffect, useRef, useCallback } from "react";

const WS_URL = process.env.REACT_APP_WS_URL || "ws://localhost:8000/ws";

export function useWebSocket(onMessage) {
  const wsRef      = useRef(null);
  const retryTimer = useRef(null);

  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(WS_URL);

      ws.onopen    = () => console.log("[WS] connected");
      ws.onmessage = (e) => {
        try { onMessage(JSON.parse(e.data)); }
        catch { /* ignore malformed */ }
      };
      ws.onclose = () => {
        console.log("[WS] closed – retrying in 3s");
        retryTimer.current = setTimeout(connect, 3000);
      };
      ws.onerror = () => ws.close();

      wsRef.current = ws;
    } catch (err) {
      console.warn("[WS] could not connect:", err.message);
      retryTimer.current = setTimeout(connect, 3000);
    }
  }, [onMessage]);

  useEffect(() => {
    connect();
    return () => {
      clearTimeout(retryTimer.current);
      wsRef.current?.close();
    };
  }, [connect]);
}
