# Landing Page Generator

Generate a conversion-optimized opt-in landing page for: **$ARGUMENTS**

## Design System
Read these before building anything:
- lead-magnet-system/reference/conversion-landing-sample.html

The reference file is the exact visual pattern to match.

---

## Pipeline:

### Step 1: Research the Topic
Use web search to research "$ARGUMENTS". Find:
- Core value proposition and what makes this topic compelling
- 3-5 specific pain points the audience faces
- Concrete outcomes/benefits to feature in copy
- Any relevant stats or social proof angles

### Step 2: Build the Landing Page
Create the landing page at website/lead-magnets/[slug].html.

Requirements:
- Pure CSS with variables (no Tailwind CDN)
- [YOUR FONT CHOICES] via Google Fonts / CDN
- Full light/dark theme support with localStorage persistence
- Accessible: contrast ratios, alt text, focus states

Sections in order:
1. **Nav Bar** -- fixed, blur backdrop, logo + theme toggle
2. **Hero** -- trust bar (your photo + name + follower count), eyebrow "FREE DOWNLOAD", H1 headline, subhead, value pills, benefits list
3. **Form Card** -- name input, email input, optional qualifying dropdown, submit button, micro-trust icons (no spam, unsubscribe anytime, instant delivery)
4. **FAQ Section** -- 3-4 questions specific to the topic
5. **Final CTA Card** -- inverted card with heading + button
6. **Footer** -- copyright line

Form Integration:
- Webhook URL: [YOUR CRM WEBHOOK URL]
- JavaScript: validate fields, POST FormData to webhook, show success state

### Step 3: Write Delivery Email
Write the plain text delivery email. Save to website/lead-magnets/[slug]-email.txt.

Structure:
- Subject line (short, specific to the topic)
- Hey {{contact.first_name}},
- Opening: 1-2 sentences about what they are getting
- Middle: why this content is valuable
- Closing: tell them to follow you for more content
- Sign off with your name
- PS: invite them to reply with questions

### Step 4: Deploy
1. git add website/lead-magnets/[slug].html website/lead-magnets/[slug]-email.txt
2. git commit -m "Add [title] lead magnet landing page"
3. git push

### Step 5: Summary
Output: page title, slug, files created, live URL, and remind user to paste the email into their CRM automation.
