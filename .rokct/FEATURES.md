# Rokct.ai — Features

## Overview
Rok's features are organized into five pillars.
Each pillar is a feature set, not a separate product.
They share one memory, one conversation, one relationship.

---

## Pillar 1: Business

Rok runs your business operations through conversation.
No dashboard required. Everything through WhatsApp.

### ERP Integration
Powered by the Frappe stack — headless, modular, 
multi-tenant. Any business vertical can be added as a 
Frappe app on a tenant (lending, delivery, HR, CRM, 
manufacturing). All ERP operations accessible via 
natural language. Rok only loads tools relevant to the 
current task — no context bloat.

- ✅ Frappe stack — headless, modular, multi-tenant (done)
- ✅ Dynamic tool loading via FrappeDynamicToolset (done)
- ✅ Entity-based tool routing via sentence transformer
  e.g. "create invoice for ABC Corp" loads invoice 
  tools only (done)
- ✅ Tools loaded on demand — no context bloat (done)
- ✅ Role-based access — coding engine disabled 
  for tenants (done)
- ✅ All calls routed via rokct.platform.api.tenant alias (done)
- 🔲 entity_groups.json needs real entries after bake
     Backend: populate after running bake_assets()
     see PENDING_UPDATES.md
- 🔲 Hot reload of entity groups without restart
     Backend: add file watcher to FrappeDynamicToolset

### Invoicing & Finance
Create, submit and send invoices via chat. All financial 
figures come directly from the Frappe API — Rok never 
calculates money independently. Invoice confirmation 
delivered as a WhatsApp card. PDF sent immediately 
after user confirms.

- ✅ Create and submit invoices via chat (done)
- ✅ All financial figures from Frappe API only
     Rok never calculates money independently (done)
- ✅ Invoice confirmation via WhatsApp card format (done)
- ✅ PDF delivered via /send-media after confirmation (done)
- ✅ Card format without uppercase title (done)
- 🔲 Verify invoice belongs to requesting user
     before sending PDF
     Backend: add ownership check in api.tenant
- 🔲 Payment reminders via cron
     Backend: create scheduled job in Frappe

### Operations
Task and todo management via ambient capture. Rok 
detects business intent from casual messages and routes 
to the correct Frappe doctype automatically. If Frappe 
is unreachable, the call is queued locally and retried 
when connection is restored.

- ✅ Task and todo management via ambient capture (done)
- ✅ Intent classification via sentence transformer (done)
- ✅ Offline queue for failed Frappe calls
     (~/.hermes/frappe_queue.json) (done)
- ✅ Retry watcher every 5 minutes (done)
- ✅ User notified on sync failure and on recovery (done)
- ✅ Validation errors shown in plain language (done)
- ✅ Transient errors retried once silently (done)
- 🔲 Frappe create_task and create_reminder methods
     not yet baked — see PENDING_UPDATES.md

### Business Intelligence
Because Rok holds both business and personal context,
it can surface insights no single tool can see. A drop 
in invoicing correlates with a difficult personal week. 
A productivity spike follows a career win. Rok notices 
these patterns and surfaces them proactively.

- 🔲 Cross-pillar correlation engine
     Backend: Frappe background job that queries
     brain/pgvector for business + life event patterns
     and surfaces insights to Rok agent weekly
- 🔲 Insight delivery via WhatsApp card on Monday morning

---

## Pillar 2: Career

Rok tracks your professional growth automatically.
Every achievement logged becomes career capital.
You never need to update your CV manually again.

### Milestone Tracking
Log career events via conversation. Rok classifies 
them as career milestones, skills or achievements and 
stores them permanently in brain/pgvector. Everything 
said becomes searchable career history.

- ✅ Career events logged via conversation (done)
- ✅ Classified by sentence transformer (done)
- ✅ Stored in brain/pgvector via RokctMemoryProvider (done)
- 🔲 Career_Milestone doctype not yet created
     Backend: create in rcore
     Fields: date, title, category, description,
     linked_pillar, is_private, linked_nominee

### CV Generation
CV generated on demand from logged milestones. Always 
up to date — no manual updating required. Rok formats 
it for the role or industry requested and delivers it 
as a PDF on WhatsApp.

- 🔲 CV generation on demand from logged milestones
     Backend: Frappe method that queries brain for
     career events and passes to Rok for formatting
- 🔲 Role-specific CV formatting
     e.g. "write me a CV for a fintech CFO role"
- 🔲 CV delivered as PDF via /send-media
     Backend: PDF generation from Frappe template

