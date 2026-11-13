# Toolbox: Chris's starred repos, and where each fits

Free, open-source tools from Chris's GitHub stars, mapped to the Shorts Studio pipeline.
Agents use a tool only after it's installed; if it's missing, they say so and give the install
command below. Nothing here costs credits.

## Wired into the workflow

| Repo | What it is | Where it fits | Install |
|---|---|---|---|
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | Write HTML, render video. Seekable animation (GSAP, CSS, Three.js, Lottie), rendered frame by frame in headless Chrome with FFmpeg. | **Animator:** code route for faceless and brainrot (HTML + Three.js scenes). **Editor:** the horror layout (hook header + 16:9 clip window + caption block) as one reusable HTML composition; caption blocks. **Idea-scout:** `/reverse-any-video` to break down a reference video into beats. | Needs Node 22+ and FFmpeg. Skills: `npx skills add heygen-com/hyperframes`. New project: `npx hyperframes init <slug>`, then `npx hyperframes preview` / `npx hyperframes render`. |
| [debpalash/VoiceStudio](https://github.com/debpalash/VoiceStudio) | Local, open-source ElevenLabs alternative: voice cloning, dubbing, transcription. Runs on CPU (slower) or GPU. | **Voices (review memory R4):** clone Chris's voice from one clean recording, and build each recurring character's voice once. Replaces robotic TTS. Has a CLI, a local API, and MCP support. | Mac: `brew tap debpalash/tap && brew install --cask debpalash/tap/voicestudio`. Windows: `irm https://voicestudio.sh/install.ps1 \| iex`. Mac/Linux: `curl -fsSL https://voicestudio.sh/install \| sh`. |
| [nvm-sh/nvm](https://github.com/nvm-sh/nvm) | Node version manager. | Gets the Node 22+ that HyperFrames needs. | See its README, then `nvm install 22`. |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) | Animation and motion skills (when and how to animate, curves, timing). | **Animator:** motion feel for code-built shots (easing, timing, follow-through), so moves don't look robotic. | `npx skills add emilkowalski/skills` |

## Voice setup (one time, about 15 minutes)
1. Record 1-2 minutes of Chris reading anything calm and clear, in a quiet room, into
   footage/_voices/chris-reference.wav.
2. In VoiceStudio, add it under Voice cloning and save the voice as "Chris".
3. For each recurring character (styles/brainrot-cast.md, styles/horror-cast.md), save one voice
   and write its name in the cast file's Voice column.
4. Check each model's license in VoiceStudio's Model Manager allows commercial use (monetized
   channel) before using it. Note it in the cast file.

## Optional, not wired in

| Repo | Why it's not in the pipeline (yet) |
|---|---|
| [drowzeys/Imagination-Studio-by-keys-Wasserman](https://github.com/drowzeys/Imagination-Studio-by-keys-Wasserman) | Local AI film studio (pictures and video with sound). Could replace paid credits for horror and brainrot route: ai, but needs an Apple Silicon Mac or NVIDIA DGX Spark. Try it if Chris has that hardware. |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem), [MemPalace/mempalace](https://github.com/MemPalace/mempalace) | Session memory for agents. docs/review-memory.md and docs/log.md already cover what the studio needs to remember. Revisit if sessions keep forgetting context. |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable), [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | Design skills for web pages and apps. Useful for night-patrol or a decant shop site, not for video. |
| [anthropics/skills](https://github.com/anthropics/skills), [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official), [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | General skill and plugin catalogs. Browse them when a new need comes up. |
| HKUDS/DeepTutor, morluto/rea, trimstray/the-book-of-secret-knowledge, vinta/awesome-python, awesome-selfhosted/awesome-selfhosted | Learning and reference (Linux, home server, Python). Fit Chris's tech-learning goals more than the studio. |
