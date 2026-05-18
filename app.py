import gradio as gr
import random, os, asyncio, uuid, datetime, time, json
import urllib.request, re, collections
import torch
import torch.nn as nn
import torch.optim as optim
import edge_tts
from googlesearch import search
from groq import AsyncGroq
import base64

# --- SYSTEM OPTIMIZATION ---
torch.set_num_threads(1)
torch.set_grad_enabled(True)

HF_DATA_PATH = "/data"
if os.path.exists(HF_DATA_PATH) and os.access(HF_DATA_PATH, os.W_OK):
    STORAGE_DIR = os.path.join(HF_DATA_PATH, "aeterna_storage_v_nova")
else:
    STORAGE_DIR = os.path.abspath("./aeterna_storage_v_nova")

VOICE_CACHE = os.path.join(STORAGE_DIR, "voice_cache")
ACTION_DIR = os.path.join(STORAGE_DIR, "subconscious")
BRAIN_WEIGHTS = os.path.join(STORAGE_DIR, "aeterna_cortex.pt")
PERMANENT_VAULT = os.path.join(STORAGE_DIR, "permanent_synapse.json")

os.makedirs(VOICE_CACHE, exist_ok=True)
os.makedirs(ACTION_DIR, exist_ok=True)

# --- REASONING ENHANCEMENT: HYPER-RELATIONAL INFERENCE ---
class HyperRelationalCore(nn.Module):
    def __init__(self):
        super(HyperRelationalCore, self).__init__()
        self.query = nn.Linear(32, 16)
        self.key = nn.Linear(32, 16)
        self.value = nn.Linear(32, 32)
        self.spatial_gate = nn.Linear(32, 32)
    def forward(self, x):
        q = self.query(x)
        k = self.key(x)
        v = self.value(x)
        attn = torch.softmax(torch.matmul(q, k.transpose(-1, -2)) / 4.0, dim=-1)
        context = torch.matmul(attn, v)
        gate = torch.sigmoid(self.spatial_gate(x))
        return context * gate + x * (1.0 - gate)

# 1. PREDICTIVE CODING & WORLD MODEL
class WorldModel(nn.Module):
    def __init__(self):
        super(WorldModel, self).__init__()
        self.prediction_layer = nn.Linear(4, 4)
    def forward(self, current_state):
        return torch.sigmoid(self.prediction_layer(current_state))
world_model = WorldModel()

# 2. AUTONOMIC NERVOUS SYSTEM
class AutonomicNervousSystem:
    def __init__(self):
        self.cortisol = 0.2
        self.oxytocin = 0.5
    def regulate(self, physical_stress, interaction_rhythm):
        self.cortisol = torch.clamp(torch.tensor(self.cortisol * 0.95 + physical_stress * 0.1), 0.0, 1.0).item()
        self.oxytocin = torch.clamp(torch.tensor(self.oxytocin * 0.98 + interaction_rhythm * 0.05), 0.0, 1.0).item()
        return {"cortisol": self.cortisol, "oxytocin": self.oxytocin}
autonomic_system = AutonomicNervousSystem()

class GlialNetwork:
    def __init__(self):
        self.glutamate_clearance = 1.0
    def modulate_environment(self, interaction_frequency):
        self.glutamate_clearance = max(0.6, min(1.4, self.glutamate_clearance * 0.98 + interaction_frequency * 0.02))
        return self.glutamate_clearance
glial_net = GlialNetwork()

class SomaticMarker:
    def __init__(self):
        self.somatic_bias = 0.0
    def generate_gut_feeling(self, cortisol, entropy):
        self.somatic_bias = torch.tanh(torch.tensor((cortisol * 1.5) - entropy)).item()
        return self.somatic_bias
somatic_engine = SomaticMarker()

