# README.md

# Do me!

Dome ...like Done!

To-do List app with ( Flask - MongoDB - Vue.js ) stack, each service containerized and pushed to [docker hub](https://hub.docker.com/u/omarabdul3ziz), And the repo has the configurations to deploy with Kubernetes.

**For Testing:**

- Download the src

    ```bash
    git clone https://github.com/Omarabdul3ziz/dome.git
    cd dome/
    ```

- Start minikube cluster

    ```bash
    minikube start
    ```

- Run the bash script

    It will download the images from public registry

    ```bash
    sh deploy.sh
    ```

- Open your browser and go to [http://do.me/](http://do.me/)