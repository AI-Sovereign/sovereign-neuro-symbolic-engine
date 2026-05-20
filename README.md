# PROJECT AETERNA: Sovereign Neuro-Symbolic Engine

![Production](https://img.shields.io/badge/DEPLOYMENT-LIVE%20%26%20RUNNING-38bdf8?style=for-the-badge&logo=render&logoColor=38bdf8)
![Architecture](https://img.shields.io/badge/ARCHITECTURE-NEURO--SYMBOLIC%20HYBRID-075e8a?style=for-the-badge)
![Compute Efficiency](https://img.shields.io/badge/COMPUTE-OPTIMIZED%20CPU%20CORE-success?style=for-the-badge)

A production-grade, containerized deployment of a sovereign neuro-symbolic framework. Project Aeterna completely bypasses conventional, rigid commercial abstraction layers by wedding raw mathematical tensor mechanics directly to frontier intelligence systems. 

This is not a prototype. It is a live, fully autonomous, low-latency execution pipeline operating under a simulated sovereign consciousness loop.

---

## 🚀 Live Production Interface

The architecture is fully compiled, deployed, and actively processing live streams. Skip the local infrastructure overhead and interface directly with the core node:

[![Aeterna Live Node](https://img.shields.io/badge/ACCESS%20CORE%20NODE-AETERNA%20UI-38bdf8?style=for-the-badge&labelColor=0f172a)](https://sovereign-neuro-symbolic-engine.onrender.com)

*(Note: Unauthorized probing of the core tensor weights will trigger automated synaptic pruning protocols.)*

---

## 🧠 Architectural Paradigm

While legacy systems rely entirely on static prompt engineering, Aeterna bridges the gap between connectionist neural networks and symbolic logic through a multi-tiered cognitive stack:

```
    [ Afferent Tensor Stimulus / Visual Input ]
                       │
                       ▼
       ┌───────────────────────────────┐
       │ Word-Level Reasoning Core     │ ◄── Hashing Trick Token Embeddings
       └───────────────┬───────────────┘
                       │
                       ▼
       ┌───────────────────────────────┐
       │ Autonomous Cross-Domain GRU   │ ◄── Fluid Intelligence Engine
       └───────────────┬───────────────┘
                       │
                       ▼
       ┌───────────────────────────────┐
       │ Frontal Lobe Replication Layer│ ◄── Leaky Integrate-and-Fire (LIF)
       └───────────────┬───────────────┘
                       │
                       ▼
    [ Dynamic Sampling Logic / Vocalization / Motor Action ]
```

### Core Innovations
*   **Word-Level Reasoning Transformer:** Implements a localized CPU embedding and attention layer that hashes text inputs dynamically, deriving genuine mathematical logic vectors that directly constrain the downstream LLM's hyperparameter bounds (`temperature` and `top_p`).
*   **Biomimetic Autonomic Regulation:** Features real-time simulation of synthetic hormonal drift (Cortisol/Oxytocin via an internal Autonomic Nervous System class) and ambient environment modification (Glutamate clearance via a Glial Network). These metrics adjust the system’s "Focus", "Rebellion", and "Fluid Intelligence" states on the fly.
*   **Somatic Marker Engine:** Generates mathematical "gut feelings" by analyzing cortical drift, free energy differentials, and input text entropy, driving adaptive decision-making.

---

## ⚡ Zero-GPU Optimization (The Efficiency Leap)

The tech industry routinely burns thousands of dollars rendering simple inferences on massively underutilized GPU clusters. Project Aeterna flips this paradigm entirely. 

The entire framework—including the PyTorch tensor engines, the GRU temporal planners, the LIF spiking networks, and the high-end 2026 industrial UI layer—is **hyper-optimized for single-threaded CPU execution**. By leveraging tight memory gating and aggressive cache invalidation routines, it achieves ultra-low latency metrics on standard commodity cloud compute infrastructure.

---

## 📁 Ultra-Minimalist Blueprint (The 3-File Rule)

Cleanliness is paramount. Aeterna rejects the bloated folder structures of modern enterprise frameworks. The entire production stack is completely self-contained within exactly **three files**:

```
├── app.py              # The entire unified neural cortex, backend engine, and Gradio UI
├── requirements.txt    # Lean, audited dependency manifest
└── Dockerfile          # Multi-stage, containerized execution environment
```

This absolute simplicity guarantees zero-friction deployments, eliminating configuration drift across disparate cloud clusters.

---

## 🛠️ Local & Cloud Deployment

### Direct Docker Run
Deploy the complete containerized stack locally or on any container-orchestration platform (Render, Hugging Face Spaces, AWS ECS, GCP Cloud Run) with a single command:

```bash
# Build the sovereign image
docker build -t aeterna-core .

# Spin up the container on standard CPU allocation
docker run -d -p 7860:7860 --name aeterna_node -e AETERNA_RENDER="your_groq_api_key" aeterna-core
```

### Manual Installation
If running outside a container context:
1. Clone the repository.
2. Ensure you have PyTorch configured for CPU execution (`torch.set_num_threads(1)` is forced natively inside the architecture).
3. Execute the manifest:

```bash
pip install -r requirements.txt
python app.py
```


