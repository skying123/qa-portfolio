pipeline {
    agent any
    
    environment {
        PYTHON = 'python3'
        PIP = 'pip3'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/skying123/qa-portfolio.git'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '${PIP} install -r requirements.txt'
            }
        }
        
        stage('Run API Tests') {
            steps {
                sh '${PYTHON} -m pytest api_tests/ -v --env=prod --alluredir=./allure-results'
            }
        }
        
        stage('Run UI Tests') {
            steps {
                sh '${PYTHON} -m pytest ui_tests/ -v --env=prod --alluredir=./allure-results'
            }
        }
    }
    
    post {
        always {
            allure([
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'allure-results']]
            ])
        }
    }
}