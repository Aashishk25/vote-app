pipeline {
    agent any

    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch to build')
        string(name: 'IMAGE_TAG', defaultValue: 'latest', description: 'Docker image tag')
    }

    environment {
        ECR_REPO = '594165872407.dkr.ecr.us-east-1.amazonaws.com/vote-app'
        IMAGE_URI = "${ECR_REPO}:${params.IMAGE_TAG}"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: "${params.BRANCH}", url: 'git@github.com:yourusername/vote-app.git'
            }
        }

        stage('Build & Push to ECR') {
            steps {
                sh """
                aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_REPO
                docker build -t vote-app .
                docker tag vote-app:latest $IMAGE_URI
                docker push $IMAGE_URI
                """
            }
        }

        stage('Deploy to App Host') {
            steps {
                sshagent(['app-instance-key']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no root@<app-ip> '
                        docker login -u AWS -p $(aws ecr get-login-password --region us-east-1) $ECR_REPO &&
                        docker stop vote-app || true &&
                        docker rm vote-app || true &&
                        docker pull $IMAGE_URI &&
                        docker run -d --name vote-app -p 80:80 $IMAGE_URI
                    '
                    """
                }
            }
        }
    }
}
