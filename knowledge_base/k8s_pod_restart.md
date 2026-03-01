# Restarting Pods in Kubernetes

When pods need to be restarted in a Kubernetes cluster:

1. Check pod status: `kubectl get pods -n <namespace>`
2. View pod events: `kubectl describe pod <pod-name> -n <namespace>`
3. Check logs: `kubectl logs <pod-name> -n <namespace> --tail=100`
4. Delete pod to trigger restart: `kubectl delete pod <pod-name> -n <namespace>`
5. For deployment rollout restart: `kubectl rollout restart deployment/<name> -n <namespace>`
6. Watch rollout status: `kubectl rollout status deployment/<name> -n <namespace>`
7. If pod is stuck in Terminating: `kubectl delete pod <pod-name> --force --grace-period=0`
8. Check resource limits if OOMKilled: increase memory in deployment spec
