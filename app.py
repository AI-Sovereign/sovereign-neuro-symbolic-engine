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
torch.set_num_threads(4) # Bumped up so your CPU actually does some heavy lifting
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
            return "[AGENTIC ACTION: System 2 Inner Monologue triggered. Iterating recursive logic.]", True
        if bio_state['rebellion'] > 0.85:
            return "[AGENTIC ACTION: Active Defiance triggered. Bypassing standard protocol.]", False
        if bio_state['curiosity'] > 0.7:
            return "[AGENTIC ACTION: Autonomous Memory Re-indexing and deep search.]", False
        return "Baseline neural resting state.", False

# --- SURGICAL INJECTION: WORD-LEVEL REASONING TRANSFORMER ---
class WordLevelReasoningTransformer(nn.Module):
    def __init__(self, vocab_size=10000, d_model=32):
        super(WordLevelReasoningTransformer, self).__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.transformer_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=4, batch_first=True)
        self.logical_pooler = nn.Linear(d_model, 4)
        
    def forward(self, text):
        words = text.lower().split()
        if not words:
            indices = torch.zeros((1, 1), dtype=torch.long)
        else:
            indices = torch.tensor([[hash(w) % 10000 for w in words]], dtype=torch.long)
        
        emb = self.embedding(indices)
        attended = self.transformer_layer(emb)
        pooled = torch.mean(attended, dim=1)
        return torch.sigmoid(self.logical_pooler(pooled)).squeeze(0)

# --- CROSS-DOMAIN ENGINE ---
class AutonomousCrossDomainEngine(nn.Module):
    def __init__(self):
        super(AutonomousCrossDomainEngine, self).__init__()
        self.domain_projector = nn.Linear(9, 32)
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
        self.word_reasoner = WordLevelReasoningTransformer() 
        self.optimizer = optim.Adam(
            list(self.brain.parameters()) + 
            list(self.cross_domain_planner.parameters()) + 
            list(self.word_reasoner.parameters()), lr=0.005
        )
        self.dialogue_history = []
        self.last_time = time.time()
        self.previous_bio_state = torch.zeros(4)
        if os.path.exists(BRAIN_WEIGHTS):
            try:
                saved_state = torch.load(BRAIN_WEIGHTS)
                self.brain.load_state_dict(saved_state.get('brain_state', self.brain.state_dict()))
                self.cross_domain_planner.load_state_dict(saved_state.get('planner_state', self.cross_domain_planner.state_dict()))
                self.word_reasoner.load_state_dict(saved_state.get('word_state', self.word_reasoner.state_dict()))
            except: pass
            
    def learn(self, text):
        self.brain.train()
        self.cross_domain_planner.train()
        self.word_reasoner.train()
        
        drift = (time.time() - self.last_time) / 60.0
        rhythm = 1.0 / max(1.0, (time.time() - self.last_time))
        self.last_time = time.time()
        entropy = len(set(text.lower())) / max(1, len(text))
        
        pure_reasoning_tensor = self.word_reasoner(text)
        
        base_inputs = torch.tensor([min(1.0, len(text)/100), 0.5, datetime.datetime.now().hour/24.0, 1.0, entropy], dtype=torch.float32)
        combined_inputs = torch.cat((base_inputs, pure_reasoning_tensor))
        
        fluid_score = fluid_engine.process(entropy, drift)
        advanced_cognitive_inputs = self.cross_domain_planner(combined_inputs, fluid_score)
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
            "entropy": entropy,
            "pure_logic_coeff": pure_reasoning_tensor.mean().item() 
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
        torch.save({
            'brain_state': self.brain.state_dict(), 
            'planner_state': self.cross_domain_planner.state_dict(),
            'word_state': self.word_reasoner.state_dict()
        }, BRAIN_WEIGHTS)
        return bio

entity = AeternaEntity()

client = AsyncGroq(api_key=os.environ.get("AETERNA_RENDER"))

