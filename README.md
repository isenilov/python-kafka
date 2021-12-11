# Schemaful Kafka streaming with Python and AVRO

## Running

Running all the services:
`docker-compose -f docker-compose.yaml up --build -d`

Attaching to the app's logs:
`docker-compose logs worker -f`

### Compiling AVRO into Python classes

Compiling AVRO schema `./avro/Messgae.avsc` into Python classes
is done during building docker image, that is why some imports
in the `__main__.py` can be unreachable. However, it is possible to
generate those classes with the [`avro-to-python`](https://pypi.org/project/avro-to-python/)
tool:
```shell
pip install avro_to_python==0.3.2

avro_to_python ./avro . 
# alternative command: `python -m avro_to_python.cli ./avro .`
```
This will result in the `protocol` Python package generated which will contain
the `Message` and `Data` classes.