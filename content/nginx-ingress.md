Title: Nginx Ingress Controller
Date: 2017-11-11 20:10
Modified: 2017-11-11 20:10
Category: programming
Tags: kubernetes
Slug: nginx-ingress-controller
Authors: Jahongir Rahmonov
Summary: Nginx Ingress Controller Tutorial

This tutorial assumes that you know the basics of [Kubernetes](/posts/introduction-to-kubernetes/).

We all know that the easiest way to forward the external traffic to your app is to create a service of type `LoadBalancer`. 
If you are running in a cloud environment such as AWS or GCP, of course. That might be OK for some simple apps. However,
if you want to do SSL termination, path based routing or host based routing, you get stuck. This is where [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) 
comes in. It will allow you to do everything mentioned above and much more, and looks like this:
  
```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: test
  annotations:
    ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: foo.bar.com
    http:
      paths:
      - path: /foo
        backend:
          serviceName: s1
          servicePort: 80
      - path: /bar
        backend:
          serviceName: s2
          servicePort: 80
```  

If you try to create an ingress resource from this file, however, you will witness that nothing will happen(except for GKE, which we will get to later). 
In order for such ingress resources to take effect, there has to be something called Ingress Controller running. Basically, Ingress Controllers 
will be constantly watching for changes in Ingress resources and ***apply*** the rules outlined in those ingress resources. GKE is an exception to this rule.
When you create a cluster in GKE, it will automatically start its built in ingress controller and you don't have to worry about starting it by yourself.
However, at the time of this writing, it has some limits such as a lack of support for web sockets and it can't force SSL. If these things are 
critical to your app, you might want to consider some other ingress controllers. The most popular ones are the following:

