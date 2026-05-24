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
                sh '${PIP} install -r requirements.txt --break-system-packages'
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
            sh '''
                allure generate ./allure-results -o ./allure-report --clean
            '''
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'allure-report',
                reportFiles: 'index.html',
                reportName: 'Allure Report'
            ])
        }
    }
}