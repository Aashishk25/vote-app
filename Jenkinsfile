pipeline {
  agent any

  stages {
    stage('Build & Deploy') {
      steps {
        sh 'docker-compose up -d --build'
      }
    }
  }

  post {
    success {
      echo '✅ Full stack deployed via Docker Compose!'
    }
    failure {
      echo '❌ Deployment failed. Check logs.'
    }
  }
}