### Performance Review Prep
Rok asks every Friday what went well. At year end it 
generates a summary of achievements automatically. 
Users never go into a performance review unprepared 
again.

- 🔲 Weekly wins prompt every Friday via cron
     Backend: scheduled job, delivery via home platform
- 🔲 Year-end achievement summary on request
     Backend: Frappe method querying full year 
     milestones and wins

### Skills & Certifications
Log new skills and certifications via chat. Rok adds 
them to the CV and career profile automatically. No 
manual updating required.

- 🔲 Skill logging via ambient capture
- 🔲 Auto-added to CV and career profile on log
     Backend: trigger CV update on new skill saved

---

## Pillar 3: Productivity

Rok is your accountability partner.
It checks on you — not the other way around.
It prevents the end-of-year feeling of having 
achieved nothing because nothing was written down.

### Goal Setting
Set goals via conversation at any time. Rok checks 
in weekly to ask if you did what you said. At year end 
it shows you what you set out to do vs what you 
actually did.

- 🔲 Goal setting via conversation
     Backend: create Goal doctype in rcore
     Fields: title, target_date, status, 
     linked_pillar, weekly_check_in_enabled
- 🔲 Weekly goal check-in prompt via cron
     Backend: scheduled job every Monday morning
- 🔲 End of year goal vs achievement summary

### Weekly Wins
Every Friday Rok asks what you achieved that week. 
Builds a log of small wins that compound over time. 
Prevents the "I did nothing this year" feeling by 
making the invisible visible.

- 🔲 Friday check-in prompt via cron
     Backend: scheduled job delivery via home platform
- 🔲 Weekly wins stored and linked to career milestones
- 🔲 Year-end wins summary on request

### Ambient Capture
Casual messages are classified by intent automatically. 
No need to open a task app or set a reminder manually. 
Just say it to Rok and it handles the rest. Rok always 
confirms before saving — and always asks whether 
something is a note or a task rather than guessing.

- ✅ Intent classification — Reminder, Task, Note (done)
- ✅ Confirmation loop before saving (done)
- ✅ Note vs Task disambiguation — Rok always asks (done)
- ✅ Reminders delivered back to WhatsApp 
     at scheduled time (done)
- ✅ Reminder delivery on original chat platform (done)
- ✅ Frappe integration via gateway/frappe_integration.py (done)
- 🔲 Goal intent missing from classifier
     Gateway: add Goal to AMBIENT_CAPTURE_CMDS
- 🔲 Frappe backend methods not yet baked
     see PENDING_UPDATES.md

### Accountability Patterns
Rok notices when productivity drops and cross-references 
with life and business pillars to surface the real 
reason. It does not wait to be asked — it tells you 
what it sees.

- 🔲 Pattern detection across pillars
     Backend: brain query comparing business events
     vs personal events vs productivity logs
- 🔲 Proactive insight delivery when pattern detected
     e.g. "You haven't logged a win in 2 weeks and
     your invoicing has dropped — are you okay?"
     Gateway: deliver via home platform card

---

## Pillar 4: Life

Rok is a life companion that listens and remembers.
Everything shared becomes part of your story.
Nothing important is lost.

### Life Logging
Log anything via WhatsApp conversation. Rok classifies 
it as a life milestone, family event, personal 
achievement or memory and stores it permanently. The 
accumulation of these logs becomes the source material 
for the evolving obituary, CV, and life insights.

- ✅ Log anything via WhatsApp conversation (done)
- ✅ Classified and stored in brain/pgvector (done)
- ✅ RokctMemoryProvider bridges agent to Frappe brain (done)
- 🔲 Life_Event doctype not yet created
     Backend: create in rcore
     Fields: date, description, category, sentiment,
     linked_pillar, is_private, linked_nominee

### Proactive Questions
Rok sends periodic prompts to surface memories and 
stories the user might not think to share. Responses 
are stored and woven into the life story. These 
questions are especially important for older users 
who may not initiate conversation but have a lifetime 
of stories worth preserving.

- 🔲 Periodic life prompts via cron
     Backend: Question_Bank doctype with prompt library
     Scheduled job picks random question weekly
     e.g. "What do you remember about your childhood?"
     e.g. "What is the most important lesson 
     from this year?"
- 🔲 Question categories: childhood, family, work,
     beliefs, achievements, regrets, wishes
- 🔲 Responses stored and linked to life story
     Backend: save to Life_Event with 
     source: prompted_question

### Family Tree & Relationships
Log key people in your life and their roles. Store 
wishes and instructions about dependants — especially 
minor children. Who to call, who to trust, who to 
exclude. This is the information families fight over 
when it is not written down.

