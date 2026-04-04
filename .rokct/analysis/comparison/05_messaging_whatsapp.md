# Comparison Point 5: Messaging Channels & WhatsApp (done)

| Feature | GoClaw (Fork) | Hermes Agent |
| :--- | :--- | :--- |
| **Bundled Bridge** | **No** (Requires manual setup) | **Yes** (Included in `scripts/`) |
| **WhatsApp Setup** | Complex (Manual Node service) | Semi-Auto (`hermes setup gateway`) |
| **WhatsApp Logic** | External TypeScript service | Native Python Adapter + Node Bridge |
| **Voice/Audio** | Basic (Text-to-Speech) | Full Voice-to-Voice (Whisper + TTS) |
| **Channel Range** | 7+ Channels | 12+ Channels (incl. Signal, Matrix) |

### Discussion

A critical difference for your project is that **Hermes Agent comes bundled with a WhatsApp bridge**. In GoClaw, you had to manually build and maintain the `whatsapp-bridge` service. Hermes includes a production-ready Node.js bridge in its `scripts/whatsapp-bridge` directory, which the Python gateway manages automatically.

#### Out-of-the-Box Experience
When you run `hermes gateway setup`, Hermes offers to configure WhatsApp for you. It automatically handles the installation of npm dependencies and manages the lifecycle of the bridge process.

#### Voice Integration
Hermes's native support for voice is its strongest differentiator for a mobile-first "Life Manager."
- **Inbound:** When you send a voice note via WhatsApp, Hermes uses Whisper (local or via Groq) to transcribe it before the agent even "thinks."
- **Outbound:** The agent can respond with audio files using providers like ElevenLabs or OpenAI, allowing for a completely hands-free conversation.

**v0.7.0 Update:**
- **Gateway Hardening:** v0.7.0 provides major stability fixes for photo media delivery and race conditions in the gateway.
- **Approval Routing:** Improved routing for `/approve` and `/deny` commands ensure tool results are no longer lost when the agent is blocked waiting for user confirmation on WhatsApp.
