    pipeline {
        agent any

        triggers {
            pollSCM('* * * * *')
        }


        environment {
            CONDA_ENV_NAME = 'web-eva'
        }

        stages {
            stage('Build') {
                parallel {
                    stage('Backend') {
                        steps {
                            echo "Build for backend on ${env.BRANCH_NAME} ..."
                            sh """
                                conda env create -f environment.yml
                                conda run -n ${env.CONDA_ENV_NAME} python manage.py makemigrations
                                conda run -n ${env.CONDA_ENV_NAME} python manage.py migrate
                            """
                        }
                    }
                    stage('Frontend') {
                        steps {
                            echo "Build for frontend on ${env.BRANCH_NAME} ..."
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