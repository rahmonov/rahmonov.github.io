Title: Introduction to Kubernetes
Date: 2018-02-03 20:10
Modified: 2018-02-03 20:10
Category: programming
Tags: kubernetes
Slug: introduction-to-kubernetes
Authors: Jahongir Rahmonov
Summary: What is Kubernetes? What does it consist of? A practical example

Looking back, 2017 was the year Kubernetes conquered the container orchestration space. For years, Kubernetes' rivals 
such as Docker Swarm and Mesos have been offering their own container orchestration tools and now they both added 
support for Kubernetes within their ecosystems. The largest cloud providers such as AWS, Microsoft Azure and Oracle 
Cloud announced Kubernetes integrations into their respective cloud platforms, not mentioning Google where Kubernetes 
came from originally. So, every developer would benefit from at least learning the basics of Kubernetes. That's exactly 
what we are going to do in this post.

Before we get started I want you to watch this awesome animated guide first. Then come back and we will discuss the 
details:

<iframe width="760" height="415" src="https://www.youtube.com/embed/4ht22ReBjno" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

Did you watch it? NO? GO BACK TO THE VIDEO YOU STUBBORN LITTLE DEVELOPER! Good. Now let's get the formal definition of 
Kubernetes out of the way:

> Kubernetes is a system for managing containerized applications across a cluster of nodes

In simple terms, you have a group of machines (e.g. VMs) and containerized applications (e.g. Dockerized applications), 
and Kubernetes will help you to easily manage those apps across those machines. We will see a practical example later.

## Kubernetes components

Kubernetes cluster consists of Master and Nodes:

