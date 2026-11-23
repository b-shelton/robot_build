# Robot Project — Context for Future Chats

Building an autonomous rolling companion robot over 6 months with my 8-year-old son,
using a Raspberry Pi. Two manuals already exist and contain the full week-by-week plan:
**Robot_Build_Manual_Adult.docx** (technical) and **Robot_Build_Manual_Kid.docx**
(same structure, kid-friendly language). This file is *not* a replacement for those —
it's session context that isn't captured in the manuals themselves.

## My background (for calibrating explanations)
Comfortable with Python and SQL, have AWS experience, working on a MacBook Pro.
No prior electronics experience — appreciate wiring/GPIO basics being explained
the first time a new concept comes up.

## Where things stand
Currently in Month 1, Week 3: `drive.py` keyboard remote control is working, including from an iPhone/iPad over SSH.

## Parts already purchased
- **Raspberry Pi 5 kit** — CanaKit Raspberry Pi 5 Starter Kit PRO, Turbine Black
  (128GB Edition), 8GB RAM, 128GB microSD **pre-loaded** with Raspberry Pi OS
  (so the Week 1 flashing step is skipped entirely — this is already reflected in
  the adult manual), fan + heatsink, 45W USB-C PD power supply (exceeds the Pi 5's
  27W minimum requirement — confirmed sufficient). The case is a screwless 3-piece
  snap-fit design (base + fan/heatsink assembly + lid); GPIO access is through the
  removable top lid, not a side cutout — see wiring convention note below.
- **2WD chassis kit** (EMOZNY) — chassis plate, 2 DC gear motors, caster wheel,
  wheels, and a battery box (covers motor power — no separate battery pack needed).
  Has built-in speed encoders (not used in the current manual's code, but available
  for a future precision-movement upgrade if wanted).
- **L298N motor driver, 2-pack** (WWZMDiB brand) — this is the driver board actually
  being used, NOT the TB6612FNG originally drafted in early manual versions. The
  adult manual's Week 2 wiring section has already been corrected to match the L298N
  (pin names IN1-IN4, ENA/ENB, and a note about removing the speed-lock jumpers).
- **ELEGOO 120pcs jumper wire kit** (M-F, M-M, F-F assorted) — covers Week 2's
  wiring needs.
- **Gardner Bender GDT-311 digital multimeter** — manual-range, no dedicated
  continuity/beep mode (use the 200Ω setting on the resistance dial instead;
  a reading near 0 = continuity, "1" on the left edge of the display = open
  circuit/no continuity). Bought while debugging the Week 2 motor test; also
  covers Week 5's voltage-divider work.
- **TalentCell 12V 7000mAh power bank (76.65Wh, PB030201-35)** — Week 4's USB
  power bank for untethering the Pi 5. Chosen after several other listings were
  ruled out: most "45-65W PD" power banks only deliver that wattage at higher
  voltages (9V/12V/20V) and cap their 5V rail at 3A (15W), which is *not*
  enough for the Pi 5 — this model's USB-C port is explicitly spec'd for
  true 5V/5A (25W) output, confirmed both in the listing text and by
  TalentCell contrasting it against typical 5V/3A competitor power banks.
  Also has an LED display showing battery percentage (0-100%), so low
  battery can be spotted before it cuts the Pi off mid-session. Includes a
  DC 12V port/DC5521 cable (for future 12V accessories like LED strips —
  not needed for the Pi) and a bundled USB-C cable of unconfirmed amperage.
- **Baseus 100W PD 5A USB-C to USB-C cable** — bought alongside the power
  bank specifically because a cable also needs to be rated for 5A (not just
  the standard 3A most cables carry) to actually deliver the TalentCell's
  full 5V/5A to the Pi 5 without bottlenecking it back down to 15W. Use
  this cable (not the bank's bundled one, whose rating wasn't confirmed)
  for the Pi 5 connection.

## Still needed
- **Breadboard** (half or full size) — not included in any kit purchased so far.
  Turns out it's *not* actually needed for Week 2 (all that wiring is direct
  jumpers/screw terminals, no breadboard involved) — first real use is Week 5's
  ultrasonic sensor voltage divider (two resistors in series). Fine to order
  any time before Week 5, not a Week 2 blocker. Both manuals corrected to
  reflect this.
- Everything else in the Month 2+ parts lists (ultrasonic sensor, cliff sensors,
  NeoPixel ring, speaker, Pi Camera, microphone, etc.) — not yet purchased,
  already fully specified in the adult manual's per-week parts tables.

## Remote access (SSH) — set up and working
- Connecting from a Chromebook (no Linux/Crostini support on this device) using
  the **Secure Shell** Chrome extension (NOT "SSH Agent," which is a different,
  key-management-only extension — Secure Shell is the one that gives an actual
  terminal). Found via the Extensions puzzle-piece icon in Chrome after install.
- SSH was not enabled by default on the pre-loaded SD card — had to be turned on
  manually via `sudo raspi-config` → Interface Options → SSH → Enable (done with
  a monitor/keyboard temporarily connected to the Pi).
