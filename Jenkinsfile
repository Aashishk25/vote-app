pipeline {
  agent any

  environment {
    IMAGE_NAME = "vote-app"
    CONTAINER_NAME = "vote-app"
    PORT = "5000"
  }

  stages {
    stage('Checkout') {
      steps {
        git url: 'https://github.com/your-org/vote-app.git', branch: 'main'
      }
    }

    stage('Build Docker Image') {
      steps {
        dir('vote') {
          sh 'docker build -t $IMAGE_NAME .'
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
  }
}
