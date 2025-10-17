pipeline {
    agent {
        docker {
            image 'python:3.9-slim'
            args '-u root'
        }
    }

    environment {
        PYTHON_VERSION = '3.9'
        PROJECT_NAME = 'fastapi-app'
        GITHUB_REPO = 'https://github.com/developerxmedia/fastapi.git'
        BRANCH_NAME = "${env.BRANCH_NAME ?: 'master'}"
    }

    parameters {
        choice(name: 'DEPLOYMENT_TARGET', choices: ['staging', 'production'], description: 'Deployment environment')
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '5'))
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: "${BRANCH_NAME}", 
                    url: "${GITHUB_REPO}", 
                    credentialsId: 'github-credentials'
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Code Quality') {
            parallel {
                stage('Lint') {
                    steps {
                        sh '''
                            . venv/bin/activate
                            pip install flake8
                            flake8 .
                        '''
                    }
                }
                stage('Security Scan') {
                    steps {
                        sh '''
                            . venv/bin/activate
                            pip install bandit
                            bandit -r .
                        '''
                    }
                }
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install pytest
                    pytest tests/
                '''
            }
            post {
                always {
                    junit 'test-reports/*.xml'
                }
            }
        }

        stage('Build') {
            steps {
                sh '''
                    . venv/bin/activate
                    python3 setup.py sdist bdist_wheel
                '''
            }
        }

        stage('Deploy') {
            when {
                expression { params.DEPLOYMENT_TARGET == 'production' && env.BRANCH_NAME == 'master' }
            }
            steps {
                script {
                    if (params.DEPLOYMENT_TARGET == 'production') {
                        sh '''
                            pip install -U pip
                            pip install gunicorn
                            gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
                        '''
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
            slackSend channel: '#deployments', 
                      message: "Build ${env.JOB_NAME} ${env.BUILD_NUMBER} succeeded"
        }
        failure {
            echo 'Pipeline failed!'
            slackSend channel: '#alerts', 
                      color: 'danger', 
                      message: "Build ${env.JOB_NAME} ${env.BUILD_NUMBER} failed"
        }
        cleanup {
            sh 'rm -rf venv dist build *.egg-info'
            deleteDir()
        }
    }
}