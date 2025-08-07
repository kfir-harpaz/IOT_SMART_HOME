// arg: Name Units Place UpdateTime

start "Emulator: PlayRoom Temp" python DHT.py 
timeout 3 
start "Emulator: windows status" python relay.py 
timeout 3
start "Emulator: air quality" python AQS.py 
timeout 3
start "System GUI" python MonitorGUI.py
