# K8sGPT Deployment and CLI Setup Guide

## Step 1: Deploy Ollama
Deploy the Ollama pod in your `ollama` namespace.
```bash
kubectl apply -f ollama-deployment.yaml -n ollama
```

## Step 2: Pull Mistral Model
Exec into the Ollama pod and pull the Mistral AI model:
```bash
kubectl exec -it -n ollama <ollama-pod-name> -- ollama pull mistral
```

## Step 3: Install K8sGPT Operator
Add Helm repo, update, and install the operator:
```bash
helm repo add k8sgpt https://charts.k8sgpt.ai/
helm repo update
helm install k8sgpt k8sgpt/k8sgpt-operator -n k8sgpt-operator-system --create-namespace
```
Verify CRDs:
```bash
kubectl get crd | grep k8sgpt
```

## Step 4: Install K8sGPT CLI on Host
Download and install CLI:
```bash
curl -sSL https://github.com/k8sgpt-ai/k8sgpt/releases/latest/download/k8sgpt_linux_amd64.tar.gz | tar -xz
sudo mv k8sgpt /usr/local/bin/
```
Verify CLI:
```bash
k8sgpt version
```
Create CLI config:
```bash
mkdir -p ~/.config/k8sgpt
cat <<EOF > ~/.config/k8sgpt/k8sgpt.yaml
ai:
    providers:
        - name: customrest
          backend: customrest
          model: mistral
          baseurl: http://172.27.65.69:30475/api/generate
          password: dummy
          temperature: 0.7
          customheaders: []
    defaultprovider: customrest
commit: a75ec50
date: unknown
kubeconfig: ""
kubecontext: ""
version: 0.4.2
EOF
```

## Step 5: Create Kubernetes Secret
Create a secret from the CLI config:
```bash
kubectl create secret generic k8sgpt-auth \
  --from-file=k8sgpt.yaml=~/.config/k8sgpt/k8sgpt.yaml \
  -n ollama
```
Verify:
```bash
kubectl get secret k8sgpt-auth -n ollama -o yaml
```

## Step 6: Verify K8sGPT Auth
Check that `customrest` provider is active:
```bash
k8sgpt auth list
```

## Step 7: Run K8sGPT CLI
Analyze the Kubernetes cluster:
```bash
k8sgpt analyze --explain --backend customrest
```

## Notes
- K8sGPT CLI reads config from `/root/.config/k8sgpt/k8sgpt.yaml`.
- Secret `k8sgpt-auth` must exist in the `ollama` namespace.
- `customrest` backend must be set in the CLI config.
- CR-based operator is optional; CLI alone can be used for debugging.

