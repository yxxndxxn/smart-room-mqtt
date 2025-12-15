from mqtt_controller import MQTTController
from analytics import GestureAnalytics

class DeviceController:
    def __init__(self, use_mqtt=True):
        """
        use_mqtt=True: MQTT 사용 (ESP32)
        use_mqtt=False: 시리얼 통신 사용 (아두이노)
        """
        self.use_mqtt = use_mqtt
        
        if use_mqtt:
            # MQTT 방식 (ESP32)
            self.controller = MQTTController()
        else:
            # 시리얼 방식 (아두이노) - 기존 코드
            from arduino_controller import ArduinoController
            self.controller = ArduinoController(arduino_port)
        
        self.analytics = GestureAnalytics()
    
    def toggle_light(self, turn_on):
        """조명 ON/OFF"""
        status = self.controller.toggle_light(turn_on)
        
        # 로깅
        gesture = "FIST" if not turn_on else "PALM"
        self.analytics.log_gesture(gesture, "LIGHT", status)
        
        return status
    
    def open_door(self):
        """문 열기"""
        status = self.controller.open_door()
        self.analytics.log_gesture("ONE_FINGER", "DOOR", "OPEN")
        return status
    
    def close_door(self):
        """문 닫기"""
        status = self.controller.close_door()
        self.analytics.log_gesture("PEACE", "DOOR", "CLOSED")
        return status
    
    def play_music(self):
        """음악 재생"""
        status = self.controller.play_music()
        self.analytics.log_gesture("THREE_FINGERS", "MUSIC", "PLAY")
        return status
    
    def stop_music(self):
        """음악 정지"""
        status = self.controller.stop_music()
        self.analytics.log_gesture("FOUR_FINGERS", "MUSIC", "STOP")
        return status
    
    def get_status(self):
        """현재 상태 반환"""
        return self.controller.get_status()
    
    def get_analytics(self):
        """분석 데이터 반환"""
        return self.analytics.get_statistics()
    
    def close(self):
        self.controller.close()