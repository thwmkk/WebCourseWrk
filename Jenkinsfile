pipeline {
    agent any

    environment {
        CONDA_ENV_NAME = 'web-eva'
    }

    stages {
        stage('Branch Validation') {
            steps {
                script {
                    echo "Current branch: ${env.BRANCH_NAME}"

                    if (env.BRANCH_NAME != 'main') {
                        currentBuild.result = 'ABORTED'
                        error("Pipeline aborted: only main branch is allowed to build")
                    }
                    
                    echo "Building for ${env.BRANCH_NAME} branch ..."
                }
            }
        }
        stage('Checkout') {
            steps {
                git branch: "${env.BRANCH_NAME}",
                    url: 'https://github.com/thwmkk/WebCourseWrk.git',
                    credentialsId: 'github-token'
            }
        }
        stage('Build') {
            parallel {
                stage('Backend') {
                    steps {
                        echo 'Build for backend ...'
                        sh """
                            conda env create -f environment.yml
                            conda run -n ${env.CONDA_ENV_NAME} python manage.py makemigrations
                            conda run -n ${env.CONDA_ENV_NAME} python manage.py migrate
                        """
                    }
                }
                stage('Frontend') {
                    steps {
                        echo 'Build for frontend ...'
                        sh '''
                            cd client
                            npm install
                        '''
                    }
                }
            }
        }
        stage('Testing') {
            steps {
                echo 'Testing...'
                script {
                    Thread.sleep(5000)
                }
            }
        }
        stage('Deploy') {
            parallel {
                stage('Backend') {
                    steps {
                        echo 'Deploy for backend ...'
                        // sh "conda run -n ${env.CONDA_ENV_NAME} python manage.py runserver"
                    }
                }
                stage('Frontend') {
                    steps {
                        echo 'Deploy for frontend ...'
                        // sh 'cd client && npm run dev'
                    }
                }
            }
        }
    }

    // постусловия
    post {
        always {
            echo "Pipiline finished for ${env.BRANCH_NAME}"
        }
        success {
            echo "Pipiline success for ${env.BRANCH_NAME}"
        }
        failure {
            echo "Pipiline failure for ${env.BRANCH_NAME}"
        }
        aborted {
            echo "Pipeline aborted for ${env.BRANCH_NAME}"
        }
    }
}