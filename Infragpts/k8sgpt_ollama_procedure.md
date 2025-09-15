# End-to-End Procedure: Running K8sGPT with Ollama on Kubernetes

This guide explains how to deploy **Ollama** in a Kubernetes cluster and configure **K8sGPT** to use Ollama as a custom REST backend.

---

## 1. Prerequisites

- A running Kubernetes cluster (k3s/k8s).
- `kubectl` and `helm` installed and configured.
- Cluster access with admin privileges.

---

## 2. Deploy Ollama in Kubernetes

### a. Create Namespace
```bash
kubectl create namespace ollama
```

### b. Create Ollama Deployment & Service (`ollamadeployment.yaml`)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama
  namespace: ollama
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ollama
  template:
    metadata:
      labels:
        app: ollama
    spec:
      containers:
        - name: ollama
          image: ollama/ollama:latest
          ports:
            - containerPort: 11434
          volumeMounts:
            - name: ollama-models
              mountPath: /root/.ollama
      volumes:
        - name: ollama-models
          emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: ollama-service
  namespace: ollama
spec:
  selector:
    app: ollama
  ports:
    - protocol: TCP
      port: 11434
      targetPort: 11434
```

Apply it:
```bash
kubectl apply -f ollamadeployment.yaml
```

Verify:
```bash
kubectl get pods -n ollama
kubectl get svc -n ollama
```

---

## 3. Install K8sGPT Operator

```bash
helm repo add k8sgpt https://charts.k8sgpt.ai/
helm repo update
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml   # for k3s users
helm upgrade --install k8sgpt k8sgpt/k8sgpt-operator -n k8sgpt-operator-system --create-namespace
```

Verify CRDs installed:
```bash
kubectl get crd | grep k8sgpt
```

---

## 4. Create K8sGPT Custom Resource

### a. Create `k8sgpt-cr.yaml`
```yaml
apiVersion: core.k8sgpt.ai/v1alpha1
kind: K8sGPT
metadata:
  name: k8sgpt-sample
  namespace: k8sgpt-operator-system
spec:
  ai:
    enabled: true
    backend: customrest
    model: mistral
    baseUrl: http://ollama-service.ollama.svc.cluster.local:11434
```

Apply it:
```bash
kubectl apply -f k8sgpt-cr.yaml
```

---

## 5. Verify Integration

Check CR status:
```bash
kubectl get k8sgpt -n k8sgpt-operator-system
```

Check operator logs:
```bash
kubectl logs -n k8sgpt-operator-system deploy/k8sgpt-operator-controller-manager -c manager
```

---

## 6. Usage

Run diagnostics:
```bash
kubectl k8sgpt analyze --explain
```

K8sGPT will now use **Ollama (Mistral model)** for AI analysis of your cluster.

---

✅ **End of Procedure**  
