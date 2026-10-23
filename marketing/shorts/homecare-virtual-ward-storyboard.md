# Short storyboard — Home care · Virtual Ward (split)

Vertical marketing short for the EyeNet **Home care · Virtual Ward** case. **Master cut is split-screen**, matching `homecare-virtual-ward-split-15s.mp4`.

| | |
|---|---|
| **Working title** | Virtual Ward — hospital-grade safety at home |
| **Layout** | **9:16 split** — top half = people / scenario · bottom half = EyeNet product UI |
| **Master deliverable** | `marketing/shorts/homecare-virtual-ward-split-15s.mp4` (~15s) |
| **Alt (full-frame)** | `marketing/shorts/homecare-virtual-ward-15s.mp4` (earlier single-frame cut) |
| **Audience** | Care providers · MDT / care coordinators · eHealth partners |
| **Source** | `value/why/home-care/` · Care coordinator beat on `value/with-eyenet/` |
| **Product UI** | Real EyeNet screenshots under `marketing/shorts/assets/eyenet-wiki/` |
| **Atmosphere ref** | `value/assets/images/homecare-caregiver-presence.jpg` (Talos — top-half mood only) |
| **Tone** | Calm, clinical-confident · never voyeuristic |

---

## Split layout (locked)

```
┌─────────────────────────┐
│  TOP — people / scenario│  photoreal home-care acting
├─────────────────────────┤  soft horizontal divider
│  BOTTOM — EyeNet UI     │  camera-entry → real product screens
└─────────────────────────┘
```

- **Top:** only people and the home environment (no fake UI overlays).  
- **Bottom:** only product truth — starts with **view entering the camera lens**, then real wiki screenshots.  
- **Sync:** what happens on top drives which EyeNet screen appears below.

---

## Real EyeNet UI assets (bottom half — not mock UI)

Paths relative to `marketing/shorts/assets/eyenet-wiki/`.

| Role | File | Notes |
|---|---|---|
| Ordinary camera / Cameras list | `camera-card.png` | Connected camera card |
| Detection armed | `camera-card-detect.png` | Instant detection on |
| Live detect / stream | `stream-detect.png` · `instant-detection.png` | Live vision |
| Automation home | `automation-toolbar.png` | Triggers & Actions |
| **Trigger** | `trigger-card.png` · `create-trigger-demographic.png` | Rule on detections |
| **Trigger** (fall / posture) | `trigger-logs-body-posture.png` | Fall / body-posture cue |
| **Action** | `action-card.png` · `create-action-alert.png` | Alert / follow-up |
| Presence / visit assurance | `presence-actions.png` · `presence-camera.png` | Caregiver presence |

Source: `/Users/nickgklezakos/Documents/ppl-meta-code/docs/documentation/wiki/owners-admins/images/`

---

## Narrative spine (split)

Top: unstaffed home → caregiver arrives → help moment needs care.  
Bottom: **enter the camera** → camera card → detect → **trigger** → **action**.  
Together: few targeted alerts, vision on-prem, Virtual Ward.

---

## Storyboard — 15s master (split)

| # | Time | TOP — people / scenario | BOTTOM — EyeNet UI | On-screen text (optional captions) | VO / tone |
|---|------|-------------------------|--------------------|--------------------------------------|-----------|
| 1 | 0–2s | Quiet unstaffed living room, soft morning light. No staff. | Dark / ambient; begin push toward a physical camera lens. | **Unstaffed home.** Still a ward. | Calm open |
| 2 | 2–3.5s | Hold room · subtle life in the space. | **Liked intro:** view **entering** the regular IP camera glass (vignette into the lens). | Any ordinary camera. | Grounding |
| 3 | 3.5–6s | Caregiver approaches / enters the home doorway. | Smash into product: **`camera-card.png`** → **`camera-card-detect.png`**. Optional bridge: **`stream-detect.png`**. | Becomes a vision node. | Product truth |
| 4 | 6–9s | Visit assurance — caregiver present with the person at home. | Presence cue: **`presence-actions.png`** / **`presence-camera.png`** (brief) then Automation → **`trigger-card.png`**. | **Right staff. Right home. Right time.** | Assurance |
| 5 | 9–12s | Tasteful non-graphic stumble / help-call energy (ethical framing). | **Trigger** pinned: **`trigger-card.png`** (± **`trigger-logs-body-posture.png`**) → **Action**: **`create-action-alert.png`** / **`action-card.png`**. | **Trigger → Action** — alert the care team. | Controlled urgency |
| 6 | 12–15s | Calm recovery / coordinator care energy; home still respectful. | Hold **`action-card.png`** / alert payoff. No video wall. Soft end. | Hospital-grade safety at home. · **EyeNet** Virtual Ward | Payoff / end |

