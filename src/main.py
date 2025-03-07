#!/usr/bin/python3

import time
import signal
from loguru import logger
import roverlib
import roverlib.rovercom as rovercom

# 
def run(service : roverlib.Service, configuration : roverlib.ServiceConfiguration):
    if configuration is None:
        return ValueError("Configuration cannot be accessed")
    
    # Access the to the identity of this service, who am I?
    logger.info(f"Hello World, a new service {service.name} was born at version {service.version}")

    # Access the service configuration found in service.yaml, to use runtime parameters
    example_num = configuration.GetFloatSafe("number-example")
    example_string = configuration.GetStringSafe("string-example")
    example_string_tunable = configuration.GetStringSafe("tunable-string-example")
    logger.info(f"Fetched runtime configuration examples: ")
    logger.info(f"number: {example_num}")
    logger.info(f"string: {example_string}")
    logger.info(f"tunable string: {example_string_tunable}")



    # This service will be reading the "path" data from the imaging service
    # and it will publish "decision" data to anyone who subscribes.
    # We initialize the streams as follows:
    image_stream : roverlib.ReadStream = service.GetReadStream("imaging", "path")
    actuator_stream : roverlib.WriteStream = service.GetWriteStream("decision")

    # Main processing loop
    while True:
        # --------------------------------
        # Reading data from other services
        # --------------------------------
        # Then read a message from imaging. Typically, the next line will be at the start of your loop
        image_data = image_stream.Read()
        if image_data.camera_output is None:
            logger.error("image data was not camera output")
            exit(1)
        
        # For more information on what available messages are published, check the rovercom
        # definition https://github.com/VU-ASE/roverlib-python/blob/main/src/roverlib/rovercom.py
        width = image_data.camera_output.trajectory.width
        height = image_data.camera_output.trajectory.height
        logger.info(f"Received an image of {width} x {height} pixels")

        for point in image_data.camera_output.trajectory.points:
            logger.info(f"imaging produced a point: {point}")

        # -------------------------
        # Writing to other services
        # -------------------------

        time.sleep(1)

        actuator_stream.Write(rovercom.SensorOutput(
            sensor_id=2,
            timestamp=int(time.time() * 1000),
            controller_output=rovercom.ControllerOutput(
                steering_angle = -0.4,
                left_throttle = 0.12,
                right_throttle = 0.12,
            )
        ))

        time.sleep(1)

        actuator_stream.Write(rovercom.SensorOutput(
            sensor_id=2,
            timestamp=int(time.time() * 1000),
            controller_output=rovercom.ControllerOutput(
                steering_angle = 0.4,
                left_throttle = 0.12,
                right_throttle = 0.12,
            )
        ))


# This function gets called when the pipeline gets terminated. This can happen if any other service
# in the pipeline crashes or if the pipeline is stopped via the the web interface.
def on_terminate(sig : signal):
    logger.info(f"signal: {str(sig)}, Terminating service")

    #
    # ...
    # If you need to add clean up logic, add it here
    # ...
    #

    return None

if __name__ == "__main__":
    roverlib.Run(run, on_terminate)
