# Weather ML Demo — Docker + Kubernetes

A machine learning project that fetches real historical weather data from a public API,
trains a Linear Regression model, and serves temperature predictions through a REST API.
Containerized with Docker and deployed on a local Kubernetes cluster using Docker Desktop.

> **Important:** You must call `/train` before `/predict`. The model is stored in memory
> and must be trained each time the app starts.

---

## What This Project Does

1. Fetches daily max temperature data for New York City from the [Open-Meteo](https://open-meteo.com/) public API (no API key needed)
2. Trains a simple **Linear Regression** model using day index as input and temperature as output
3. Predicts the **next day's temperature** via a REST API endpoint
4. Runs as a **Docker container** deployed on **Kubernetes**

---

## Architecture

| Layer | Technology | Role |
| --- | --- | --- |
| ML model | Python + scikit-learn | Trains LinearRegression on weather data |
| API server | Flask | Exposes `/train` and `/predict` HTTP endpoints |
| Container | Docker | Packages the app and its dependencies |
| Orchestration | Kubernetes | Deploys, scales, and self-heals the container |

---

## Project Files

| File | Purpose |
| --- | --- |
| `app.py` | Flask app with `/train` and `/predict` endpoints |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Instructions to build the Docker image |
| `ml-demo.yaml` | Kubernetes Deployment + Service |

---

## Prerequisites

Make sure the following are installed before you start:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (with Kubernetes enabled — see Step 3)
- [kubectl](https://kubernetes.io/docs/tasks/tools/) (included with Docker Desktop)
- Terminal

---

## Step 1 — Build the Docker Image

Open PowerShell in the project folder and run:

```powershell
docker build -t wx-ml:1.0 .
```

Verify the image was created:

```powershell
docker images
```

You should see `wx-ml` listed with tag `1.0`.

---

## Step 2 — Run the Container Locally (optional smoke test)

```powershell
docker run -p 5000:5000 wx-ml:1.0
```

In a second PowerShell window, test the endpoints:

```powershell
Invoke-RestMethod http://localhost:5000/train
Invoke-RestMethod http://localhost:5000/predict
```

Press `Ctrl+C` to stop the container when done.

---

## Step 3 — Create a Kubernetes Cluster with Docker Desktop

1. Open **Docker Desktop**
2. Click **Kubernetes** in the left sidebar
3. Click **Create cluster**
4. Leave all settings at their defaults:
   - Cluster type: **kind**
   - Nodes: **1**
5. Click **Create**
6. Wait until the cluster status shows **Running**

Verify the cluster is ready:

```powershell
kubectl get nodes
```

You should see one node with status `Ready`.

---

## Step 4 — Apply the Kubernetes YAML

```powershell
kubectl apply -f ml-demo.yaml
```

This creates the Deployment and the Service in one command.

---

## Step 5 — Check Kubernetes Resources

Check nodes:
```powershell
kubectl get nodes
```

Check pods (wait until STATUS shows `Running`):
```powershell
kubectl get pods
```

Check deployments:
```powershell
kubectl get deployments
```

Check services:
```powershell
kubectl get services
```

---

## Step 6 — Call the API Endpoints

### Recommended: port-forward (easiest)

Forward port 5000 from the Service directly to your machine:

```powershell
kubectl port-forward service/wx-ml-svc 5000:5000
```

Leave that running, then open a second PowerShell window:

```powershell
# Step 1 — train the model (always required first)
Invoke-RestMethod http://localhost:5000/train

# Step 2 — get the predicted next-day temperature
Invoke-RestMethod http://localhost:5000/predict
```

Example output from `/predict`:

```json
{
  "next_day_index": 18,
  "predicted_temperature_celsius": 26.16
}
```

> The predicted value will vary depending on the weather data returned by the API.

### Alternative: NodePort (optional)

Run `kubectl get services` and look at the `PORT(S)` column. It will show something like `5000:32500/TCP`. Use the 5-digit port:

```powershell
Invoke-RestMethod http://localhost:32500/train
Invoke-RestMethod http://localhost:32500/predict
```

---

## Step 7 — Scale to 3 Replicas

```powershell
kubectl scale deployment wx-ml --replicas=3
```

Check that 3 pods are running:

```powershell
kubectl get pods
```

---

## Step 8 — Self-Healing Demo

Copy one of the pod names from `kubectl get pods`, then delete it:

```powershell
kubectl delete pod <pod-name>
```

Immediately check pods again:

```powershell
kubectl get pods
```

Kubernetes detects the missing pod and automatically starts a replacement.
This is **self-healing** in action.

---

## Cleanup

Remove all Kubernetes resources:

```powershell
kubectl delete -f ml-demo.yaml
```
