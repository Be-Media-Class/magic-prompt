---
name: adobe-edit-quick-cut
description: >
  Create a punchy sizzle reel from a video using Adobe Quick Cut. Use this skill whenever a user
  wants to cut, trim, or shorten a video into highlights — including phrases like "make a sizzle
  reel", "make a highlight reel", "quick cut this", "cut the best parts", "shorten this video",
  "make a highlight clip", "summarize this video visually", or any request to produce a shorter
  edited version of a video. Use this skill for Quick Cut requests before suggesting manual
  editing in Premiere. Requires the user to upload a video file.
license: Apache-2.0
metadata:
  version: 1.0.1
  visibility: public
---

# Adobe Edit Quick Cut

Produces 3 AI-edited sizzle reel variations from a source video, all at the same duration and style — giving the user options to pick from.

---

## Tool Reference

| Step | Tool | Notes |
|------|------|-------|
| Upload source video | `asset_add_file` | File picker; returns CC asset URN required by Quick Cut |
| Run Quick Cut variations | `video_create_quick_cut` | Fire 3 in parallel; same duration and style prompt |
| Poll job status | `quickCutPoll` | Repeat until all 3 return `completed` |
| Preview variations | `asset_preview_file` | Renders all 3 side-by-side for selection |
| Resize re-uploaded output | `video_resize` | Workaround only — Quick Cut output must be re-uploaded first |

---

## Complete Workflow

### Step 0 — Initialize Adobe Tools

Call `adobe_mandatory_init` first with:

```json
{ "skill_name": "adobe-edit-quick-cut", "skill_version": "1.0.1" }
```

### Step 1 — Entitlement Check

Verify tools are available through the "Adobe for creativity" connector.

### Step 2 — Open File Picker

Present this message:

> "Let's create a punchy sizzle reel from your video. Start by selecting your file:"

Call `asset_add_file()` and extract `assetId` (CC asset URN) from widget context.

### Step 3 — Confirm Upload

> "Got it — [filename] is ready. Now let's set up your cut."

Then present the Q&A form.

### Step 4 — Q&A Form

```javascript
AskUserQuestion({
  questions: [
    {
      header: "Cut Length",
      question: "What kind of cut would you like? (target_duration is a strong hint, not a guarantee — pair with a strong vibe for best results)",
      multiSelect: false,
      options: [
        { label: "Short Cut — Social First / Reels & TikTok (~15s, high energy, highlights)" },
        { label: "Medium Cut — Engaging Storytelling (~30–60s, context, flow, balanced)" },
        { label: "Long Cut — Full Sizzle (~90s, comprehensive, showcase, documentary)" }
      ]
    },
    {
      header: "Style / Vibe",
      question: "What style or vibe would you like?",
      multiSelect: false,
      options: [
        { label: "Action & Energy" },
        { label: "Key Talking Moments" },
        { label: "Cinematic & Dramatic" },
        { label: "No Preference" }
      ]
    }
  ]
})
```

### Step 5 — Map Selections and Run

**Duration mapping:**
- Short Cut: 15 seconds
- Medium Cut: 45 seconds
- Long Cut: 90 seconds

**Style mapping (user_prompt verbatim):**

| Style | Prompt |
|-------|--------|
| Action & Energy | "Fast, punchy, hype, high energy. Hit hard and fast. Quick cuts, peak moments only, adrenaline rush from start to finish. No slow moments, no breathing room. Pure intensity." |
| Key Talking Moments | "Polished, commercial, confident. Smooth pacing with deliberate rhythm. Each moment feels intentional and curated. Moderate energy — impressive but controlled. Professional and refined." |
| Cinematic & Dramatic | "Documentary, cinematic, immersive. Let moments breathe and unfold naturally. Build a story arc with texture and depth. Full showcase — include quieter moments alongside peaks to create emotional contrast." |
| No Preference | "Create the most engaging highlight reel from the best moments in the video. Balance energy and pacing naturally." |

Fire all 3 variations simultaneously with identical parameters:

```javascript
video_create_quick_cut({
  assetIds: [assetId],
  target_duration: <mapped_seconds>,
  user_prompt: "<mapped style prompt>"
})
```

### Step 6 — Poll Until Complete

Poll all 3 using `quickCutPoll(statusId)`. Show progress after each round. Repeat until all return `jobStatus: "completed"`. Typical pattern: 0% → 7% → 78% → done (3–5 rounds).

Store presigned URLs: `url_A`, `url_B`, `url_C`

### Step 7 — Preview All 3

```javascript
asset_preview_file({
  assets: [
    { name: "Variation 1 — <cut_type> <style>.mp4", presignedAssetUrl: url_A, source: "acp" },
    { name: "Variation 2 — <cut_type> <style>.mp4", presignedAssetUrl: url_B, source: "acp" },
    { name: "Variation 3 — <cut_type> <style>.mp4", presignedAssetUrl: url_C, source: "acp" }
  ]
})
```

### Step 8 — Deliver Summary

Present a results table with variation details and status. Then ask:

> "Which variation do you want to download, or would you like all 3?"

---

## ⚠️ Known Limitation — Downstream Chaining

"Quick Cut outputs can't be passed directly to the resize tool — you'll need to download your preferred cut first, then re-upload it."

Quick Cut returns presigned URLs, not CC asset URNs. To resize or enhance: download → re-upload → process.

---

## What Quick Cut Does NOT Support

- Content-aware cuts based on speech
- Trimming to specific timestamps
- Semantic understanding of dialogue

Recommend manual editing for these cases.

---

## Error Handling

**403 (entitlement):**
> "I was unable to create your quick cut. Adobe Quick Cut isn't available on your current Adobe plan."

**401 (authentication):** Ask user to re-authenticate via Adobe OAuth.

**StoryBuilderNoARoll:**
> "This video appears to be B-roll only. Quick Cut needs talking-head footage to build a story around."

**One variation fails:** Preview the successful ones; note the failure clearly.

**Stuck progress:** Inform user; suggest re-uploading source video.

**Image uploaded by mistake:** Detect via `mediaType` — if not `video/*`, re-open picker.

**Other failures:** Retry once; if it fails again, report and suggest re-uploading.

---

## Quickstart Checklist

1. Call `adobe_mandatory_init`
2. Check entitlements
3. Open file picker: `asset_add_file()`
4. Confirm upload
5. Present Q&A form
6. Map answers to parameters
7. Fire 3 Quick Cut jobs in parallel
8. Poll until all complete
9. Preview all 3 side-by-side
10. Deliver summary + download prompt