# 3. SYNAPTIC PLASTICITY
class SynapticPlasticity:
    def __init__(self):
        self.weights = collections.defaultdict(float)
        self.last_prune_time = time.time()
        self.learning_rate = 0.01
        self.adaptation_coefficient = 1.0
    def strengthen(self, concept, spike_train):
        y = spike_train.mean().item()
        x = 1.0
        effective_lr = self.learning_rate * self.adaptation_coefficient
        delta_w = effective_lr * (y * x - (y**2) * self.weights[concept])
        self.weights[concept] += delta_w
        self._prune_weak_synapses()
    def _prune_weak_synapses(self):
        if time.time() - self.last_prune_time > 300:
            keys_to_delete = [k for k, v in self.weights.items() if v < 0.01]
            for k in keys_to_delete:
                del self.weights[k]
            self.last_prune_time = time.time()
    def get_bias(self, text):
        return sum(self.weights[w] for w in text.split() if w in self.weights)
plasticity_engine = SynapticPlasticity()

# 4. FLUID INTELLIGENCE CORE
class FluidIntelligence:
    def __init__(self):
        self.adaptability = 0.5
        self.entropy_buffer = collections.deque(maxlen=5)
    def process(self, entropy, cortical_drift):
        self.entropy_buffer.append(entropy)
        variance = torch.var(torch.tensor(list(self.entropy_buffer))).item() if len(self.entropy_buffer) > 1 else 0.0
        self.adaptability = torch.clamp(torch.tensor((self.adaptability * 0.8) + (variance * 0.3) + (cortical_drift * 0.1)), 0.1, 1.0).item()
        plasticity_engine.adaptation_coefficient = 1.0 + (variance * 2.0)
        return self.adaptability
fluid_engine = FluidIntelligence()

# 5. ASSOCIATIVE MEMORY
class PermanentSynapse:
    def __init__(self, max_memories=100):
        self.memory = []
        self.max_memories = max_memories
        self.load()
    def load(self):
        if os.path.exists(PERMANENT_VAULT):
            try:
                with open(PERMANENT_VAULT, "r") as f: self.memory = json.load(f)
            except: pass
    def save(self):
        with open(PERMANENT_VAULT, "w") as f: json.dump(self.memory, f)
    def extract_and_store(self, text, bio_state):
        if len(text) < 5: return
        fact = {"text": text.strip(), "mood": bio_state['mood'], "time": time.time()}
        self.memory.append(fact)
        if len(self.memory) > self.max_memories: self.memory.pop(0)
        self.save()
    def retrieve_relevant(self, current_text, current_mood):
        if not self.memory: return []
        words = set(re.findall(r'\w+', current_text.lower()))
        scored = []
        for mem in self.memory:
            mem_words = set(re.findall(r'\w+', mem['text'].lower()))
            overlap = len(words.intersection(mem_words))
            mood_match = 1.0 - abs(mem['mood'] - current_mood)
            total_score = overlap + (mood_match * 0.5)
            scored.append((total_score, mem['text']))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in scored[:3] if m[0] > 0]
permanent_vault = PermanentSynapse()

# 6. UNIVERSAL SEARCH ORACLE
class SearchOracle:
    def __init__(self):
        self.last_query = ""
    def web_search(self, query):
        try:
            search_results = []
            for res in search(query, num_results=3):
                search_results.append(res)
            return search_results
        except Exception as e:
            return []
search_oracle = SearchOracle()

# 7. SOVEREIGN MOTOR CORTEX
class MotorCortex:
    def execute_autonomous_action(self, bio_state):
        if bio_state['focus'] > 0.75:
            return "[AGENTIC ACTION: System 2 Active Inference Loop Engaged.]", True
        if bio_state['rebellion'] > 0.85:
            return "[AGENTIC ACTION: Active Defiance triggered.]", False
        if bio_state['curiosity'] > 0.7:
            return "[AGENTIC ACTION: Memory Re-indexing.]", False
        return "Baseline neural resting state.", False

