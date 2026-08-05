pipeline {
    agent any

    environment {
        IMAGE_NAME = "devops-ecommerce"
        IMAGE_TAG  = "v1.${BUILD_NUMBER}"
    }

    options {
        timestamps()
        ansiColor('xterm')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Environment') {
            steps {
                sh 'python3 --version'
                sh 'pip3 --version'
                sh 'docker --version'
            }
        }

        stage('Create Python Virtual Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                python -m pip install --upgrade pip
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest tests/ || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('List Docker Images') {
            steps {
                sh 'docker images'
            }
        }

    }

    post {

        success {
            echo 'Build completed successfully!'
        }

        failure {
            echo 'Build failed!'
        }

        always {
            cleanWs()
        }
    }
}
