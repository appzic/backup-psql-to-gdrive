pipeline {
    environment {
        IMAGE_NAME = 'appzic/backup-psql-to-gdrive'
        DOCKERHUB_CREDENTIALS = credentials('APPZIC_DOCKERHUB_CREDENTIALS')
        VERSION = '1.0.0'
    }
    agent any
    stages {
        stage("Build Docker Image") {
            steps {
                script {
                    sh 'docker build -t $IMAGE_NAME:$VERSION .'
                }
            }
            post {
                always {
                    echo "🛠️  The build stage has completed, regardless of the outcome."
                }
                success {
                    echo "✅ Hooray! The Docker image was built successfully!"
                }
                failure {
                    echo "❌ Oops! There was an issue while building the Docker image. Please check the logs."
                }
            }
        }
        stage("Push to Docker Hub") {
            steps {
                script {
                    sh '''
                    echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                    docker push $IMAGE_NAME:$VERSION
                    docker logout
                    '''
                }
            }
            post {
                always {
                    echo "🔄 The image push step has finished, regardless of the result."
                }
                success {
                    echo "🚀 Image pushed to Docker Hub successfully!"
                }
                failure {
                    echo "⚠️ Something went wrong while pushing the image. Please review the logs."
                }
            }
        }
    }
    post {
        always {
            echo "🔄 The pipeline has finished, regardless of the final result."
            cleanWs()
        }
        success {
            echo "🎉 Congratulations! The pipeline executed successfully from start to finish."
        }
        failure {
            echo "🚨 Uh-oh! The pipeline failed. Please investigate the errors and try again."
        }
    }
}