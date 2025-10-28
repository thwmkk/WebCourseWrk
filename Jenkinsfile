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
                            echo "Build for backend ..."
                            bat """
                                echo "=== Creating conda environment ==="
                                conda env create -f environment.yml

                                echo "=== Running makemigrations ==="
                                conda run -n ${env.CONDA_ENV_NAME} python manage.py makemigrations

                                echo "=== Running migrate ==="
                                conda run -n ${env.CONDA_ENV_NAME} python manage.py migrate

                                echo "=== Checking migration status ==="
                                conda run -n ${env.CONDA_ENV_NAME} python manage.py showmigrations
                            """
                        }
                    }
                    stage('Frontend') {
                        steps {
                            echo "Build for frontend ..."
                            bat '''
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
                }
            }
            stage('Deploy') {
                parallel {
                    stage('Backend') {
                        steps {
                            echo 'Deploy for backend ...'
                            // bat "conda run -n ${env.CONDA_ENV_NAME} python manage.py runserver"
                        }
                    }
                    stage('Frontend') {
                        steps {
                            echo 'Deploy for frontend ...'
                            // bat 'cd client && npm run dev'
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