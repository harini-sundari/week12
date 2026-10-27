
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'harinisundari/devops_week12:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python3 -m pytest tests/ -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t "$DOCKER_IMAGE" .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds-global',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_TOKEN'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_TOKEN" |
                            docker login -u "$DOCKER_USER" --password-stdin
                        docker push "$DOCKER_IMAGE"
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f deployment.yaml'
                sh 'kubectl apply -f service.yaml'
                sh 'kubectl rollout status deployment/week12-deployment --timeout=120s'
            }
        }
    }

    post {
        success {
            echo 'Week 12 pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check Console Output for the error.'
        }
    }
}
