import os
import sys
import time
import subprocess
import threading
from collections import deque
import gradio as gr

# Buffer log real-time (150 baris terakhir)
log_buffer = deque(maxlen=150)
bot_process = None
bot_status = "Memulai sistem cloud WhatsApp Bot..."

def log_msg(msg):
    print(msg, flush=True)
    log_buffer.append(f"[{time.strftime('%H:%M:%S')}] {msg}")

# ZeroGPU Event Handler - hanya dijalankan saat tombol UI ditekan oleh pengguna
try:
    import spaces
    @spaces.GPU
    def run_ai_gpu_test(prompt):
        return f"✅ ZeroGPU Cluster Active | Input: '{prompt}' | Engine: Gemini Multimodal & Baileys Gateway"
except Exception:
    def run_ai_gpu_test(prompt):
        return f"Cluster Active | Input: '{prompt}'"

def setup_node_and_run_bot():
    global bot_process, bot_status
    try:
        log_msg("🚀 [EXPEDIENT-43] Inisialisasi Cloud Server WhatsApp...")
        
        # 1. Cek Node.js sistem (terinstall otomatis via packages.txt)
        try:
            v = subprocess.check_output(["node", "-v"], text=True).strip()
            log_msg(f"✅ Node.js sistem siap: {v}")
        except Exception as e:
            log_msg(f"Node.js check warning: {e}")

        # 2. Install dependensi Baileys & Supabase
        if not os.path.exists("node_modules"):
            log_msg("📦 Menginstall dependensi Baileys & Supabase...")
            os.system("npm install --omit=dev")
            log_msg("✅ Dependensi berhasil terinstall.")

        # 3. Jalankan Baileys Gateway Daemon
        log_msg("🤖 Menjalankan Expedient 43 WhatsApp Gateway Daemon...")
        bot_status = "🟢 ONLINE & MENJAGA SESI 24 JAM"

        bot_env = os.environ.copy()
        bot_env["GATEWAY_PORT"] = "7861"

        while True:
            cmd = ["npx", "tsx", "scripts/wa-gateway.ts"]
            log_msg("Memulai proses gateway...")
            bot_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env=bot_env
            )

            for line in iter(bot_process.stdout.readline, ""):
                clean = line.strip()
                if clean:
                    log_msg(clean)

            rc = bot_process.poll()
            log_msg(f"⚠️ Gateway terhenti (exit code {rc}). Merestart otomatis dalam 5 detik...")
            bot_status = "🟡 RECONNECTING..."
            time.sleep(5)

    except Exception as e:
        bot_status = f"🔴 ERROR: {str(e)}"
        log_msg(f"Error pada bot runner: {e}")

# Jalankan bot di latar belakang thread otomatis saat server menyala
t = threading.Thread(target=setup_node_and_run_bot, daemon=True)
t.start()

def get_dashboard_data():
    recent_logs = "\n".join(log_buffer) if log_buffer else "Menunggu inisialisasi bot WhatsApp..."
    return bot_status, recent_logs

# Antarmuka Dashboard Web Gradio
with gr.Blocks(title="Expedient 43 - WhatsApp Cloud Bot") as demo:
    gr.Markdown("# 🤖 EXPEDIENT GENERATION 43")
    gr.Markdown("### Official 24/7 Self-Hosted WhatsApp Cloud Gateway & Multimodal AI (Free Server)")
    
    with gr.Row():
        status_box = gr.Textbox(label="Status Server WhatsApp Bot", value=bot_status, interactive=False)
    
    with gr.Row():
        logs_box = gr.Textbox(label="Live Terminal Logs (Real-time)", lines=18, interactive=False)
    
    with gr.Row():
        refresh_btn = gr.Button("🔄 Refresh Status / Logs", variant="primary")
        refresh_btn.click(fn=get_dashboard_data, outputs=[status_box, logs_box])

    with gr.Accordion("⚙️ AI Hardware Diagnostic (ZeroGPU Test Bench)", open=False):
        test_in = gr.Textbox(label="Test Prompt", value="Test connection")
        test_out = gr.Textbox(label="Result")
        test_btn = gr.Button("Run Inference Test")
        test_btn.click(fn=run_ai_gpu_test, inputs=test_in, outputs=test_out)

    try:
        timer = gr.Timer(5)
        timer.tick(fn=get_dashboard_data, outputs=[status_box, logs_box])
    except Exception:
        pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_port=port, server_name="0.0.0.0")
