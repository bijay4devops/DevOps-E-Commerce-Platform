pipeline {
    agent any

    environment {
        IMAGE_NAME = "devops-ecommerce"
        IMAGE_TAG  = "v1.${BUILD_NUMBER}"

    SONAR_HOST_URL    = "http://15.252.107.160"
        SONAR_PROJECT_KEY = "devops-ecommerce-platform"
        SONAR_SCANNER     = "/opt/sonar-scanner/bin/sonar-scanner"
    }

    options {
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Environment') {
            steps {
                sh '''
                    set -e

                    echo "========================================"
                    echo "Environment Verification"
                    echo "========================================"

                    echo "Python:"
                    python3 --version

                    echo "Docker:"
                    docker --version

                    echo "SonarScanner:"
                    ${SONAR_SCANNER} --version

                    echo "Trivy:"
                    trivy --version

                    echo "Repository:"
                    pwd
                    ls -la
                '''
            }
        }

        stage('Create Python Virtual Environment') {
            steps {
                sh '''
                    set -e

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
                    set -e

                    . venv/bin/activate

                    pip install -r requirements.txt

                    pip install pytest-cov
                '''
            }
        }

        stage('Run Tests & Coverage') {
            steps {
                sh '''
                    set -e

                    echo "========================================"
                    echo "Running Tests"
                    echo "========================================"

                    . venv/bin/activate

                    if [ ! -d "tests" ]; then
                        echo "ERROR: tests/ directory does not exist."
                        echo "Repository contents:"
                        find . -maxdepth 2 -type f | sort
                        exit 1
                    fi

                    pytest tests/ \
                        --cov=app \
                        --cov-report=term-missing \
                        --cov-report=xml:coverage.xml \
                        -v
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

        stage('Verify Coverage Report') {
            steps {
                sh '''
                    set -e

                    echo "========================================"
                    echo "Checking coverage.xml"
                    echo "========================================"

                    if [ ! -f coverage.xml ]; then
                        echo "ERROR: coverage.xml was not generated."
                        exit 1
                    fi

                    ls -lh coverage.xml

                    grep -o 'line-rate="[^"]*"' coverage.xml | head
                '''
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
                        set -e

                        echo "========================================"
                        echo "SonarQube Analysis"
                        echo "========================================"

                        echo "SonarQube URL: ${SONAR_HOST_URL}"
                        echo "Project Key: ${SONAR_PROJECT_KEY}"

                        ${SONAR_SCANNER} \
                            -Dsonar.host.url="${SONAR_HOST_URL}" \
                            -Dsonar.projectKey="${SONAR_PROJECT_KEY}" \
                            -Dsonar.projectName="DevOps E-Commerce Platform" \
                            -Dsonar.sources=app \
                            -Dsonar.tests=tests \
                            -Dsonar.python.coverage.reportPaths=coverage.xml \
                            -Dsonar.token="${SONAR_TOKEN}"
                    '''
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    set -e

                    echo "========================================"
                    echo "Building Docker Image"
                    echo "========================================"

                    docker build \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} \
                        -t ${IMAGE_NAME}:latest \
                        .
                '''
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh '''
                    set -e

                    echo "========================================"
                    echo "Trivy Security Scan"
                    echo "========================================"

                    trivy image \
                        --severity HIGH,CRITICAL \
                        --exit-code 1 \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('List Docker Images') {
            steps {
                sh '''
                    docker images
                '''
            }
        }
    }

    post {
        success {
            echo """
=========================================
 Jenkins Pipeline SUCCESS
=========================================
Docker Image: ${IMAGE_NAME}:${IMAGE_TAG}
SonarQube Project: ${SONAR_PROJECT_KEY}
"""
        }

        failure {
            echo """
=========================================
 Jenkins Pipeline FAILED
=========================================
Check the stage that failed above.
"""
        }

        always {
            cleanWs()
        }
    }
}


