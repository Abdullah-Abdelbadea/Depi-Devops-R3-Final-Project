def gv
pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = "eu-north-1"

        ECR_WEB           = "923816247512.dkr.ecr.eu-north-1.amazonaws.com/depi-devops-project"
        ECR_PROMETHEUS    = "923816247512.dkr.ecr.eu-north-1.amazonaws.com/depi-prometheus"
        ECR_ALERTMANAGER  = "923816247512.dkr.ecr.eu-north-1.amazonaws.com/depi-alertmanager"
        ECR_GRAFANA       = "923816247512.dkr.ecr.eu-north-1.amazonaws.com/depi-grafana"

        IMAGE_TAG = "latest"

        CLUSTER = "depi-devops-cluster"

        SERVICE_WEB          = "depi-devops-task-service-6msvmsc3"
        SERVICE_PROMETHEUS   = "depi-prometheus-service"
        SERVICE_ALERTMANAGER = "depi-alertmanager-service"
        SERVICE_GRAFANA      = "depi-grafana-service"
    }

    stages {

        stage('Load Functions') {
            steps {
                script {
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
                        export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
                        export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
                        """
                        gv.awsLogin(ECR_WEB, AWS_DEFAULT_REGION)
                    }
                }
            }
        }

        /*
        BUILD + PUSH
        */

        stage('Build Web Image') {
            steps {
                script { gv.buildImage(ECR_WEB, IMAGE_TAG) }
            }
        }

        stage('Push Web Image') {
            steps {
                script { gv.pushImage(ECR_WEB, IMAGE_TAG) }
            }
        }

        stage('Build Prometheus Image') {
            steps {
                script {
                    dir("prometheus") {
                        gv.buildImage(ECR_PROMETHEUS, IMAGE_TAG)
                    }
                }
            }
        }

        stage('Push Prometheus Image') {
            steps {
                script { gv.pushImage(ECR_PROMETHEUS, IMAGE_TAG) }
            }
        }

        stage('Build Alertmanager Image') {
            steps {
                script {
                    dir("prometheus/alertmanager") {
                        gv.buildImage(ECR_ALERTMANAGER, IMAGE_TAG)
                    }
                }
            }
        }

        stage('Push Alertmanager Image') {
            steps {
                script { gv.pushImage(ECR_ALERTMANAGER, IMAGE_TAG) }
            }
        }

        stage('Build Grafana Image') {
            steps {
                script {
                    dir("grafana") {
                        gv.buildImage(ECR_GRAFANA, IMAGE_TAG)
                    }
                }
            }
        }

        stage('Push Grafana Image') {
            steps {
                script { gv.pushImage(ECR_GRAFANA, IMAGE_TAG) }
            }
        }

        /*
        DEPLOY
        */

        stage('Deploy All Services to ECS') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'aws-creds',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {
                    script {
                        sh """
                        export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
                        export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
                        """

                        gv.deployToEcs(CLUSTER, SERVICE_WEB, AWS_DEFAULT_REGION)
                        gv.deployToEcs(CLUSTER, SERVICE_PROMETHEUS, AWS_DEFAULT_REGION)
                        gv.deployToEcs(CLUSTER, SERVICE_ALERTMANAGER, AWS_DEFAULT_REGION)
                        gv.deployToEcs(CLUSTER, SERVICE_GRAFANA, AWS_DEFAULT_REGION)
                    }
                }
            }
        }
    }
}