<div class="gallery large">
    <a href="https://s3.amazonaws.com/rahmonov.me/post-images/intro-to-k8s/cluster.svg" rel="lightbox" title="Kubernetes Cluster">
        <img src="https://s3.amazonaws.com/rahmonov.me/post-images/intro-to-k8s/cluster.svg" alt="Kubernetes Cluster">
        <span>Kubernetes Cluster (https://kubernetes.io)</span>
    </a>
</div>

Master is the controlling machine and has components which operate as the main management contact point for users. 
Nodes are where your containerized apps run. Simply put, you run your containerized apps in nodes and you control them 
through the master.

Both master and nodes have very important components which we discuss below.

### Master Components

- **Etcd** is a consistent and highly-available key-value store used as Kubernetes’ backing store for all cluster data. 
Basically, it is a database for Kubernetes data and represents the state of the cluster.

- **API Server** is what exposes Kubernetes API, as its name suggests. It is the main management point of the entire 
cluster. It acts as the bridge between various components disseminating information and commands. In simple terms, it is
the frontend of the Kubernetes control pane.
 
- **Controller Manager** is responsible for regulating the state of the cluster and performing routine tasks. For example, 
the replication controller ensures that the number of replicas defined for a service matches the number currently deployed
on the cluster. Another example is the endpoints controller adjusting, well, endpoints by watching for changes in Etcd.

- **Scheduler Service** is what assigns workloads to nodes. This is how it does it:
    1. Reads the workload's operating requirements
    2. Analyze the current infrastructure environment
    3. Place the workload on an acceptable node(s)
   
### Node Components

<div class="gallery large">
    <a href="https://s3.amazonaws.com/rahmonov.me/post-images/intro-to-k8s/node.svg" rel="lightbox" title="Node components">
        <img src="https://s3.amazonaws.com/rahmonov.me/post-images/intro-to-k8s/node.svg" alt="Node components">
        <span>Node Components (https://kubernetes.io)</span>
    </a>
</div>

- **Docker** is used in order to run your containers, duh! `rkt` can be used as an alternative to docker.

- **Kubelet** is the main contact point for each node with the cluster group, relaying to and from control pane
services (master).

- **Proxy** is used for maintaning network rules and performing connection forwarding. This is what enables the 
Kubernetes service abstraction (DNS).

You won't directly interact with these components directly but it is good to know what is happening behind the magic.

If the above components are something you don't have to know, the following you must know. Pay great attention.

## Kubernetes Work Units

- **Pod** is the most basic unit in Kubernetes. It represents a unit of deployment, i.e. a single instance of an 
application which may consist of either a single container or a small number of containers that are tightly coupled and 
that share resources (for example, a cloud sql proxy container should run in the same pod as the main application). Other
than an application container (or multiple containers), a pod encapsulates storage resources, a unique network IP and options
that govern how the container(s) should run.

<div class="gallery large">
    <a href="https://s3.amazonaws.com/rahmonov.me/post-images/intro-to-k8s/pods.svg" rel="lightbox" title="Pods">
        <img src="https://s3.amazonaws.com/rahmonov.me/post-images/intro-to-k8s/pods.svg" alt="Pods">
        <span>Pods (https://kubernetes.io)</span>
    </a>
</div>

Excuse the image size. You rarely have to directly deploy pods (I never have). You mostly will attach into the process 
for debugging and testing purposes.
 
- **Service** groups together logical collections of pods that perform the same function and presents them as a single 
entity. Also, it acts as a basic load balancer between pods and enables consumers not to worry about anything beyond a 
single access location.

<div class="gallery large">
    <a href="https://s3.amazonaws.com/rahmonov.me/post-images/intro-to-k8s/service1.svg" rel="lightbox" title="Service">
        <img src="https://s3.amazonaws.com/rahmonov.me/post-images/intro-to-k8s/service1.svg" alt="Service">
        <span>Service (https://kubernetes.io)</span>
    </a>
</div>

- **Label** is an arbitrary tag to mark work units. Basic key-value pairs. They are what enable services to group 
several pods together. Let's say you give your pods this label "microservice: auth" and the service with the same selector
("microservice: auth") will be able to forward traffic to those pods.

<div class="gallery large">
    <a href="https://s3.amazonaws.com/rahmonov.me/post-images/intro-to-k8s/service2.svg" rel="lightbox" title="Lables">
        <img src="https://s3.amazonaws.com/rahmonov.me/post-images/intro-to-k8s/service2.svg" alt="Labels">
        <span>Labels (https://kubernetes.io)</span>
    </a>
</div>

- **Deployment** provides a declarative syntax to create/update pods. You tell a deployment your desired state (how many, 
how fast, when) and it changes the actual state to the desired state at a specified rate

<div class="gallery large">
    <a href="https://s3.amazonaws.com/rahmonov.me/post-images/intro-to-k8s/deployment2.svg" rel="lightbox" title="Deployment">
        <img src="https://s3.amazonaws.com/rahmonov.me/post-images/intro-to-k8s/deployment2.svg" alt="Deployment">
        <span>Deployment (https://kubernetes.io)</span>
    </a>
</div>

- **Ingress** manages external access to the services. Provides load balancing, SSL termination and path/hos based routing, 
which are considered its advantages over services of "Load Balancer" type. See below for more details.

- **Ingress Controller** is what implements `Ingress` definitions. That is, you write what you need in `Ingress` objects
and ingress controllers will turn them into reality. It means that `Ingress` itself is nothing without `Ingress Controllers`.
 
## Full example
 
I know that this is all theory and it is boring. You need to set these things up yourself in order to fully understand.
That's why, carefully go trough this post and get your hands dirty:
 
> <a href="/posts/nginx-ingress-controller/">Full Kubernetes Example</a> 

Did you go through the example? Pretty cool huh? Kubernetes makes everything very easy. Now that you have seen a practical
example, read these common pitfalls that I have been a victim of while learning Kubernetes. They will save you weeks of 
your time.

## Common pitfalls

- **Using services of type "LoadBalancer" to expose externally**: In most tutorials, even in the official documentation,
they use `LoadBalancer` services to expose the application. The reason is that it is really easy to do and great of testing.
However, when you want to do SSL termination or route/host based routing, services are not your friends. Use `Ingress` for 
real applications.

- **GKE Ingress Controller**: In GKE, you don't have to manage your own ingress controller 
because GKE has its own managed for you. It is great and it works great. However, it cannot force `https` at the time of 
this writing. Maybe it will change in the future. But for now, you will have to manage your own Ingress Controller if `https`
is a must for your app, which it should be in 2018. See the full example about on how to do that.
 
- **SSL certificates**: Don't manage them yourself. Use [`kube-lego`](https://github.com/jetstack/kube-lego) which 
automatically updates your certificates when they are about to expire.

## Bonus

- **Zero Downtime**: By using something called `readiness-probe` and a rolling update strategy it is very easy to achieve
zero-downtime deployment. Let me know in the comments if you want a post showing how to do this.

- **Don't be afraid to switch to Kubernetes**: Kubernetes is a new technology and is full of <strike>dark</strike> magic.
That's why, it is very natural to be afraid to switch from old tools to Kubernetes, especially in production. I know I was
terrified. So, what I did was to switch gradually. First step was to forward 10% of the production traffic to our 
Kubernetes cluster and the rest 90% to our old setup. Next step was to monitor how it was doing. If it was doing OK we changed 
those numbers to 30% and 70%. And on it goes until it reaches 100% to Kubernetes cluster and 0% to our old setup. This way,
you can make sure that your new Kuberbetes cluster will do just fine even in production. We were using `NGINX` in our 
old setup and this is how we split traffic between upstreams:

```bash
upstream dashboard_app_server {
    server old-setup.com weight=9;
    server new-kubernetes-cluster.com weight=1;
}
```

It means that 90% of the traffic goes to old old-setup.com and 10% goes to new-kubernetes-cluster.com. Pretty easy.

## Conclusion
I wish I had this material when I was learning Kubernetes. It would save me weeks of my time. I hope it saves for somebody
else. Make sure to check out the <a href="/posts/nginx-ingress-controller/">full example</a>. And always remember this quote
from [Kelsey Hightower](https://twitter.com/kelseyhightower) himself:

> Kubernetes is going to set you free. But it is going to piss you off first.

Thanks for reading.
  
Fight on!  

<hr>

You may also find this <strong>related</strong> post interesting: <a href="/posts/nginx-ingress-controller/">Nginx Ingress Controller</a>