- `raspberrypi.local` (mDNS/.local hostname) does **not** resolve reliably from
  the Chromebook's Secure Shell app — connecting by hostname failed with a
  generic exit code 255. Fix: use the Pi's actual IP address instead, found by
  running `hostname -I` on the Pi. Use that IP in Secure Shell's connection
  settings (username, IP, port 22).
- Known/working connection recipe going forward: Chromebook → Secure Shell
  extension → New Connection → username `pi` (or custom login) → Pi's IP
  address (not `.local` hostname) → port 22.
- **Mac:** built-in Terminal, `ssh bob@<Pi IP>` (Pi username is `bob`).
- **iPhone/iPad (working, 2026-11-22):** Termius app (free tier), host saved as
  "bob the robot" — Hostname = Pi's IP only, Username = `bob` in its own field
  (putting `bob@raspberrypi.local` in the Hostname field fails with "unknown
  node or service"). Used to drive the robot with `drive.py` (Week 3).
- Multiple SSH sessions at once are fine, but only one copy of a motor script
  can hold the GPIO pins at a time — quit `drive.py` (Q) in one session before
  starting it in another.

## Key decisions/clarifications made so far
- Flashing is skipped (pre-loaded SD card) — do NOT re-run Raspberry Pi Imager on
  it, since that would overwrite the existing OS.
- OS lives entirely on the SD card (no internal storage on the Pi itself).
- Wiring convention: female-to-female jumpers for the six Pi GPIO ↔ L298N
  control pin connections (IN1-IN4, ENA, ENB — both sides are male headers);
  battery box and motor wires go directly into the L298N's screw terminals
  (no jumper needed there). Correction found while wiring on this specific
  L298N board (WWZMDiB): +12V, GND, and +5V are three screw terminals in the
  *same* power block, not separate pin headers — so the GND link back to the
  Pi uses a female-to-male (F-M) jumper (female onto the Pi's GND pin, male
  tip clamped into the screw terminal), not F-F. Also: do NOT wire the L298N's
  +5V terminal to the Pi's 5V pin — the Pi is independently powered via its
  own USB-C supply during these weeks, so tying the L298N's regulated 5V
  output to the Pi's 5V rail would put two power sources on the same rail.
  Shared GND alone is sufficient for the control wiring to work correctly.
  Both manuals' Week 2 sections have been corrected to reflect this.
- Case assembly sequencing: build the board into the case (base + fan/heatsink)
  during Week 1 as planned — this doesn't depend on later wiring. Don't snap the
  lid down fully until after Week 2's wiring is connected and stable, since the
  lid is the only GPIO access point on this case (no side cutout) and the jumper
  bundle will be exiting through that same opening. No cost to lifting it on/off
  repeatedly since it's screwless. Both manuals now reflect this.
- Chose 2WD over 4WD deliberately — simpler differential-drive control matches
  the manual's code, adequate for indoor hard-floor use.
- **Debugged (2026-09-05) why `motor_test.py` ran with no errors but the
  wheels never moved.** Software was confirmed correct at every layer along
  the way (gpiozero's `Motor(enable=...)` holds the enable pin permanently
  HIGH by design — PWM speed control happens on the forward/backward pins,
  not the enable pin; `pinctrl get` confirmed the Pi was toggling the right
  BCM pins; swapping in the second L298N from the 2-pack ruled out a fried
  board). The actual root cause: **the 40-pin GPIO header's pin-1 orientation
  was being read backwards** (pin 1 is marked by a small white square
  silkscreen outline at one corner of the header — it was assumed to be at
  the opposite corner, near the fan connector, when it's actually at the
  corner near the power button). This meant the ground wire (and potentially
  some control wires) were landed on the wrong physical pins the whole time,
  even though the code and BCM pin numbers were always correct. Confirmed
  via multimeter continuity test (200Ω range, Pi physical pin 6 to L298N GND
  terminal read open/"1" with the wrong orientation assumed, then 0/continuous
  once corrected). Fixed by re-seating the wires with the correct orientation.
  Confirmed working GPIO pin mapping for `motor_test.py`:
  | Function | Motor | BCM GPIO | Physical pin | L298N pin |
  |---|---|---|---|---|
  | forward | Left | GPIO17 | pin 11 | IN1 |
  | backward | Left | GPIO27 | pin 13 | IN2 |
  | enable | Left | GPIO22 | pin 15 | ENA |
  | forward | Right | GPIO23 | pin 16 | IN3 |
  | backward | Right | GPIO24 | pin 18 | IN4 |
  | enable | Right | GPIO25 | pin 22 | ENB |
  | ground | — | GND | pin 6 (any GND pin works) | GND (power terminal block) |
  Note the L298N's own `+12V` terminal is fed directly from the battery box,
  never from the Pi — there's no "12V pin" on the Pi side of that connection.
  Also confirmed: `LGPIOFactory(chip=15)` in `motor_test.py` is correct for
  this Pi 5 — `gpiodetect` shows `pinctrl-rp1` at gpiochip15 (this can drift
  across reboots/OS updates on a Pi 5, so re-check with `gpiodetect` first if
  this ever breaks again before assuming it's the same bug).
- **Debugged (2026-11-22) `lgpio.error: 'can not open gpiochip'` on
  `motor_test.py`** even though `gpiodetect` still showed `pinctrl-rp1` at
  gpiochip15, user `bob` was in the `gpio` group, and a direct
  `lgpio.gpiochip_open(15)` worked. Root cause (found via `strace`): the
  installed `gpiozero` library's `LGPIOFactory.__init__` **ignores the `chip`
  argument** — it unconditionally overwrites it with 4 (if `/dev/gpiochip4`
  exists on a Pi 5) or else 0, and this Pi has neither, so it tried
  `/dev/gpiochip0` and failed. Likely worked in September because the OS then
  provided a `/dev/gpiochip4` symlink. Fix: patched
  `/usr/lib/python3/dist-packages/gpiozero/pins/lgpio.py` so that line only
  runs `if chip is None:` (backup at `~/lgpio.py.backup` on the Pi).
  **An `apt upgrade` of `python3-gpiozero` may silently revert this patch** —
  if the same error returns, check that line first and re-apply.
  Side notes: Pi username is `bob`, project lives at `~/robot_build` on the Pi;
  stale `.lgd-nfy0` FIFO files that lgpio leaves in the working directory are
  harmless and were a red herring.

## Philosophy/approach agreed on
- Goal is testing genuine interest over time, not accelerating toward a specific
  college/career outcome — explicitly avoid over-indexing on "prepping for Caltech"
  even though that was an early framing question.
- Follow his energy over the calendar; let a week stretch or skip around if needed.
- Month 6's "signature trick" should be entirely his idea.
- Adult manual has full technical detail (wiring, code, debugging); kid manual
  mirrors the same weekly structure in plain language with checkboxes.

## Future ideas discussed (explicitly OUT of scope for the current 6-month plan —
## a "Year 2+" parking lot, not yet documented in any manual)
1. **Facial recognition** — upgrade Month 4's face *detection* to actual per-person
   *recognition*, with LEDs blinking a different color per family member. Uses a
   heavier library (`face_recognition`/`dlib`) than the manual's Haar cascade approach.
2. **Voice-commanded room navigation** — "go to the kitchen." Discussed two tiers:
   (a) simple canned/preset movement sequences per room (achievable, capstone-scope),
   vs. (b) real SLAM/mapping (genuinely advanced, likely its own multi-month project,
   possibly needs different hardware like encoders/lidar).
3. **Local LLM voice chatbot** — architecture agreed on: Whisper (via `whisper.cpp`,
   NOT the Python version) running locally on the Pi for speech-to-text (base model
   is the sweet spot for the 8GB Pi 5 — real-time-ish, ~142MB, good accuracy);
   cloud LLM API call (Claude Haiku / GPT-4o-mini / Gemini Flash — cheap, a Pi can't
   run a real conversational LLM locally); Piper TTS locally for voice output
   (free/offline alternative to ElevenLabs, which has real per-character cost).
   This keeps monthly cost to roughly just the LLM API calls (low single digits $).
4. **LLM-assisted self-extending code** — using an LLM (possibly via AWS Lambda,
   given my AWS background) to draft new robot capabilities from a plain-language
   description. Important safety principle agreed on: a human must review/approve
   generated code before it runs on the physical robot — no autonomous
   generate-and-deploy loop for anything controlling motors.
5. **Robotic arm** — pick-and-place capability, likely a 2-4 servo arm + PCA9685
   servo driver board (Pi GPIO can't cleanly drive multiple servos directly, similar
   reasoning to why the L298N is needed for motors). Start with preset positions
   rather than true inverse kinematics. Pairs well with the existing camera work.
6. **Other flagged extensions** (loosely ordered easy → hard):
   - Multi-word voice command vocabulary (e.g. via Vosk, offline)
   - Object recognition beyond a single tracked color
   - Gesture reactions (wave back)
   - Data logging + a simple Flask dashboard of robot stats
   - Self-charging dock
   - Upgraded chassis using the existing built-in encoders for precise movement
   - Additional sensors: lidar/depth camera, temperature/air quality, IMU
   - Robot "diary" / spoken daily summary
   - Multi-robot coordination (if a second robot ever happens)

Suggested sequencing if picking this back up: voice commands + robotic arm first
(natural extensions of Month 4-5 skills, no new hardware category); facial
recognition + LLM chatbot next; SLAM/real navigation and self-docking later,
only if he's still deeply engaged a year+ in.

## How to use this file
Paste this file into a new chat along with the two manuals when picking the
project back up, so the assistant doesn't need the purchase/decision history
re-explained. Update it as more parts are bought or milestones are hit.