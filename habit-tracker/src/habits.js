// Pure helpers for dates, streaks and weekly progress. No React here.

export const DEFAULT_HABITS = [
  'Drink water',
  'Morning workout',
  'Golf practice',
  'Read 20 pages',
].map((name, i) => ({ id: `default-${i}`, name, done: [] }));

// Local-time YYYY-MM-DD. toISOString() would use UTC and flip days early in the evening.
export function dateKey(date = new Date()) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

function addDays(date, n) {
  const copy = new Date(date);
  copy.setDate(copy.getDate() + n);
  return copy;
}

// Consecutive days completed, ending today. If today isn't done yet the
// streak is still alive, so count back from yesterday.
export function streak(done, today = new Date()) {
  const set = new Set(done);
  let day = set.has(dateKey(today)) ? today : addDays(today, -1);
  let count = 0;
  while (set.has(dateKey(day))) {
    count += 1;
    day = addDays(day, -1);
  }
  return count;
}

// Monday through Sunday of the week containing `today`.
export function weekKeys(today = new Date()) {
  const offset = (today.getDay() + 6) % 7; // Monday = 0
  const monday = addDays(today, -offset);
  return Array.from({ length: 7 }, (_, i) => dateKey(addDays(monday, i)));
}

export function weekCount(done, today = new Date()) {
  const week = new Set(weekKeys(today));
  return done.filter((k) => week.has(k)).length;
}

export function weeklyProgress(habits, today = new Date()) {
  const total = habits.length * 7;
  const completed = habits.reduce((sum, h) => sum + weekCount(h.done, today), 0);
  return { completed, total, ratio: total ? completed / total : 0 };
}

export function toggleToday(habit, today = new Date()) {
  const key = dateKey(today);
  const done = habit.done.includes(key)
    ? habit.done.filter((k) => k !== key)
    : [...habit.done, key];
  return { ...habit, done };
}