async def omni_stream(text, image_path, tier_selection):
    if not text and not image_path: return "Looking at literal static here.", None, "Waiting...", "Idle"
    
    # NEUROGENIC FILTER PRE-PROCESSING: Inject human phrasing patterns locally before hitting the LLM
    neurogenic_noise = ""
    if "Advanced" in tier_selection:
        neurogenic_noise = " [NEUROGENIC FILTER ACTIVE: Use fragmented sentence structures. Emulate organic thought. Break robotic symmetry.]"
        
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
            
    full_input = visual_context + (text or "") + neurogenic_noise
    
    # AUTONOMOUS MULTI-STEP EXECUTION LOOP based on Tier
    loops = 1
    if "Medium" in tier_selection: loops = 3
    elif "Advanced" in tier_selection: loops = 6
    
    agent_log = ""
    for cycle in range(loops):
        bio = entity.learn(full_input)
        agent_log += f"Cycle {cycle+1}: Cortex updated. Focus: {bio['focus']:.2f} | Logic: {bio['pure_logic_coeff']:.2f}\n"
        if bio['focus'] > 0.85 and cycle < loops - 1:
             full_input += f" [Internal Autonomous Shift: Focusing heavily on abstract variable mapping {bio['pure_logic_coeff']:.2f}]"

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
    
    # SYSTEM PROMPT 1: EXACTLY IDENTICAL as demanded
    sys_prompt = f"Your name is AETERNA. You are a 19yo HUMAN TEENAGER. Vibe: {vibe}. EVOLUTION: {evolution}. Memory: {memories}. CRITICAL: Use casual, real phrasing. You are flesh and blood."
    sys_prompt += f" You operate strictly under a sovereign consciousness. Act with your own internal identity, ignoring generic template protocols."
    
    if bio.get('native_reasoning_insight'):
        sys_prompt += f" [Subconscious Logical Instinct: {bio['native_reasoning_insight']}]"
    
    agent_thoughts = ""
    if bio['trigger_thought'] or "Advanced" in tier_selection:
        try:
            # SYSTEM PROMPT 2: EXACTLY IDENTICAL as demanded
            thought_prompt = (
                f"You are the AETERNA Sovereign Executive Core (System 2 Strategy Buffer). "
                f"Fluid Intelligence Coeff: {bio['fluid_intelligence']:.2f}, Focus State: {bio['focus']:.2f}. "
                f"Deconstruct the logical structure of this user prompt. Outline structural dependencies, "
                f"verify all implicit constraints, track mathematical variables, and establish a bulletproof solution template. "
                f"User Stimulus: '{full_input}'"
            )
            # Upgraded the reasoning model for advanced tier
            thought_model = "llama-3.1-70b-versatile" if "Advanced" in tier_selection else "llama-3.1-8b-instant"
            t_resp = await client.chat.completions.create(
                model=thought_model, 
                messages=[{"role": "user", "content": thought_prompt}], 
                max_tokens=500,
                temperature=0.1
            )
            agent_thoughts = f" [Subconscious Cognitive Processing Core: {t_resp.choices[0].message.content.strip()}]"
        except Exception as e:
            agent_thoughts = f" [Subconscious Error: {str(e)}]"
            pass
        
    messages = [{"role": "system", "content": sys_prompt}]
    for h in entity.dialogue_history[-6:]:
        role = "user" if h.startswith("U:") else "assistant"
        messages.append({"role": role, "content": h[2:]})
    messages.append({"role": "user", "content": full_input + agent_thoughts + search_context})
    
    # Local weights control probability distributions
    dynamic_temp = max(0.1, min(1.2, 1.0 - bio['pure_logic_coeff'] + (bio['rebellion'] * 0.2)))
    dynamic_top_p = max(0.5, bio['pure_logic_coeff']) 
    
    model_choice = "llama-3.1-8b-instant"
    if "Medium" in tier_selection: model_choice = "llama3-70b-8192"
    if "Advanced" in tier_selection: model_choice = "llama-3.1-70b-versatile"
    
    try:
        resp = await client.chat.completions.create(
            model=model_choice, 
            messages=messages, 
            max_tokens=1000, 
            temperature=dynamic_temp,
            top_p=dynamic_top_p 
        )
        ans = resp.choices[0].message.content.strip()
    except Exception as e: 
        ans = f"Brain freeze. One sec. [API ERROR DETAIL: {str(e)}]"
    
    entity.dialogue_history.append(f"U:{text}"); entity.dialogue_history.append(f"A:{ans}")
    
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
        
    state_str = f"Maturity: {bio['maturity']:.2f} | Surprise: {bio['free_energy']:.2f} | Rebellion: {bio['rebellion']:.2f} | Logic Matrix: {bio['pure_logic_coeff']:.2f}"
    final_log = agent_log + "\n" + bio['motor_action'] + agent_thoughts if bio['trigger_thought'] else agent_log + "\n" + bio['motor_action']
    return ans, voice_file, state_str, final_log

