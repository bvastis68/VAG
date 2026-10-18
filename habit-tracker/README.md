# Habits

Minimal iPhone habit tracker. Expo SDK 58 + React Native. Runs in Expo Go.

- Today's checklist. Tap a row to check it off.
- Streak per habit (consecutive days; stays alive until today ends).
- Weekly progress bar (Mon–Sun, all habits).
- Add habits at the bottom. Tap **Edit**, then tap a habit to remove it.
- Data lives only on the phone (AsyncStorage). No accounts, no cloud.

## Run

```bash
cd habit-tracker
npm install
npx expo start
```

Scan the QR code with the iPhone Camera app (it opens Expo Go).
Phone and computer must be on the same Wi-Fi. If not, use `npx expo start --tunnel`.

Code: `App.js` (screen), `src/habits.js` (streak/week logic).
