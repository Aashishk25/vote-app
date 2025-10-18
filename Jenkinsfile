pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        git url: 'https://github.com/Aashishk25/vote-app.git', branch: 'main'
      }
    }

    stage('Build') {
      steps {
        sh 'npm install'
      }
    }

    stage('Test') {
      steps {
        sh 'npm test'
      }
    }

    stage('Deploy') {
      steps {
        sh './deploy.sh'
      }
    }
  }

  post {
    success {
      echo '✅ Build and deploy successful!'
    }
    failure {
      echo '❌ Build failed. Check logs.'
    }
  }
}
