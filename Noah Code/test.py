from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True)


print(vehicle.location.global_frame)
vehicle.mode = VehicleMode("GUIDED")
vehicle.armed = True

a_location = LocationGlobalRelative(-50, 50, 30)
vehicle.simple_goto(a_location)

print(vehicle.location.global_frame)
