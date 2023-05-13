# EC-ConnectedCars

## Edge Devices ( Vehicles or any) 
- Install aws-iot-device-sdk-python-v2 on device (Refer https://docs.aws.amazon.com/iot/latest/developerguide/using-laptop-as-device.html) 

## Edge Gateway 
- Install AWS Green Grass Core Device (Refer https://docs.aws.amazon.com/greengrass/v2/developerguide/install-greengrass-core-v2.html) 
- Associate Client devices (Refer https://docs.aws.amazon.com/greengrass/v2/developerguide/associate-client-devices.html)  
- Verify Client devices are able to communicate with Green Grass Core (Refer https://docs.aws.amazon.com/greengrass/v2/developerguide/connect-client-devices.html) 
- For Custom Components refer - https://docs.aws.amazon.com/greengrass/v2/developerguide/develop-greengrass-components.html 
- Recepie and code for VehicleHealthMonitoring and VehicleSituationHandler components is present in package ggEdgeGateway/GreenGrass-RSU-001 
- To deploy components use  
     .\greengrass-cli deployment create --recipeDir C:\workspace\GreenGrass-RSU-001\recipes --artifactDir C:\workspace\GreenGrass-RSU-001\artifacts --merge "org.bits.ec.VehicleHealthMonitoring=1.0.0" 
	 
	 .\greengrass-cli deployment create --recipeDir C:\workspace\GreenGrass-RSU-001\recipes --artifactDir C:\workspace\GreenGrass-RSU-001\artifacts --merge "org.bits.ec.VehicleSituationAwareness=1.0.0" 
	 
	** Note - change path as per need. 
- To restart components use - 
    .\greengrass-cli component restart -n="org.bits.ec.VehicleHealthMonitoring" 
	.\greengrass-cli component restart -n="org.bits.ec.VehicleSituationAwareness" 
	
## To Test various use case from device use below python scripts (scripts located in package edgeDevice)- 
- Device to Cloud (For vehicle health monitoring)
  python vehicle_health.py --topic device/car1/health --ca_file %USERPROFILE%\client-device-cert\Amazon-root-CA-1.pem --cert %USERPROFILE%\client-device-cert\device.pem.crt --key %USERPROFILE%\client-device-cert\private.pem.key --endpoint azqhb3vhjca36-ats.iot.us-east-1.amazonaws.com 
- Device to Edge gateway  
  (For Vehicle Health Monitoring)  
  
  python vehicle_health_edge_pub.py --thing_name Car1 --topic device/Car1/health --message "Car Health status" --ca_file %USERPROFILE%\client-device-cert\Amazon-root-CA-1.pem  --cert %USERPROFILE%\client-device-cert\device.pem.crt --key %USERPROFILE%\client-device-cert\private.pem.key --region us-east-1 --verbosity Warn --max_pub_ops 20  
  
  (For Vehicle Situation Alert)  
  
  python vehicle_alert.py --thing_name Car1 --topic device/Car1/alerts/situation --message "Situation Message" --ca_file %USERPROFILE%\client-device-cert\Amazon-root-CA-1.pem  --cert %USERPROFILE%\client-device-cert\device.pem.crt --key %USERPROFILE%\client-device-cert\private.pem.key --region us-east-1 --verbosity Warn --max_pub_ops 12  
