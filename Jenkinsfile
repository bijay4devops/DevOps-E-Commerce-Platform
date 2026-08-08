pipeline {
    agent any

    environment {
        IMAGE_NAME = "devops-ecommerce"
        IMAGE_TAG  = "v1.${BUILD_NUMBER}"

        SONAR_SCANNER = "/opt/sonar-scanner/bin/sonar-scanner"
        SONAR_HOST    = "http://15.252.107.160"
    }

    options {
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm

                sh '''
                    echo "========================================="
                    echo "Jenkins Workspace"
                    echo "========================================="
                    echo "WORKSPACE=$WORKSPACE"
                    pwd
                    ls -la
                '''
            }
        }

        stage('Verify Environment') {
            steps {
                sh '''
                    echo "========================================="
                    echo "Environment"
                    echo "========================================="

                    python3 --version
                    pip3 --version
                    docker --version

                    echo "SonarScanner:"
                    ${SONAR_SCANNER} --version

                    echo "Current user:"
                    whoami

                    echo "Workspace:"
                    pwd
                '''
            }
        }

        stage('Create Python Virtual Environment') {
            steps {
                sh '''
                    rm -rf venv

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
                    pip install pytest pytest-cov
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate

                    pytest tests/ \
                        --cov=app \
                        --cov-report=term-missing \
                        --cov-report=xml:coverage.xml
                '''
            }

            post {
                always {
                    archiveArtifacts(
                        artifacts: 'coverage.xml',
                        allowEmptyArchive: true
                    )
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'sonarqube-token',
                        variable: 'SONAR_TOKEN'
                    )
                ]) {
                    sh '''
                        echo "========================================="
                        echo "SonarQube Analysis"
                        echo "========================================="

                        echo "Workspace: $WORKSPACE"
                        pwd

                        test -f sonar-project.properties
                        test -f coverage.xml

                        ${SONAR_SCANNER} \
                            -Dsonar.host.url="${SONAR_HOST}" \
                            -Dsonar.token="${SONAR_TOKEN}"
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "========================================="
                    echo "Building Docker Image"
                    echo "========================================="

                    docker build \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} \
                        .

                    docker tag \
                        ${IMAGE_NAME}:${IMAGE_TAG} \
                        ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('List Docker Images') {
            steps {
                sh '''
                    docker images ${IMAGE_NAME}
                '''
            }
        }
    }

    post {

        success {
            echo '========================================='
            echo 'PIPELINE SUCCESSFUL'
            echo '========================================='
        }

        failure {
            echo '========================================='
            echo 'PIPELINE FAILED'
            echo '========================================='
        }

        always {
            echo "Cleaning Jenkins workspace..."
            cleanWs()
        }
    }
}