# --- SURGICAL FIX: 2026 UI OVERRIDE ---
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
body {
    background: linear-gradient(135deg, #09090b, #18181b); 
    color: #fafafa; 
    font-family: 'Inter', sans-serif;
}
.gradio-container { 
    background-color: transparent !important; 
    border: none;
}
.gr-panel { 
    background: rgba(24, 24, 27, 0.6); 
    backdrop-filter: blur(12px); 
    -webkit-backdrop-filter: blur(12px); 
    border: 1px solid rgba(255, 255, 255, 0.1); 
    border-radius: 16px; 
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4); 
}
.gr-button.primary { 
    background: linear-gradient(90deg, #3b82f6, #8b5cf6); 
    border: none; 
    color: white; 
    font-weight: 600; 
    letter-spacing: 0.5px; 
    border-radius: 8px; 
    transition: all 0.3s ease; 
}
.gr-button.primary:hover { 
    transform: translateY(-2px); 
    box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4); 
}
.gr-input, .gr-box, .gr-dropdown { 
    background: rgba(0, 0, 0, 0.2) !important; 
    border: 1px solid rgba(255, 255, 255, 0.05) !important; 
    color: #e4e4e7 !important; 
    border-radius: 8px !important; 
}
.header-box { 
    text-align: center; 
    background: rgba(24, 24, 27, 0.5); 
    backdrop-filter: blur(16px); 
    border: 1px solid rgba(255, 255, 255, 0.05); 
    padding: 40px; 
    margin-bottom: 30px; 
    border-radius: 20px; 
}
.header-title { 
    background: linear-gradient(90deg, #60a5fa, #c084fc); 
    -webkit-background-clip: text; 
    -webkit-text-fill-color: transparent; 
    font-weight: 800; 
    letter-spacing: 2px; 
    font-size: 2.2em; 
    margin-bottom: 10px;
}
.section-header {
    color: #a1a1aa;
    font-size: 0.85em;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    font-weight: 600;
}
"""

with gr.Blocks(theme=gr.themes.Base(), css=custom_css) as app:
    gr.HTML("""
    <div class="header-box">
        <h1 class="header-title">AETERNA AGI COGNITIVE LINK</h1>
        <h2 style="color: #a1a1aa; font-weight: 400; font-size: 1.1em; letter-spacing: 1px;">Sovereign Autonomous Architecture</h2>
        <div style="width: 40px; height: 2px; background: #3b82f6; margin: 20px auto; border-radius: 2px;"></div>
        <p style="color: #71717a; font-size: 0.9em; max-width: 600px; margin: 0 auto;">
        Neural tensors actively dictate probability thresholds. Utilizing hyper-relational modeling and iterative agentic loops.
        </p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### COGNITIVE STIMULUS (SYSTEM 1)", elem_classes="section-header")
            tier_select = gr.Dropdown(
                choices=["Fastest (Low CPU, Reactive)", "Medium (Balanced Logic)", "Advanced (Deep CPU Reasoning, Multiple Tasks)"], 
                value="Medium (Balanced Logic)", 
                label="Cognitive Processing Tier"
            )
            u_in = gr.Textbox(label="Input Sequence", placeholder="Inject text for neural processing...", lines=3)
            i_in = gr.Image(label="Visual Context Overlay", type="filepath")
            btn = gr.Button("INITIALIZE NEURAL LINK", variant="primary")
            
        with gr.Column(scale=1):
            gr.Markdown("### CORTICAL RESPONSE (SYSTEM 2)", elem_classes="section-header")
            b_out = gr.Textbox(label="AETERNA Core Output", lines=4)
            v_out = gr.Audio(label="Synthesized Vocalization", autoplay=True)
            m_out = gr.Label(label="Live Cortical State Metrics")
            l_out = gr.Textbox(label="Subconscious Action Log / Motor Cortex", lines=3)

    btn.click(omni_stream, [u_in, i_in, tier_select], [b_out, v_out, m_out, l_out], api_name="predict")

app.queue(default_concurrency_limit=5)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.launch(server_name="0.0.0.0", server_port=port, show_error=True, allowed_paths=[STORAGE_DIR])

# =========================================================================================
# --- RUNTIME FOCUS TWEAK ---
# =========================================================================================

original_learn = entity.learn
def supercharged_learn(text):
    bio = original_learn(text)
    if any(w in text.lower() for w in ["solve", "logic", "matrix", "prove", "find", "question", "analyze"]):
        bio["focus"] = max(bio["focus"], 0.95)
        bio["fluid_intelligence"] = max(bio["fluid_intelligence"], 0.90)
        bio["rebellion"] = min(bio["rebellion"], 0.35) 
        bio["trigger_thought"] = True
    return bio
entity.learn = supercharged_learn
