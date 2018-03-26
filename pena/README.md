## PENA tool
A lightweight tool to detect plugins conflicts on a WordPress environment.

### Requirements
1. [Docker](https://www.docker.com/get-docker)

### Running PENA container
1. Open the terminal and download [PENA](https://github.com/pag-tools/pena/tree/master/pena) project: `$ wget https://github.com/pag-tools/pena/blob/master/pena/dist/pena.zip` or [click here](https://github.com/pag-tools/pena/blob/master/pena/dist/pena.zip) to download the zip file.
2. Extract it and run: `$ cd pena && docker build -t pena .`
3. To run the container use: `$ docker run --name pena --rm -it -p 80:80 pena`

The time-consuming to build, install, download all plugins and configure the environment depends of your internet connection.

### Running Experiments
This steps will be executed on container, you can define an alias: 
- `$ alias pena_cmd="docker exec -i -t pena sudo -E -u www-data $1"`

All runners are inside `experiment` folder, to run each of them:
- Efficiency Experiment: `$ pena_cmd ./experiments/efficiency.sh`
- Accuracy Experiment: `$ pena_cmd ./experiments/accuracy.sh`
- Conflicts on Wordpress Experiment: `$ pena_cmd ./experiments/wp_experiment.sh`

* To run all of them, use: `$ pena_cmd ./experiments/all_experiment.sh`

The logs are stored on each experiment folder, you can check after each execution:
- Efficiency Experiment: `$ pena_cmd ./experiments/efficiency/logs/efficiency.log`
- Accuracy Experiment: `$ pena_cmd ./experiments/accuracy/logs/accuracy.log`
- Conflicts on Wordpress Experiment: `$ pena_cmd ./experiments/wp_experiment/logs/wp_experiment.log`

#### To check logs and conflicts found in our experiment, check the [artifacts page](https://github.com/pag-tools/pena/tree/master/pena).

### Removing PENA
1. Get PENA CONTAINER_ID: `$ docker ps | grep pena`
2. Stop PENA container and remove image: `$ docker stop PENA_ID && docker rmi PENA_ID`
