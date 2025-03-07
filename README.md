# service-template-python
This template serves as a starting point for writing a service in python. It uses [roverlib](https://pypi.org/project/roverlib/) to make setting up communication with other services easier.

This example service acts like a "controller" so it takes as input data from [imaging](https://github.com/VU-ASE/imaging) and outputs data for the [actuator](https://github.com/VU-ASE/actuator). For simplicity, it does nothing with the image data, but simply starts driving in a snake pattern. For details, take a look at [`src/main.py`](./src/main.py).

## Uploading

After changing the name, author and version in the [service.yaml](./service.yaml) you can use the following command to upload the service to the rover (in this case to Rover 5):

``` bash
roverctl -r 5 upload .
```

For more fast-paced development you can add `-w` which will watch for changes and automatically upload them.

``` bash
roverctl -r 5 upload . -w
```

## Running a Pipeline
To run this in a pipeline, open the web interface with `roverctl -r 5` and make sure you enable the dependencies that this service requires, namely `vu-ase/imaging` and `vu-ase/actuator`.

