## PENA tool
A lightweight tool to detect plugins conflicts on a WordPress environment

### Requirements
1. [Docker](https://www.docker.com/get-docker)

### Installation
1. Download [PENA project]() and extract it on your local environment.
2. Go to PENA folder and build PENA container: `$ cd pena/ && docker build -t pena</code>`

### Running experiments
1. Run PENA container: `$ docker run -it -v $(pwd)/pena:/pena -p 8081:8081 --rm pena bash`
2. Go to `$ cd PENA/experiments`
3. Run the scripts:
    - `$ ./efficiency-single-conflicts.sh`
    - `$ ./efficiency-multiple-conflicts.sh`
    - `$ ./accuracy-precision.sh`
    - `$ ./accuracy-recall.sh`
    - `$ ./wordpress-conflicts.sh`

### [Conflicts found](https://github.com/pag-tools/pena/tree/master/pena/conflicts) by PENA