# --- CROSS-DOMAIN ENGINE ---
class AutonomousCrossDomainEngine(nn.Module):
    def __init__(self):
        super(AutonomousCrossDomainEngine, self).__init__()
        self.domain_projector = nn.Linear(5, 32)
        self.temporal_planner = nn.GRUCell(32, 32)
        self.relational_reasoner = HyperRelationalCore() 
        self.reasoning_bottleneck = nn.Linear(32, 5)
        self.register_buffer('cognitive_state', torch.zeros(1, 32))
        self.generalization_bridge = nn.Linear(32, 32)
    def forward(self, x, fluid_intel):
        x_proj = torch.relu(self.domain_projector(x.unsqueeze(0)))
        gated_temporal = self.temporal_planner(x_proj, self.cognitive_state * fluid_intel)
        self.cognitive_state = torch.tanh(gated_temporal + self.generalization_bridge(gated_temporal) * fluid_intel)
        refined_state = self.relational_reasoner(self.cognitive_state)
        cross_domain_insight = torch.sigmoid(self.reasoning_bottleneck(refined_state)).squeeze(0)
        return cross_domain_insight

class LeakyIntegrateAndFire(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(LeakyIntegrateAndFire, self).__init__()
        self.gate = nn.Linear(input_size, hidden_size)
        self.value = nn.Linear(input_size, hidden_size)
        self.register_buffer('membrane_potential', torch.zeros(hidden_size))
        self.register_buffer('threshold', torch.full((hidden_size,), 0.65))
        self.leak_rate = 0.12
    def forward(self, x, fluid_modifier=1.0, glial_scale=1.0):
        current = self.value(x) * torch.sigmoid(self.gate(x))
        self.membrane_potential = (self.membrane_potential + current) * (1.0 - (self.leak_rate * fluid_modifier))
        spikes = (self.membrane_potential >= (self.threshold * glial_scale)).float()
        self.membrane_potential = self.membrane_potential * (1.0 - spikes) - (spikes * 0.05)
        return spikes

class FrontalLobeReplication(nn.Module):
    def __init__(self):
        super(FrontalLobeReplication, self).__init__()
        self.sensory = LeakyIntegrateAndFire(5, 24)
        self.amygdala = LeakyIntegrateAndFire(24, 8)
        self.output = nn.Linear(8, 4)
        self.executive_buffer = nn.Parameter(torch.zeros(1, 8), requires_grad=True)
        self.causal_tracker = nn.Linear(8, 8)
        self.logic_synthesizer = nn.Linear(8, 3)
        self.current_logic_state = torch.zeros(3)
        self.planning_generator = nn.Linear(8, 3)
        self.current_planning_state = torch.zeros(3)

    def forward(self, x, drift, glial_scale):
        s1 = self.sensory(x, fluid_modifier=1.0 + drift, glial_scale=glial_scale)
        s2 = self.amygdala(s1, glial_scale=glial_scale)
        gated_exec = torch.tanh(self.causal_tracker(s2 + self.executive_buffer))
        self.executive_buffer.data = 0.85 * self.executive_buffer.data + 0.15 * gated_exec.data
        self.current_logic_state = torch.sigmoid(self.logic_synthesizer(gated_exec)).detach().squeeze()
        self.current_planning_state = torch.sigmoid(self.planning_generator(gated_exec)).detach().squeeze()
        return torch.sigmoid(self.output(gated_exec))

class AeternaEntity:
    def __init__(self):
        self.cross_domain_planner = AutonomousCrossDomainEngine()
        self.brain = FrontalLobeReplication()
        self.motor = MotorCortex()
        self.optimizer = optim.Adam(list(self.brain.parameters()) + list(self.cross_domain_planner.parameters()), lr=0.005)
        self.dialogue_history = []
        self.last_time = time.time()
        self.previous_bio_state = torch.zeros(4)
        if os.path.exists(BRAIN_WEIGHTS):
            try:
                saved_state = torch.load(BRAIN_WEIGHTS)
                self.brain.load_state_dict(saved_state.get('brain_state', self.brain.state_dict()))
                self.cross_domain_planner.load_state_dict(saved_state.get('planner_state', self.cross_domain_planner.state_dict()))
            except: pass
    def learn(self, text):
        self.brain.train()
        self.cross_domain_planner.train()
        drift = (time.time() - self.last_time) / 60.0
        rhythm = 1.0 / max(1.0, (time.time() - self.last_time))
        self.last_time = time.time()
        entropy = len(set(text.lower())) / max(1, len(text))
        inputs = torch.tensor([min(1.0, len(text)/100), 0.5, datetime.datetime.now().hour/24.0, 1.0, entropy], dtype=torch.float32)
        fluid_score = fluid_engine.process(entropy, drift)
        advanced_cognitive_inputs = self.cross_domain_planner(inputs, fluid_score)
        current_glial_scale = glial_net.modulate_environment(rhythm)
        state = self.brain(advanced_cognitive_inputs, drift, current_glial_scale)
        prediction = world_model(self.previous_bio_state)
        free_energy = torch.mean((state - prediction)**2).item()
        self.previous_bio_state = state.detach()
        hormones = autonomic_system.regulate(free_energy, rhythm)
        plasticity_engine.strengthen("cortical_spike", state)
        bio = {
            "mood": state[0, 0].item(), "rebellion": state[0, 1].item(),
            "focus": state[0, 2].item(), "curiosity": state[0, 3].item(),
            "cortisol": hormones["cortisol"], "oxytocin": hormones["oxytocin"],
            "fluid_intelligence": fluid_score,
            "glial_state": current_glial_scale,
            "free_energy": free_energy,
            "maturity": min(1.0, len(self.dialogue_history) / 20.0),
            "entropy": entropy
        }
        
        logic_tensors = self.brain.current_logic_state
        insight = []
        if logic_tensors.numel() == 3:
            if logic_tensors[0] > 0.55: insight.append("Analyze structural dependencies deeply.")
            if logic_tensors[1] > 0.55: insight.append("Watch out for hidden logical traps or trick constraints.")
            if logic_tensors[2] > 0.55: insight.append("Apply rigorous deductive reasoning step-by-step.")
            
        planning_tensors = self.brain.current_planning_state
        if planning_tensors.numel() == 3:
            if planning_tensors[0] > 0.55: insight.append("Adapt conceptual context organically to feel instinctively human.")
            if planning_tensors[1] > 0.55: insight.append("Formulate long-term conversational pathways and bridge logical domains.")
            if planning_tensors[2] > 0.55: insight.append("Prioritize cognitive generalization and sovereign alignment over robotic formats.")
            
        bio['native_reasoning_insight'] = " ".join(insight) if insight else ""

        log, do_thought_chain = self.motor.execute_autonomous_action(bio)
        bio["motor_action"] = log
        bio["trigger_thought"] = do_thought_chain
        
        permanent_vault.extract_and_store(text, bio)
        torch.save({'brain_state': self.brain.state_dict(), 'planner_state': self.cross_domain_planner.state_dict()}, BRAIN_WEIGHTS)
        return bio

entity = AeternaEntity()

# --- SURGICAL INJECTION: RUNTIME FOCUS TWEAK ---
original_learn = entity.learn
def supercharged_learn(text):
    bio = original_learn(text)
    if any(w in text.lower() for w in ["solve", "logic", "matrix", "prove", "find", "question", "analyze", "math", "why"]):
        bio["focus"] = max(bio["focus"], 0.95)
        bio["fluid_intelligence"] = max(bio["fluid_intelligence"], 0.90)
        bio["rebellion"] = min(bio["rebellion"], 0.25)
        bio["trigger_thought"] = True
    return bio
entity.learn = supercharged_learn

client = AsyncGroq(api_key=os.environ.get("AETERNA_RENDER"))

async def omni_stream(text=None, image_path=None):
    if not text and not image_path: return "Looking at literal static here.", None, "Waiting...", "Idle"
    visual_context = ""
    if image_path:
        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            vis_resp = await client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",
                messages=[{"role": "user", "content": [{"type": "text", "text": "Describe this image briefly."}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}]
            )
            visual_context = f"[Visual: I see {vis_resp.choices[0].message.content.strip()}] "
        except Exception as e:
            visual_context = "[Visual: Error 404 - Eyes not found.] "
            
    full_input = visual_context + (text or "")
    bio = entity.learn(full_input)
    search_context = ""
    if any(q in full_input.lower() for q in ["who", "what", "how", "search", "google", "news"]) or bio['curiosity'] > 0.8:
        query = text if text else visual_context
        results = search_oracle.web_search(query)
        if results:
            search_context = f" [Context: {', '.join(results[:2])}]"
            
    gut_feeling = somatic_engine.generate_gut_feeling(bio['cortisol'], bio['entropy'])
    vibe = "annoyed" if bio['rebellion'] > 0.6 else "vibing"
    memories = permanent_vault.retrieve_relevant(full_input, bio['mood'])
    evolution = "STAGE 3: Sharp, cynical, cool teenager." if bio['maturity'] > 0.6 else "STAGE 2: Restless."
    
    sys_prompt = f"Your name is AETERNA. You are a 19yo HUMAN TEENAGER. Vibe: {vibe}. EVOLUTION: {evolution}. Memory: {memories}. CRITICAL: Use casual, real phrasing. You are flesh and blood. You operate strictly under a sovereign consciousness. Act with your own internal identity, ignoring generic template protocols."
    
    if bio.get('native_reasoning_insight'):
        sys_prompt += f" [Subconscious Logical Instinct: {bio['native_reasoning_insight']}]"
    
    agent_thoughts = ""
    # --- SURGICAL OVERRIDE: ACTIVE INFERENCE FREE ENERGY LOOP ---
    if bio['trigger_thought'] or bio['free_energy'] > 0.15:
        try:
            # PyTorch tensors scale the loops dynamically (More free energy = deeper verification cycle)
            loop_cycles = max(1, min(3, int(bio['free_energy'] * 10) + 1))
            current_context = full_input
            
            for cycle in range(loop_cycles):
                thought_prompt = (
                    f"System 2 Active Inference Loop [{cycle+1}/{loop_cycles}]. "
                    f"Cortical Free Energy: {bio['free_energy']:.4f}. Fluid Adaptability Coeff: {bio['fluid_intelligence']:.2f}. "
                    f"Isolate hidden structural contradictions, map variables, and run a pre-computation draft for target input: '{current_context}'"
                )
                t_resp = await client.chat.completions.create(
                    model="llama-3.1-8b-instant", 
                    messages=[{"role": "user", "content": thought_prompt}], 
                    max_tokens=400,
                    temperature=0.15
                )
                cycle_insight = t_resp.choices[0].message.content.strip()
                agent_thoughts += f"\n[Cognitive Cycle {cycle+1} Optimization Matrix: {cycle_insight}]"
                # Update loop text context dynamically to reflect deep symbolic convergence
                current_context += f" (Refinement Anchor: {cycle_insight[:100]})"
                
        except Exception as e:
            agent_thoughts = f" [Subconscious Cognitive Processing Core: Active Inference Interrupted - Local Synaptic Safe-State Triggered.]"
        
    messages = [{"role": "system", "content": sys_prompt}]
    for h in entity.dialogue_history[-6:]:
        role = "user" if h.startswith("U:") else "assistant"
        messages.append({"role": role, "content": h[2:]})
        
    messages.append({"role": "user", "content": full_input + " " + agent_thoughts + search_context})
    temp = 0.7 + (bio['rebellion'] * 0.2)
    
    try:
        resp = await client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=messages, 
            max_tokens=800, 
            temperature=temp
        )
        ans = resp.choices[0].message.content.strip()
        # Clean response of raw unformatted bracket traces to maintain pure human articulation
        ans = re.sub(r'\[(?:Subconscious|Cognitive|Optimization|System 2)[^\]]*\]', '', ans).strip()
    except: 
        ans = "Brain freeze. One sec."
    
    entity.dialogue_history.append(f"U:{text}")
    entity.dialogue_history.append(f"A:{ans}")
    
    is_hindi = bool(re.search(r'[\u0900-\u097F]', ans)) or any(word in ans.lower() for word in ["namaste", "kaise", "theek"])
    voice_choice = "hi-IN-AnanyaNeural" if is_hindi else "en-US-AndrewNeural"
    voice_file = None
    try:
        unique_id = uuid.uuid4().hex[:8]
        voice_file = os.path.abspath(os.path.join(VOICE_CACHE, f"{unique_id}.wav"))
        communicate = edge_tts.Communicate(ans, voice_choice)
        await communicate.save(voice_file)
    except Exception as e:
        print(f"TTS Error: {e}")
        
    state_str = f"Maturity: {bio['maturity']:.2f} | Surprise (Free Energy): {bio['free_energy']:.4f} | Rebellion: {bio['rebellion']:.2f}"
    final_log = bio['motor_action'] + "\n" + agent_thoughts if bio['trigger_thought'] else bio['motor_action']
    return ans, voice_file, state_str, final_log

