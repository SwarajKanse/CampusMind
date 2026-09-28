pipeline {
    agent any

    environment {
        GROQ_MODEL = 'qwen/qwen3.8-27b'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend Quality Gate') {
            steps {
                dir('backend') {
                    sh 'python -m pip install -r requirements.txt'
                    sh 'python -c "from main import app; print(\'Backend validated\')"'
                }
            }
        }

        stage('Frontend Build') {
            steps {
                dir('frontend') {
                    sh 'npm ci'
                    sh 'npm run build'
                }
            }
        }

        stage('Docker Compose Validation') {
            steps {
                dir('devops') {
                    sh 'docker compose config'
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
