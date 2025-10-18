pipeline {
  agent any

  environment {
    IMAGE_NAME = "vote-app"
    CONTAINER_NAME = "vote-app"
    PORT = "5000"
  }

  stages {
    stage('Build Docker Image') {
      options {
        timeout(time: 10, unit: 'MINUTES')
      }
      steps {
        dir('vote') {
          sh 'docker build --network=host -t $IMAGE_NAME .'
        }
      }
    }

    stage('Deploy Container') {
      steps {
        sh '''
          docker rm -f $CONTAINER_NAME || true
          docker run -d --name $CONTAINER_NAME -p $PORT:80 $IMAGE_NAME
        '''
      }
    }

    stage('Health Check') {
      steps {
        sh 'curl -f http://localhost:$PORT || exit 1'
      }
    }
  }
}