- [NGINX ingress controller by Kubernetes](https://github.com/kubernetes/ingress-nginx)
- [NGINX ingress controller by Nginx Inc](https://github.com/nginxinc/kubernetes-ingress)
- [Traefik](https://traefik.io/)
 
I don't have much insight into the difference between two nginx controllers but I think that both of them are good enough. In this tutorial, 
we will be using the one by the Kubernetes team just because it has more stars in GitHub at the time of writing.  
     
Here is the plan:

1. We will create a cluster on GKE
2. We will set up an Nginx Ingress Controller
3. Once it is running, we will deploy a simple app with the help of an Ingress Resource
4. Be happy
 
 
## Creating a cluster
    
On GKE, it is as easy as this:
 
```bash
gcloud container clusters create nginx-ingress-controller
``` 

Your mileage will vary if you are using another cloud provider.

It will take a while to create a cluster. After the command is done, you can check if nodes are ready:

```bash
kubectl get nodes
```

Output should be:

```bash
gke-nginx-ingress-contro-default-pool-6dbb0978-mkwj   Ready     <none>    1h        v1.7.8-gke.0
gke-nginx-ingress-contro-default-pool-6dbb0978-xvtb   Ready     <none>    1h        v1.7.8-gke.0
gke-nginx-ingress-contro-default-pool-6dbb0978-zp6b   Ready     <none>    1h        v1.7.8-gke.0
```

## Setting up the Nginx Ingress Controller

Our Nginx Ingress Controller will be running in its own namespace. That's why, create `namespace.yaml` with the following content:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ingress-nginx
```

Then, create the resource:

```yaml
kubectl create -f namespace.yaml
```

One of the requirements is to have a default backend and that default backend should handle all url paths and hosts that Nginx Controller does not 
understand (i.e., all the requests that are not mapped with an Ingress). Basically, it should expose `/healtz` url which returns 200 and all the 
other urls should return 404. Such container has already been written for us. That's why, in this step, we create a default backend deployment and service.
Create `default-backend.yaml` with the following content:

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: default-http-backend
  labels:
    app: default-http-backend
  namespace: ingress-nginx
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: default-http-backend
    spec:
      terminationGracePeriodSeconds: 60
      containers:
      - name: default-http-backend
        # Any image is permissable as long as:
        # 1. It serves a 404 page at /
        # 2. It serves 200 on a /healthz endpoint
        image: gcr.io/google_containers/defaultbackend:1.4
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 30
          timeoutSeconds: 5
        ports:
        - containerPort: 8080
        resources:
          limits:
            cpu: 10m
            memory: 20Mi
          requests:
            cpu: 10m
            memory: 20Mi
---

apiVersion: v1
kind: Service
metadata:
  name: default-http-backend
  namespace: ingress-nginx
  labels:
    app: default-http-backend
spec:
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: default-http-backend
```
 
Create the resources:
 
```bash
kubectl create -f default-backend.yaml
``` 

Now that our default backend is running, we can create the Nginx Ingress Controller. Create `nginx-ingress-controller.yaml` with the following content:
  
```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-ingress-controller
  namespace: ingress-nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ingress-nginx
  template:
    metadata:
      labels:
        app: ingress-nginx
      annotations:
        prometheus.io/port: '10254'
        prometheus.io/scrape: 'true'
    spec:
      containers:
        - name: nginx-ingress-controller
          image: quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.9.0-beta.17
          args:
            - /nginx-ingress-controller
            - --default-backend-service=$(POD_NAMESPACE)/default-http-backend
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
          ports:
          - name: http
            containerPort: 80
          - name: https
            containerPort: 443
          livenessProbe:
            failureThreshold: 3
            httpGet:
              path: /healthz
              port: 10254
              scheme: HTTP
            initialDelaySeconds: 10
            periodSeconds: 10
            successThreshold: 1
            timeoutSeconds: 1
          readinessProbe:
            failureThreshold: 3
            httpGet:
              path: /healthz
              port: 10254
              scheme: HTTP
            periodSeconds: 10
            successThreshold: 1
            timeoutSeconds: 1
```

Then, create the resource:

```bash
kubectl create -f nginx-ingress-controller.yaml
```

This will create a deployment whose pods will have the ports 80 and 443 open for http and https respectively. Now, we can expose this deployment 
so that it will have External IP through which users will connect to our app. For that we will create a service of type `LoadBalancer`:

```yaml
kind: Service
apiVersion: v1
metadata:
  name: ingress-nginx
  namespace: ingress-nginx
  labels:
    app: ingress-nginx
spec:
  externalTrafficPolicy: Local
  type: LoadBalancer
  selector:
    app: ingress-nginx
  ports:
  - name: http
    port: 80
    targetPort: http
  - name: https
    port: 443
    targetPort: https
```

Create the resource:

```bash
kubectl create -f nginx-controller-service.yaml
```

After a little while, if you get all the services, you will see that this service will have an External IP:

```bash
kubectl get svc --namespace=ingress-nginx
```

Output should be:

```bash
NAME                   TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)                      AGE
ingress-nginx          LoadBalancer   10.59.251.2     104.155.150.97   80:32392/TCP,443:30799/TCP   1h
```

We can try that out by using `curl`. Requests to `/` should return 404 and to `/healthz` should return 200:

```bash
curl -v 104.155.150.97/
```

Output should be:

```bash
...
< HTTP/1.1 404 Not Found
...
```

and then:

```bash
curl -v 104.155.150.97/healthz
```

will give this:

```bash
...
< HTTP/1.1 200 OK
...
```

In the last step, we will patch our nginx ingress controller deployment a little bit, as intructed [here](https://github.com/kubernetes/ingress-nginx/blob/master/deploy/README.md#gce---gke).
Create `nginx-contoller-patch.yaml` with this content:

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-ingress-controller
  namespace: ingress-nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ingress-nginx
  template:
    metadata:
      labels:
        app: ingress-nginx
    spec:
      containers:
        - name: nginx-ingress-controller
          image: quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.9.0-beta.16
          args:
            - /nginx-ingress-controller
            - --default-backend-service=$(POD_NAMESPACE)/default-http-backend
            - --publish-service=$(POD_NAMESPACE)/ingress-nginx
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
          ports:
          - name: http
            containerPort: 80
          - name: https
            containerPort: 443
```

This time, use `apply` because we are patching an existing resource:

```bash
kubectl apply -f nginx-contoller-patch.yaml
```

At this point, our nginx ingress controller should be ready. Verify by typing this:

```bash
kubectl get pods --all-namespaces -l app=ingress-nginx
```

Output should be:

```bash
NAMESPACE       NAME                                        READY     STATUS    RESTARTS   AGE
ingress-nginx   nginx-ingress-controller-1038678203-x2bjb   1/1       Running   0          2h
```

## Deploy an app

Great! Now that our nginx ingress controller is running, we can deploy our application. It is a simple app called cafe. It has two paths: 
`/coffee` and `/tea` which simple prints info about the server they are running on. Let's get started.

Create `coffee.yaml` with this content:

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: coffee-rc
spec:
  replicas: 2
  template:
    metadata:
      labels:
        app: coffee
    spec:
      containers:
      - name: coffee
        image: nginxdemos/hello
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: coffee-svc
  labels:
    app: coffee
spec:
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
    name: http
  selector:
    app: coffee
```

Create `tea.yaml` with this content:

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: tea-rc
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: tea
    spec:
      containers:
      - name: tea
        image: nginxdemos/hello
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: tea-svc
  labels:
    app: tea
spec:
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
    name: http
  selector:
    app: tea
```

Create the resources:

```bash
kubectl create -f coffee.yaml
kubectl create -f tea.yaml
```

Verify that pods are running:

```bash
kubectl get pods
```

Output:

```bash
NAME                         READY     STATUS    RESTARTS   AGE
coffee-rc-3539744749-99qc3   1/1       Running   0          2h
coffee-rc-3539744749-pbwwz   1/1       Running   0          2h
tea-rc-3874333905-g173z      1/1       Running   0          2h
tea-rc-3874333905-n2r25      1/1       Running   0          2h
tea-rc-3874333905-rtsrp      1/1       Running   0          2h
```

Cool, now we can create our Ingress object which specifies the path rules:

```bash
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: cafe-ingress-nginx
  annotations:
    kubernetes.io/ingress.class: "nginx"
spec:
  rules:
  - host: cafe.example.com
    http:
      paths:
      - path: /tea
        backend:
          serviceName: tea-svc
          servicePort: 80
      - path: /coffee
        backend:
          serviceName: coffee-svc
          servicePort: 80
```

Note that this resource has an annotation `kubernetes.io/ingress.class: "nginx"`. This is needed because this ingress is only to be picked up by 
our Nginx Ingress Controller, not the one by GKE.

Create the resource:

```bash
kubectl create -f cafe-ingress.yaml
```

It will take a while to take effect. After some time if you attach to the Nginx Ingress Controller pod, you can verify that Nginx configuration was updated:

```bash
kubectl get pods --namespace=ingress-nginx
```

Output:

```bash
NAME                                        READY     STATUS    RESTARTS   AGE
nginx-ingress-controller-1038678203-x2bjb   1/1       Running   0          2h
```

Attach to its bash:

```bash
kubectl exec -it nginx-ingress-controller-1038678203-x2bjb bash --namespace=ingress-nginx
```

Then, open `/etc/nginx/nginx.conf` and you will see that the paths `/tea` and `/coffee` have been configured there:

```bash
server {
    server_name cafe.example.com ;
...    
location /tea
...
location /coffee 
...
```


Everything is ready now. The only thing left is to configure DNS. If you are on a UNIX like machine, you can go open `/etc/hosts` and 
append this:

```bash
104.155.150.97 cafe.example.com
```

Make sure to replace `104.155.150.97` with the IP of your Nginx Ingress Controller's External IP, which you can find by typing this:

```bash
kubectl get svc --namespace=ingress-nginx
```

Also, make sure that you flush your DNS cache. If you are on a mac, you can do this:

```bash
sudo dscacheutil -flushcache
```

Now, go ahead to `cafe.example.com` and see the result. Try going to `cafe.example.com/tea` and `cafe.example.com/coffee`:

<div class="gallery large">
    <a href="https://s3.amazonaws.com/rahmonov.me/post-images/nginx-ingress-conroller/tea.png" rel="lightbox" title="Cafe">
        <img src="https://s3.amazonaws.com/rahmonov.me/post-images/nginx-ingress-conroller/tea.png" alt="Cafe">
        <span>The Cafe App</span>
    </a>
</div>

## Conclusion
This is something that I have had tons of problems setting up and getting my heads around. I hope that this will save some time for some of you guys.
Thanks for reading.

Fight on!

<hr>

You may also find this <strong>related</strong> post interesting: <a href="/posts/introduction-to-kubernetes/">Introduction to Kubernetes</a>
