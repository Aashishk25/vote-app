pipeline {
  agent any

  environment {
    IMAGE_NAME = '594165872407.dkr.ecr.us-east-1.amazonaws.com/vote-app:latest'
    CONTAINER_NAME = 'vote-app'
    APP_HOST = 'ubuntu@10.101.3.153'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        dir('vote') {
          sh 'docker build --network=host -t $IMAGE_NAME .'
        }
      }
    }

    stage('Login to AWS ECR') {
      steps {
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
          sh '''
            aws ecr get-login-password --region us-east-1 | \
            docker login --username AWS --password-stdin 594165872407.dkr.ecr.us-east-1.amazonaws.com
          '''
        }
      }
    }

    stage('Push to ECR') {
      steps {
        sh 'docker push $IMAGE_NAME'
      }
    }

    stage('Deploy to App Host') {
  steps {
    sshagent(credentials: ['app-host-key']) {
      sh """
        ssh -o StrictHostKeyChecking=no $APP_HOST '
          docker pull $IMAGE_NAME &&
          docker stop $CONTAINER_NAME || true &&
          docker rm $CONTAINER_NAME || true &&
          docker run -d --name $CONTAINER_NAME -p 80:80 $IMAGE_NAME gunicorn app:application -b 0.0.0.0:80
        '
      """
       }
      }
    }
  }
}

