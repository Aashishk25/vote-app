pipeline {
  agent any

  environment {
    APP_NAME = 'vote-app'
    DEPLOY_ENV = 'staging'
  }

  stages {
    stage('Build') {
      steps {
        dir('vote') { // 👈 change this to your actual subfolder name
          echo '🔧 Installing dependencies...'
          sh 'npm install'
        }
      }
    }

    stage('Test') {
      steps {
        dir('vote') {
          echo '🧪 Running tests...'
          sh 'npm test'
        }
      }
    }

    stage('Deploy') {
      steps {
        dir('vote') {
          script {
            if (fileExists('deploy.sh')) {
              echo '🚀 Deploying application...'
              sh './deploy.sh'
            } else {
              echo '⚠️ deploy.sh not found, skipping deploy.'
            }
          }
        }
      }
    }
  }

  post {
    success {
      echo '✅ Build and deploy successful!'
    }
    failure {
      echo '❌ Build failed. Check logs for details.'
    }
  }
}
