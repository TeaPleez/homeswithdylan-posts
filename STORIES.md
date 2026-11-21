# Sharing Instagram stories via Meta Business Suite

IMPORTANT (learned Nov 21 2026): on the Creator account @homeswithdylan, SCHEDULED stories are accepted by
Business Suite but FAIL to publish at the scheduled time ("Story failed to publish"). "Share now" works.
So stories are shared at their time by the "Share open house story" scheduled tasks, using steps 1-4 below
and then the blue "Share" button (leave the Schedule section on "Share now"). Do not schedule stories.
Runs in the Claude desktop app's built-in browser pane on Dylan's Mac.

## Make the frames
python3 story.py --slides <folder with slide-01.jpg (cover) … slide-NN.jpg> --out <out folder> \
  --variant thu|sat --sat-date "Nov 21" --year 2026 --days both|sat|sun
- --days: which days have open houses (caption lines "📍 SATURDAY" / "📍 SUNDAY").
- Writes story-01.jpg (9:16 cover; "This weekend…" for thu, "Today & tomorrow…" for sat) + story-02.jpg… (one per listing).
- Max 10 frames per story (cover + 9 listings). LOOK at the frames before uploading.
- Put them in posts/<Thu YYYY-MM-DD>-openhouse-story-thu/ and -story-sat/, commit + push, wait ~90 s for Pages (relay 404 = not deployed yet; wait 60 s and retry).

## Share one story (all frames in one go)
Steps 1-4, then click the blue "Share" button at the bottom ONCE, wait ~20 s, then check
https://business.facebook.com/latest/posts/active_stories?business_id=689683847537534&asset_id=1000087319863101
(re-check after ~60 s; frames can take a minute) — one "Photo · 5 seconds" row per frame with today's time.

## (Old) scheduling steps — do not use on the Creator account
1. Navigate (force:true) to https://business.facebook.com/latest/story_composer?asset_id=1000087319863101&business_id=689683847537534 , wait ~3 s.
2. javascript_exec — hook the file picker (same code as PUBLISHING.md step 2).
3. find "Add photo/video", left_click it by ref (real click).
4. javascript_exec — same relay code as PUBLISHING.md step 4, but names = posts/<folder>/story-01.jpg … story-NN.jpg. Wait ~8 s, then check
   (document.body.innerText.match(/1080 × 1920/g)||[]).length equals N (note the × character).
5. find "Schedule" and click the generic "Schedule" toggle next to "Share now" (in the Schedule section).
6. Date: find textbox "mm/dd/yyyy", triple_click it, type MM/DD/YYYY, press Tab.
7. Time: spinbuttons hours / minutes / meridiem — click hours and type the digit(s); click minutes and press ArrowDown/ArrowUp until correct (typing digits doesn't work); click meridiem and type A or P.
8. Verify: input mm/dd/yyyy value (e.g. "Nov 21, 2026") and spinbutton aria-valuenow/valuetext.
9. Click the blue "Schedule" button at the bottom ONCE (the last "Schedule" match from find). It jumps to the Planner.
10. Confirm at https://business.facebook.com/latest/posts/scheduled_stories?business_id=689683847537534&asset_id=1000087319863101 — one "Photo · 5 seconds" row per frame at the right date/time. That page is also the duplicate check: if rows already exist at that exact date/time, the story is already scheduled — don't schedule again.
Never use "Share now". Never schedule without Dylan's approval.