- 🔲 Family_Member doctype
     Backend: create in rcore
     Fields: name, relationship, phone, trust_level,
     guardian_eligible, excluded_from_custody
- 🔲 Guardian_Preference doctype
     Backend: create in rcore
     Fields: child_name, preferred_guardian,
     excluded_persons, financial_instructions,
     school_instructions, values_to_instill
- 🔲 Capture via conversational flow not form
     Gateway: guided question sequence on 
     family setup

### Health & Wellbeing
Log health events and patterns via conversation. Rok 
notices when personal health struggles affect business 
or career performance and surfaces this connection 
proactively.

- 🔲 Health event logging via ambient capture
- 🔲 Wellbeing patterns surfaced to Rok agent
     Backend: brain query linking health logs
     to productivity and business performance dips

---

## Pillar 5: Legacy

Rok preserves your story for the people you leave 
behind. The obituary is always ready. The vault is 
always secure. Your family will know what to do.

### Evolving Obituary
Built continuously from life logs, career milestones, 
business achievements and personal memories. Never 
written from a form — written from a life. The 
obituary evolves as the user grows. It is always 
ready. The user can request the current draft at 
any time. Sensitive sections are tagged for nominated 
persons only and never revealed to general executors.

- 🔲 Obituary_Draft doctype
     Backend: singleton per user updated on each
     significant life/career/business event saved
     Frappe hook: on_save of Life_Event and
     Career_Milestone triggers Rok to rewrite
     relevant obituary section
- 🔲 User can request current draft via chat
     e.g. "Rok show me my obituary draft"
- 🔲 Version history preserved
     Backend: child table of Obituary_Version rows
- 🔲 Sensitive sections tagged for nominated 
     persons only
     Backend: field is_private on each section,
     linked_nominee field

### The Vault
Secure storage for sensitive end of life information: 
insurance policy numbers and provider contacts, 
physical safe location and PIN (stored encrypted), 
will location and executor details, funeral preferences 
(burial vs cremation, clothing), property and asset 
instructions, digital account access for nominated 
persons.

Vault requires active subscription to remain unlocked. 
On cancellation — life story kept forever, vault 
archived after 90 days with warning.

- 🔲 Legacy_Vault doctype
     Backend: create in rcore
     Fields: insurance policies, safe PIN (encrypted),
     will location, funeral preferences,
     digital account instructions, property details,
     digital account access
- 🔲 Vault items tagged by recipient
     Backend: Legacy_Vault_Item child table
     with nominee link and access_level
- ✅ Subscription status check already implemented (done)
- 🔲 Vault locked for Basic/cancelled users
     Gateway: check tier before returning vault data
- 🔲 Secure web form for PIN entry
     never sent via WhatsApp chat — web only
- 🔲 90 day archive warning on cancellation
     Backend: scheduled job with WhatsApp card warning

### Nominated Persons & Secrets
Some information is only for specific people. Hidden 
assets, private relationships, specific wishes that 
only certain people should know. Rok never reveals 
nominated-only information to general executors — 
access level is enforced at the gateway layer before 
any legacy data is returned.

- 🔲 Nominee doctype
     Backend: create in rcore
     Fields: name, phone, relationship,
     access_level (full/partial/specific_items),
     verification_method
- 🔲 Rok never reveals nominated-only info to others
     Gateway: access_level check before any
     legacy data is returned to executor

### Executor System
The executor is designated during onboarding and given 
an offline PIN verbally. On death, the executor 
messages Rok with the PIN. Rok initiates Protocol 99 — 
contacting the user via WhatsApp, SMS and voice call. 
If there is no response after 6 hours the vault 
unlocks and the executor receives the full legacy 
package.

If the executor is also a Rok user, a role menu is 
presented before routing to the agent so there is no 
confusion between their own account and their 
executor responsibilities.

- 🔲 Legacy_Relationship doctype
     Backend: create in rcore
     Fields: master_user, executor_phone,
     executor_name, access_pin_hash, 
     secondary_contact
- 🔲 Executor role menu when dual user detected
     Bridge: check if incoming number is both
     a Rok user and registered executor for 
     another user — present role menu card
     before routing to agent
- 🔲 Protocol 99 flow
     Gateway: on PIN verification initiate:
     1. WhatsApp message to user via Baileys
     2. SMS to user via Twilio
     3. Voice call to user via Twilio
     Message: "Protocol 99 initiated by [Name].
     Reply STOP within 3 hours if you are alive."
     If no response in 3 hours — contact secondary
     If no response in 6 hours — unlock vault