**Keyframe pins used in production (bottom half):**  
~3.5s `camera-card.png` · ~6s `camera-card-detect.png` · ~9s `trigger-card.png` · ~12s `action-card.png`

---

## Signature sequence (must hit)

**Bottom half**

1. **Enter the camera** — push into physical lens  
2. **Camera in EyeNet** — `camera-card.png` → `camera-card-detect.png`  
3. **Trigger** — `trigger-card.png` (± body-posture log)  
4. **Action** — `create-action-alert.png` / `action-card.png`

**Top half stays in sync** — arrival with camera/detect; help moment with trigger→action.

Do not invent fake EyeNet chrome on the bottom.

---

## Extended 40–45s split (optional longer cut)

Same layout; stretch top/bottom pairs:

| Beat | TOP | BOTTOM |
|---|---|---|
| Open | Unstaffed home | Enter camera lens |
| Node | Caregiver arrives | Camera card → detect → stream |
| Presence | Visit in progress | Presence Actions UI |
| Fall / help | Ethical help moment | Trigger log → Action alert |
| Zone | Doorway unknown presence | Same trigger→action pattern |
| Privacy | Quiet home + care continues | On-prem lock sense (no cloud video wall) |
| Payoff | Coordinator calm | Action / alert reprise + end card |

---

## Copy anchors (keep faithful to value page)

**Capabilities**

- Caregiver presence — right staff, right home, right time (visit assurance)
- Secure zones — alarm on unspecified persons in/around the dwelling
- Fall detection — automation trigger → care team
- Voice / help-call — spoken request for help → immediate actionable alert
- Clinical fuse — tokenized events into ePokratis / IoMT / telemedicine (**not** cloud video)
- Virtual Ward — hospital-level care at home: admission avoidance & early discharge

**Why it matters**

> Differentiator vs vitals-only RPM: the home becomes a monitored care environment. Privacy by architecture — vision stays on-prem; only fall / help / presence / zone events reach the health stack.

**Care coordinator line**

> With EyeNet, a care coordinator gets hospital-grade safety in every unstaffed home — falls, help-calls, and zone breaches as a few targeted alerts in the clinical app.

**Tags:** `Presence` · `Automation` · `Fall` · `Voice` · `Area · Spot` · `Talos · TMAIX`

---

## Shot list (split production)

1. Top room plate + bottom lens-entry (liked intro)  
2. Top caregiver arrive ‖ bottom `camera-card` → `camera-card-detect`  
3. Top visit assurance ‖ bottom presence UI → `trigger-card`  
4. Top help moment ‖ bottom trigger → action alert  
5. Top calm payoff ‖ bottom action card hold + end title  

---

## Don’ts

- Do not break the split (no full-bleed UI covering the people; no people covering the UI)  
- No continuous “watching the patient” live-wall vibe on either half  
- No graphic medical trauma or panic UI spam  
- Do not imply cloud clinical video  
- **Do not use fake product UI** on the bottom when a wiki screenshot exists  

---

## CTA options

- Primary: Learn more — EyeNet Home care · Virtual Ward  
- Secondary: Talos eHealth / TMAIX integration path  
- Link: value wiki `/why/home-care/`
