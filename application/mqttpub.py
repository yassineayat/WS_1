# import paho.mqtt.client as mqtt
#
# client = mqtt.Client()
# client.username_pw_set("user","user") # authentification
# #client.connect("broker.hivemq.com",1883,60) #connect with EC2 instance on port 8883
# #client.connect("192.168.43.112", 1883, 60)
# client.connect("mqtt.eclipseprojects.io", 1883, 60)
# msg = input("Enter your message:")
# client.publish("message", msg); # publish the message typed by the user
# #client.disconnect(); #disconnect from server