- 🔲 Vault unlock delivery to executor
     Bridge: deliver structured package as cards
     followed by documents via /send-media
     Obituary card + PDF, insurance contacts card,
     funeral preferences card, nominated items only

### Insurance Notification at Scale
When Rokct has significant users with a specific 
insurer, approach the insurer with verified executor 
contact data. This reduces their unclaimed benefits 
liability and saves them tracing fees. Revenue model: 
fee per successful policy match. User consent is 
captured during onboarding.

- 🔲 Insurance_Policy doctype
     Backend: create in rcore
     Fields: provider, policy_number,
     provider_contact, policy_type, 
     user_consent_given
- 🔲 Consent capture during onboarding
     Gateway: ask user during legacy setup
- 🔲 Monthly report generation when volume reached
     Backend: scheduled job counts policies 
     per insurer — when threshold reached generate
     report and notify admin for outreach

### Funeral Partner Channel
Funeral parlors can market Rokct Legacy to their 
clients as a bundled benefit. The parlor pays Rokct 
a flat fee per member per month. The user owns the 
relationship with Rokct — not the parlor. If the user 
stops paying the parlor, their Rokct account downgrades 
but their life story is never deleted.

Two tiers:
- Basic (R3/user/mo): policy storage, payment 
  reminders, WhatsApp claims handling
- Premium (R10/user/mo): full AI life companion 
  included

The parlor dashboard allows CSV import of members, 
active/lapsed status toggle, claims inbox and 
broadcast messaging to their member base.

- 🔲 Partner_Organization doctype
     Backend: create in rcore
     Fields: name, billing_rate, plan_type,
     active_status, contact_person
- 🔲 Partner_Member doctype
     Backend: create in rcore
     Fields: partner, user, policy_number,
     plan_type (basic/premium), 
     status (active/lapsed)
- 🔲 Partner dashboard
     Frontend: Frappe Desk workspace for 
     Partner Manager role
     Features: CSV import, member list, 
     status toggle, claims inbox, broadcast
- 🔲 CSV import with auto WhatsApp welcome message
     Backend: background job on CSV upload
- 🔲 Lapsed user notification card
     Gateway: when partner marks member lapsed
     send WhatsApp card:
     "Your policy is in arrears. Your Rok vault
     will be downgraded in X days."
- 🔲 Affiliate code system for non-partner referrals
     Backend: referral tracking on signup

### Data Retention Policy
Text and life story is kept forever even after 
cancellation — it costs almost nothing to store and 
is the strongest retention hook. If a user comes 
back 3 years later their whole story is still there.

Vault files, PINs and documents are archived 90 days 
after cancellation with advance warning. If the user 
explicitly requests account deletion (right to be 
forgotten under GDPR/POPIA) everything is wiped 
immediately.

- 🔲 Cancellation flow
     Backend: on subscription cancel keep life 
     story text forever, schedule vault archive 
     in 90 days, send warning card via WhatsApp
- 🔲 Account deletion full wipe on request
     Backend: delete all doctypes, brain engrams,
     session history on confirmed request
     Gateway: confirmation card before wipe
- 🔲 Quarterly vault health check prompt
     Gateway: cron job every 90 days to 
     premium users
     Card: "Is your vault still accurate?
     Reply UPDATE to review your details."

---

## The Interface Layer

All features accessible via WhatsApp conversation.
No app to download. No dashboard to learn. 
No form to fill. Rok meets you where you are.

### Wake Phrase
"Hey Rok" activates a full agent session. Messages 
without the wake phrase are handled by ambient capture 
— classified by intent and acted on without starting 
a full session. Slash commands always work regardless 
of wake phrase.

- ✅ Wake phrase filtering implemented (done)
- ✅ "Hey Rok" activates full agent session (done)
- ✅ Ambient capture handles messages without 
     wake phrase (done)
- ✅ Slash commands always work regardless of 
     wake phrase (done)
- ✅ Wake phrase stripped before passing to agent
     Rok never echoes the unstripped message (done)

### Card Format
Structured output delivered as monospace WhatsApp 
cards. Used for confirmations, summaries, task lists, 
session digests, invoice previews, reminders and 
legacy package delivery. Consistent format across 
all pillars. Safe monospace width of 30 content 
characters respected on all cards.

- ✅ formatCard() implemented in bridge.js (done)
- ✅ Monospace box with correct WhatsApp width (done)
- ✅ Used for confirmations, session digest,
     invoice preview, voice note confirmation (done)
- ✅ Uppercase title removed (done)
- 🔲 Standardize card usage across all pillars
     Bridge: ensure all structured output uses
     card format not plain text

