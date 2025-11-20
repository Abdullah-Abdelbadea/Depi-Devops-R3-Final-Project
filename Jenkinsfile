def gv //Declare the global variable for use across stages
pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = "eu-north-1"
        ECR_REPO = "923816247512.dkr.ecr.eu-north-1.amazonaws.com/depi-devops-project"
        IMAGE_TAG = "latest"

        CLUSTER = "depi-devops-cluster"
        SERVICE = "depi-devops-task-service-6msvmsc3"
    }

    stages {

        // stage('Checkout') {
        //     steps {
        //         git 'https://github.com/Abdullah-Abdelbadea/Depi-Devops-R3-Final-Project.git'
        //     }
        // }

        stage('Load Functions') {
            steps {
                script {
                    echo "testing Loading"
                    gv = load 'script.groovy'
                }
            }
        }

        stage('AWS Login to ECR') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'aws-creds',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {
                    script {
                        sh """
                        echo "Testing before export" 
                        export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
                        export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
                        echo "Testing after export"
                        """

                        gv.awsLogin(ECR_REPO, AWS_DEFAULT_REGION)
                    }
                }
            }
        }

        stage('Build Image') {
            steps {
                script {
                    echo "Testing build"
                    gv.buildImage(ECR_REPO, IMAGE_TAG)
                }
            }
        }

        stage('Push Image') {
            steps {
                script {
                    echo "Testing Push"
                    gv.pushImage(ECR_REPO, IMAGE_TAG)
                }
            }
        }

        stage('Deploy to ECS') {
            steps {
                script {
                    echo "Testing Deploy"
                    gv.deployToEcs(CLUSTER, SERVICE, AWS_DEFAULT_REGION)
                }
            }
        }
    }
}
