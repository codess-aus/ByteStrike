"""
Deployment configuration and orchestration for Blueprint Decoder.
This demonstrates a complete production deployment workflow.
"""

import os
import subprocess
import json
from typing import Optional
from dataclasses import dataclass

@dataclass
class DeploymentConfig:
    service_name: str = "blueprint-decoder"
    version: str = os.getenv("VERSION", "1.0.0")
    environment: str = os.getenv("ENVIRONMENT", "staging")
    replicas: int = 3
    docker_registry: str = "registry.company.com"
    namespace: str = "default"
    timeout_seconds: int = 300

class KubernetesDeployer:
    """Handles deployments to Kubernetes cluster"""
    
    def __init__(self, config: DeploymentConfig):
        self.config = config
    
    def build_docker_image(self) -> bool:
        """Build Docker image"""
        tag = f"{self.config.docker_registry}/{self.config.service_name}:{self.config.version}"
        
        print(f"Building Docker image: {tag}")
        result = subprocess.run(
            ["docker", "build", "-t", tag, "."],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Build failed: {result.stderr}")
            return False
        
        print("✓ Docker image built successfully")
        return True
    
    def push_docker_image(self) -> bool:
        """Push Docker image to registry"""
        tag = f"{self.config.docker_registry}/{self.config.service_name}:{self.config.version}"
        
        print(f"Pushing image to registry: {tag}")
        result = subprocess.run(
            ["docker", "push", tag],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Push failed: {result.stderr}")
            return False
        
        print("✓ Image pushed to registry")
        return True
    
    def deploy_to_kubernetes(self) -> bool:
        """Deploy to Kubernetes using kubectl"""
        image = f"{self.config.docker_registry}/{self.config.service_name}:{self.config.version}"
        
        # Create deployment YAML
        deployment_yaml = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {self.config.service_name}
  namespace: {self.config.namespace}
spec:
  replicas: {self.config.replicas}
  selector:
    matchLabels:
      app: {self.config.service_name}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: {self.config.service_name}
        version: {self.config.version}
    spec:
      containers:
      - name: {self.config.service_name}
        image: {image}
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8080
          name: http
        - containerPort: 9090
          name: metrics
        env:
        - name: ENVIRONMENT
          value: {self.config.environment}
        - name: DECODER_TIMEOUT_SECONDS
          value: "30"
        - name: LOG_LEVEL
          value: INFO
        - name: ENCRYPTION_KEY_ID
          valueFrom:
            secretKeyRef:
              name: blueprint-decoder-secrets
              key: encryption-key-id
        - name: WHITELIST_URLS
          valueFrom:
            configMapKeyRef:
              name: blueprint-decoder-config
              key: whitelist-urls
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /readiness
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          readOnlyRootFilesystem: true
---
apiVersion: v1
kind: Service
metadata:
  name: {self.config.service_name}
  namespace: {self.config.namespace}
spec:
  selector:
    app: {self.config.service_name}
  ports:
  - name: http
    port: 80
    targetPort: 8080
  - name: metrics
    port: 9090
    targetPort: 9090
  type: ClusterIP
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: {self.config.service_name}
  namespace: {self.config.namespace}
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: {self.config.service_name}
"""
        
        # Apply deployment
        print(f"Deploying to Kubernetes cluster in namespace: {self.config.namespace}")
        result = subprocess.run(
            ["kubectl", "apply", "-f", "-", f"--namespace={self.config.namespace}"],
            input=deployment_yaml,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Deployment failed: {result.stderr}")
            return False
        
        print("✓ Deployment applied to Kubernetes")
        
        # Wait for rollout
        return self.wait_for_rollout()
    
    def wait_for_rollout(self, timeout_seconds: int = 300) -> bool:
        """Wait for deployment rollout to complete"""
        print(f"Waiting for rollout to complete (timeout: {timeout_seconds}s)...")
        
        result = subprocess.run(
            ["kubectl", "rollout", "status", 
             f"deployment/{self.config.service_name}",
             f"--namespace={self.config.namespace}",
             f"--timeout={timeout_seconds}s"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Rollout failed: {result.stderr}")
            return False
        
        print("✓ Rollout completed successfully")
        return True
    
    def smoke_test(self) -> bool:
        """Run smoke tests against deployed service"""
        print("Running smoke tests...")
        
        # Port-forward to service
        subprocess.Popen(
            ["kubectl", "port-forward", 
             f"svc/{self.config.service_name}", "8080:80",
             f"--namespace={self.config.namespace}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        import time
        time.sleep(2)  # Wait for port-forward
        
        # Test basic endpoint
        result = subprocess.run(
            ["curl", "-f", "http://localhost:8080/healthz"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Smoke test failed: {result.stderr}")
            return False
        
        print("✓ Smoke tests passed")
        return True
    
    def rollback(self, revision: Optional[int] = None) -> bool:
        """Rollback to previous deployment"""
        print("Initiating rollback...")
        
        cmd = ["kubectl", "rollout", "undo",
               f"deployment/{self.config.service_name}",
               f"--namespace={self.config.namespace}"]
        
        if revision:
            cmd.append(f"--to-revision={revision}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Rollback failed: {result.stderr}")
            return False
        
        print("✓ Rollback completed")
        return self.wait_for_rollout()

class DeploymentPipeline:
    """Complete deployment pipeline"""
    
    def __init__(self, config: DeploymentConfig):
        self.config = config
        self.deployer = KubernetesDeployer(config)
    
    def deploy(self) -> bool:
        """Execute complete deployment pipeline"""
        print(f"\n{'='*60}")
        print(f"Deploying {self.config.service_name} v{self.config.version}")
        print(f"Environment: {self.config.environment}")
        print(f"{'='*60}\n")
        
        steps = [
            ("Building Docker image", self.deployer.build_docker_image),
            ("Pushing to registry", self.deployer.push_docker_image),
            ("Deploying to Kubernetes", self.deployer.deploy_to_kubernetes),
            ("Running smoke tests", self.deployer.smoke_test),
        ]
        
        for step_name, step_func in steps:
            print(f"\n→ {step_name}...")
            if not step_func():
                print(f"\n✗ Deployment failed at: {step_name}")
                print("Initiating automatic rollback...")
                self.deployer.rollback()
                return False
        
        print(f"\n{'='*60}")
        print(f"✓ Deployment successful!")
        print(f"Service: {self.config.service_name}")
        print(f"Version: {self.config.version}")
        print(f"Environment: {self.config.environment}")
        print(f"{'='*60}\n")
        
        return True

# Example usage
if __name__ == "__main__":
    config = DeploymentConfig(
        version=os.getenv("VERSION", "1.0.0"),
        environment=os.getenv("ENVIRONMENT", "production"),
        replicas=int(os.getenv("REPLICAS", "3"))
    )
    
    pipeline = DeploymentPipeline(config)
    success = pipeline.deploy()
    
    exit(0 if success else 1)