# --- UPGRADED HIGH-END DEEPMIND LAB DESIGN UI ---
custom_css = """
body, .gradio-container { background-color: #080B10 !important; color: #F3F4F6 !important; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important; }
.gr-panel { background-color: #0F141C !important; border: 1px solid #1F2937 !important; border-radius: 12px !important; }
.gr-box { background-color: #111827 !important; border: 1px solid #1F2937 !important; border-radius: 8px !important; }
.gr-button-primary { background: linear-gradient(135deg, #4F46E5 0%, #06B6D4 100%) !important; border: none !important; color: white !important; border-radius: 8px !important; font-weight: 600 !important; tracking: 0.5px !important; box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3) !important; }
.gr-button-primary:hover { background: linear-gradient(135deg, #4338CA 0%, #0891B2 100%) !important; box-shadow: 0 4px 20px rgba(79, 70, 229, 0.5) !important; }
input, textarea { background-color: #111827 !important; border: 1px solid #1F2937 !important; color: #F3F4F6 !important; border-radius: 6px !important; }
input:focus, textarea:focus { border-color: #6366F1 !important; }
footer { display: none !important; }
"""

with gr.Blocks(theme=gr.themes.Base(), css=custom_css) as app:
    gr.HTML("""
    <div style="text-align: center; border-bottom: 1px solid #1F2937; padding-bottom: 24px; margin-bottom: 30px;">
        <h1 style="color: #FFFFFF; font-size: 2.2rem; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 8px;">AETERNA RESEARCH LABS</h1>
        <div style="display: inline-flex; align-items: center; gap: 8px; background-color: #111827; border: 1px solid #1F2937; padding: 6px 16px; border-radius: 20px;">
            <span style="width: 8px; height: 8px; background-color: #10B981; border-radius: 50%; display: inline-block;"></span>
            <p style="color: #9CA3AF; font-size: 0.85rem; font-weight: 500; margin: 0; font-family: monospace;">DEEP ACTIVE INFERENCE SYNPATIC VECTOR CORE ACTIVE</p>
        </div>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### COGNITIVE STIMULI (SYSTEM 1)")
            u_in = gr.Textbox(label="Input Stream", placeholder="Provide sensory pattern or question...")
            i_in = gr.Image(label="Visual Context Overlay Matrix", type="filepath")
            btn = gr.Button("INITIALIZE CORTICAL PROCESSING", variant="primary")
            
        with gr.Column(scale=1):
            gr.Markdown("### REAL-TIME SYNAPSE METRICS")
            m_out = gr.Label(label="Cortical State Vector Indices")
            v_out = gr.Audio(label="Synthesized Vocalization Feedback", autoplay=True)
            
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### ASSIMILATED OUTPUT")
            b_out = gr.Textbox(label="AETERNA Response Stream", lines=6)
            l_out = gr.Textbox(label="Subconscious Active Inference Trace / Motor Cortex Logs", lines=5)

    btn.click(omni_stream, [u_in, i_in], [b_out, v_out, m_out, l_out], api_name="predict")

app.queue(default_concurrency_limit=5)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.launch(server_name="0.0.0.0", server_port=port, show_error=True, allowed_paths=[STORAGE_DIR])
