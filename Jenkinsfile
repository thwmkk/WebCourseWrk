pipeline {
    agent any    
    
    stages {
        stage('Build') {
            steps {
                echo "Building images"
                sh 'docker compose down'
                sh 'docker compose build'
            }
        }
        stage('Test') {
            steps {
                echo "Running tests ..."
                dir('server') {
                    sh '''
                        docker compose run --rm backend \
                        poetry run python manage.py test characters.tests
                    '''
                }
            }
        }
        stage('Deploy') {
            when { 
                branch 'main'
            }
            steps {
            echo "Docker compose deploy"
                sh '''
                    docker compose down 
                    docker compose up -d
                '''
            }
        }
    }

    post {
        always {
             echo "Pipeline finished"
        }
        success {
            echo "Pipeline success"
        }
        failure {
            echo "Pipeline failure"
        }
        aborted {
            echo "Pipeline aborted"
        }
    }
}
