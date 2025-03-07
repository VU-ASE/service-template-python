#!/usr/bin/python3
import roverlib
import signal
from loguru import logger
import roverlib.rovercom as rovercom
import time


def run(service : roverlib.Service, configuration : roverlib.ServiceConfiguration):
    if configuration is None:
        return ValueError("Configuration cannot be accessed")
    
    #
    # Access the service indendity, who am I?
    #
    logger.info(f"Hello World, a new service {service.name} was born at version {service.version}")

    #
    # Access the service configuration, to use runtime parameters
    #
    example_num = configuration.GetFloatSafe("number-example")
    logger.info(f"Fetched runtime configuration example number: {example_num}")

    example_string = configuration.GetStringSafe("string-example")
    logger.info(f"Fetched runtime configuration example string: {example_string}")

    example_string_tunable = configuration.GetStringSafe("tunable-string-example")
    logger.info(f"Fetched runtime configuration example tunable sring: {example_string_tunable}")

    #
    # Writing to an output that other services can read (see service.yaml to understand the output name)
    #
    write_stream : roverlib.WriteStream = service.GetWriteStream("example-output")

    # Try to write a simple rovercom message, as if we are sending RPM data
    write_stream.Write(rovercom.SensorOutput(
        sensor_id=404,
        timestamp=int(time.time() * 1000),
        status=0,
        rpm_ouput=rovercom.RpmSensorOutput(
            left_rpm=1000,
            right_rpm=1200,
        )
    ))

    # You don't like using protobuf messages? No problem, you can write raw bytes too
    write_stream.WriteBytes(b"Hello world!")

    # 
    # Reading from an input, to get data from other services (see service.yaml to understand the input name)
    #
    read_stream : roverlib.ReadStream = service.GetReadStream("example-input", "rpm-data")

    # Try to read a simple rovercom message, as if we are receiving RPM data
    pb_data = read_stream.Read()

    # Find out if we actually have rpm data
    if pb_data.rpm_ouput is None:
        logger.error("expected RPM data, but got something else")
    else:
        logger.info(f"Received RPM data: {pb_data.rpm_ouput.left_rpm}, {pb_data.rpm_ouput.right_rpm}")

    # You don't like using protobuf messages? No problem, you can read raw bytes too
    raw_data = read_stream.ReadBytes()
    logger.info(f"Received raw data: {str(raw_data)}")

    #
    # Now do something else fun, see if our "example-string-tunable" is updated
    #
    curr = example_string_tunable
    while True:
        logger.info("Checking for tunable string update")

        # We are not using the safe version here, because using locks is boring
		# (this is perfectly fine if you are constantly polling the value)
		# nb: this is not a blocking call, it will return the last known value
        new_val = configuration.GetString("tunable-string-example")

        if curr is not new_val:
            logger.info(f"Tunable string updated: {curr} -> {new_val}")

        # Don't waste CPU cycles
        time.sleep(1)

def on_terminate(sig : signal):
    logger.info(f"signal: {str(sig)}, Terminating service")

    #
    # ...
    # Any clean up logic here
    # ...
    #

    return None

roverlib.Run(run, on_terminate)