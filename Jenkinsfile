pipeline {
    environment {
        registry = "boressan/o3skim"
        registryCredential = 'dockerhub_id'
    }
    agent any
    stages {
        stage('Image build') {
            steps {
                echo '====================building image===================================='
                script { customImage = docker.build(registry) }
            }
        }
        stage('Unit testing') {
            steps {
                echo '====================executing unittest================================'
                script { customImage.inside("--entrypoint=''") {sh 'tox'} }
            }
        }
        stage('Docker-hub upload') {
            steps {
                echo '====================uploading docker-hub=============================='
                script { docker.withRegistry('', registryCredential) { customImage.push() } }
            }
        }
    }
}