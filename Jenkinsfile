pipeline {
  agent any

  environment {
    IMAGE_NAME = "vote-app"
    ECR_REPO = "594165872407.dkr.ecr.us-east-1.amazonaws.com/vote-app"
    CONTAINER_NAME = "vote-app"
    PORT = "5000"
    APP_HOST = "ip-10-101-3-153"
    AWS_REGION = "us-east-1"
  }

  stages {
    stage('Build Docker Image') {
      steps {
        dir('vote') {
          sh 'docker build --network=host -t $IMAGE_NAME .'
        }
      }
    }

    stage('Tag and Push to ECR') {
      steps {
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
          sh '''
            aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO
            docker tag $IMAGE_NAME $ECR_REPO:latest
            docker push $ECR_REPO:latest
          '''
        }
      }
    }

    stage('Deploy to App Host') {
      steps {
        sshagent(credentials: ['app-host-key']) {
          sh '''
            ssh -o StrictHostKeyChecking=no ubuntu@$APP_HOST '
              aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO &&
              docker rm -f $CONTAINER_NAME || true &&
              docker pull $ECR_REPO:latest &&
              docker run -d --name $CONTAINER_NAME -p $PORT:80 $ECR_REPO:latest
            '
          '''
        }
      }
    }
  }
}
