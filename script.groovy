// script.groovy - AWS ECR + ECS helper functions

def buildImage(ecrRepo, imageTag) {
    sh "docker build -t ${ecrRepo}:${imageTag} ."
}

def awsLogin(ecrRepo, region) {
    sh """
    aws ecr get-login-password --region ${region} \
    | docker login --username AWS --password-stdin ${ecrRepo}
    """
}

def pushImage(ecrRepo, imageTag) {
    sh "docker push ${ecrRepo}:${imageTag}"
}

def deployToEcs(cluster, service, region) {
    sh """
    aws ecs update-service \
    --cluster ${cluster} \
    --service ${service} \
    --force-new-deployment \
    --region ${region}
    """
}
