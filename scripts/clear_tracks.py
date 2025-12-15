
import socket
import json
import time

PORT = 9877

def main():
    print("🧹 Clearing Ableton Tracks...")

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        sock.connect(('localhost', PORT))
    except Exception as e:
        print(f"❌ Could not connect to Ableton: {e}")
        return

    def send(cmd, params=None):
        msg = {"type": cmd, "params": params or {}}
        sock.sendall(json.dumps(msg).encode('utf-8'))
        # Simple receive (not robust for large data but fine for status)
        data = sock.recv(8192)
        return json.loads(data.decode('utf-8'))

    # 1. Get Session Info
    res = send("get_session_info")
    if res.get("status") != "success":
        print("❌ Failed to get session info")
        return

    tracks = res["result"]["track_count"]
    print(f"found {tracks} tracks.")

    # 2. Iterate backwards from the last track down to the second track (index 1)
    #    Ableton requires at least one track to remain.
    deleted = 0
    # Start at last index (tracks-1), stop before 0 (at 1), step -1
    for i in range(tracks - 1, 0, -1):
        print(f"  Deleting track {i}...")
        res = send("delete_track", {"track_index": i})
        if res.get("status") == "success":
            deleted += 1
            time.sleep(0.05)
        else:
            print(f"  ❌ Failed: {res.get('message')}")

    print(f"✅ Cleared {deleted} tracks. (1 track remains)")
    sock.close()

if __name__ == "__main__":
    main()
