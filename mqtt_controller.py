import paho.mqtt.client as mqtt
import time

class MQTTController:
    def __init__(self, broker_address="localhost", port=1883):
        self.broker_address = broker_address
        self.port = port
        self.client = mqtt.Client("SmartRoomPi")
        
        # MQTT 토픽
        self.topic_control = "smartroom/control"
        self.topic_status = "smartroom/status"
        
        # 디바이스 상태 (ESP32로부터 업데이트됨)
        self.light_on = False
        self.door_open = False
        self.music_playing = False
        
        # 콜백 설정
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        # 연결
        try:
            self.client.connect(self.broker_address, self.port, 60)
            self.client.loop_start()
            print(f"✅ MQTT connected to {self.broker_address}:{self.port}")
        except Exception as e:
            print(f"❌ MQTT connection failed: {e}")
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("📡 MQTT broker connected!")
            # 상태 토픽 구독
            self.client.subscribe(self.topic_status)
        else:
            print(f"❌ Connection failed with code {rc}")
    
    def on_message(self, client, userdata, msg):
        """ESP32로부터 상태 업데이트 수신"""
        message = msg.payload.decode()
        print(f"📩 Received: {message}")
        
        # 상태 업데이트
        if "LIGHT:" in message:
            self.light_on = message.split(":")[1] == "1"
        elif "DOOR:" in message:
            self.door_open = message.split(":")[1] == "1"
        elif "MUSIC:" in message:
            self.music_playing = message.split(":")[1] == "1"
    
    def send_command(self, command):
        """ESP32에 명령 전송"""
        self.client.publish(self.topic_control, command)
        print(f"📤 Sent: {command}")
    
    def toggle_light(self, turn_on):
        """조명 제어"""
        command = "LIGHT_ON" if turn_on else "LIGHT_OFF"
        self.send_command(command)
        status = "ON" if turn_on else "OFF"
        print(f"💡 Light: {status}")
        return status
    
    def open_door(self):
        """문 열기"""
        self.send_command("DOOR_OPEN")
        print(f"🚪 Door: OPEN")
        return "OPEN"
    
    def close_door(self):
        """문 닫기"""
        self.send_command("DOOR_CLOSE")
        print(f"🚪 Door: CLOSED")
        return "CLOSED"
    
    def play_music(self):
        """음악 재생"""
        self.send_command("MUSIC_PLAY")
        print(f"🎵 Music: PLAYING")
        return "PLAYING"
    
    def stop_music(self):
        """음악 정지"""
        self.send_command("MUSIC_STOP")
        print(f"🎵 Music: STOPPED")
        return "STOPPED"
    
    def get_status(self):
        """현재 상태 반환"""
        return {
            "light": {"on": self.light_on},
            "door": {"open": self.door_open},
            "music": {"playing": self.music_playing}
        }
    
    def close(self):
        """연결 종료"""
        self.client.loop_stop()
        self.client.disconnect()
        print("👋 MQTT disconnected")