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
            if command -v allure >/dev/null 2>&1; then
                allure generate ./allure-results -o ./allure-report --clean
            else
                echo "Allure CLI not found, skipping report generation"
            fi
        '''
    }
    
    success {
        archiveArtifacts artifacts: 'allure-report/**/*', allowEmptyArchive: true
    }
    }
}