### Session Management
Sessions persist across messages. Pre-reset warning 
gives the user a chance to keep a session alive 
before it auto-resets. Session digest sent periodically 
so the user always knows what Rok is working on. 
Named sessions are resumable. Background sessions 
allow long-running tasks to run while the main chat 
stays responsive.

- ✅ Pre-reset warning with /keep command (done)
- ✅ 10 minute window before reset (done)
- ✅ Session digest delivered every 24 hours via cron (done)
- ✅ Session digest uses card format (done)
- ✅ Named sessions resumable (done)
- ✅ Background sessions for long running tasks (done)
- ✅ Active background processes never auto-reset (done)
- 🔲 Coding engine sessions idle after PR submission
     Gateway: detect PR submitted event and 
     set session to idle

### Streaming & Typing
Rok shows typing indicator while working so the user 
knows it is active. Streaming via message editing 
shows progress updates as tools are called. The final 
edit is the actual response. This makes Rok feel alive 
and responsive even on long tasks.

- ✅ Persistent typing indicator every 5 seconds (done)
- ✅ /typing/stop clears interval (done)
- ✅ Typing cleared on /send (done)
- ✅ Typing cleared on /send-media (done)
- ✅ Streaming via message editing (done)
- 🔲 Verify typing cleared on card send
     Bridge: confirm /send with card object 
     also clears typing interval

### Message Formatting
Rok never overwhelms. Long messages are split 
intelligently. Diff summaries are compact and readable 
on mobile. Rok asks one focused question at a time — 
never a list of clarifying questions. Financial figures 
are always from the API, never calculated by Rok.

- ✅ Long message splitting at 4000 chars (done)
- ✅ Split at sentence boundaries not mid-word (done)
- ✅ Sequential send with delay to prevent reordering (done)
- ✅ Diff format with 30 char monospace limit (done)
- ✅ File paths trimmed from left with ../ (done)
- ✅ Single focused question rule (done)
- ✅ Voice note confirmation before acting (done)
- ✅ Financial data always from API never calculated (done)
- 🔲 Human-like delay between messages
     WhatsApp only — 0.8 to 2.5 seconds default
     base.py keeps default off for other platforms

### Media
Full media support via Baileys bridge. Images, video, 
audio, documents all downloaded and cached locally. 
Voice notes transcribed automatically. PDFs delivered 
as documents. TTS replies sent as voice bubbles not 
file attachments.

- ✅ Image, video, audio, document download and cache (done)
- ✅ PTT/voice note transcription (done)
- ✅ PDF delivery via /send-media (done)
- ✅ Card + document in single /send-media call (done)
- 🔲 TTS replies sent as PTT voice bubbles
     Bridge: send as ptt:true for .ogg and .opus
     not as file attachments

---

## The Memory Layer

One brain. All pillars. Forever. Every conversation 
turn is recorded and vectorized. The longer Rok knows 
you the more it understands the connections between 
your business, career, life and legacy. This is the 
moat — 10 years of context cannot be exported to 
a competitor.

- ✅ RokctMemoryProvider implemented (done)
- ✅ pgvector semantic search via brain Frappe app (done)
- ✅ Every conversation turn recorded and vectorized (done)
- ✅ Tenant-scoped — data never crosses between users (done)
- ✅ Session search via FTS5 (done)
- 🔲 Cross-pillar tagging on engram save
     Backend: tag each engram with pillar
     (business/career/life/legacy/productivity)
     enables cross-pillar correlation queries
- 🔲 Engram scoring and expiry
     Backend: score engrams by access frequency
     archive low-score engrams after 1 year

---

## Pricing

### Personal
- Free: WhatsApp life logging text only, 
  manual legacy release
- Pro ($5/mo): Full AI, vault, CV, evolving obituary,
  ambient capture, career tracking, goal accountability
- Family ($15/mo): 5 accounts, manage legacy 
  for parents, one subscription covers the household

### Business (via Funeral Parlor Partners)
- Basic (R3/user/mo): Policy storage, payment 
  reminders, WhatsApp claims handling
- Premium (R10/user/mo): Full life companion included
- User can upgrade directly to Pro at any time

### Subscription Gating
- ✅ Subscription status check already implemented (done)
- 🔲 Feature gating by tier in gateway
     Gateway: before routing to agent check tier
     Basic — block CV, obituary, vault features
     Free/Lapsed — block vault, show upgrade card
- 🔲 Upgrade prompt card when blocked feature 
     requested
     e.g. "This feature is on Pro ($5/mo).
     Reply UPGRADE to activate."

---

## Pending
See `.rokct/corrections/PENDING_UPDATES.md`
