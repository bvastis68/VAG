import { useEffect, useState } from 'react';
import {
  Alert,
  AppState,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import AsyncStorage from '@react-native-async-storage/async-storage';
import {
  DEFAULT_HABITS,
  dateKey,
  streak,
  toggleToday,
  weekCount,
  weeklyProgress,
} from './src/habits';

const STORAGE_KEY = 'habits.v1';

const colors = {
  bg: '#F7F7F5',
  card: '#FFFFFF',
  text: '#1A1A1A',
  muted: '#8A8A85',
  line: '#E6E6E1',
  accent: '#2E7D5B',
  accentSoft: '#E3F1EA',
  danger: '#C8423B',
};

export default function App() {
  return (
    <SafeAreaProvider>
      <HabitScreen />
    </SafeAreaProvider>
  );
}

function HabitScreen() {
  const [habits, setHabits] = useState(null); // null until loaded from storage
  const [today, setToday] = useState(new Date());
  const [newName, setNewName] = useState('');
  const [editing, setEditing] = useState(false);

  // Load once from on-device storage.
  useEffect(() => {
    AsyncStorage.getItem(STORAGE_KEY)
      .then((raw) => setHabits(raw ? JSON.parse(raw) : DEFAULT_HABITS))
      .catch(() => setHabits(DEFAULT_HABITS));
  }, []);

  // Save on every change after the initial load.
  useEffect(() => {
    if (habits) AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(habits));
  }, [habits]);

  // Roll over to the new day when the app comes back to the foreground.
  useEffect(() => {
    const sub = AppState.addEventListener('change', (state) => {
      if (state === 'active') setToday(new Date());
    });
    return () => sub.remove();
  }, []);

  if (!habits) return <View style={styles.screen} />;

  const todayKey = dateKey(today);
  const doneToday = habits.filter((h) => h.done.includes(todayKey)).length;
  const week = weeklyProgress(habits, today);

  const toggle = (id) =>
    setHabits((hs) => hs.map((h) => (h.id === id ? toggleToday(h, today) : h)));

  const add = () => {
    const name = newName.trim();
    if (!name) return;
    setHabits((hs) => [...hs, { id: String(Date.now()), name, done: [] }]);
    setNewName('');
  };

  const remove = (habit) =>
    Alert.alert('Remove habit?', `"${habit.name}" and its history will be deleted.`, [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Remove',
        style: 'destructive',
        onPress: () => setHabits((hs) => hs.filter((h) => h.id !== habit.id)),
      },
    ]);

  return (
    <SafeAreaView style={styles.screen} edges={['top', 'left', 'right']}>
      <StatusBar style="dark" />
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        <ScrollView contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">
          <View style={styles.header}>
            <View>
              <Text style={styles.date}>
                {today.toLocaleDateString(undefined, {
                  weekday: 'long',
                  month: 'long',
                  day: 'numeric',
                })}
              </Text>
              <Text style={styles.title}>Today</Text>
            </View>
            <Pressable onPress={() => setEditing((e) => !e)} hitSlop={12} style={styles.editBtn}>
              <Text style={styles.editText}>{editing ? 'Done' : 'Edit'}</Text>
            </Pressable>
          </View>

          <View style={styles.card}>
            <View style={styles.weekRow}>
              <Text style={styles.weekLabel}>This week</Text>
              <Text style={styles.weekValue}>
                {week.completed} / {week.total}
              </Text>
            </View>
            <View style={styles.barTrack}>
              <View style={[styles.barFill, { width: `${Math.round(week.ratio * 100)}%` }]} />
            </View>
            <Text style={styles.subtle}>
              {doneToday} of {habits.length} done today · {Math.round(week.ratio * 100)}% of the week
            </Text>
          </View>

          {habits.map((h) => {
            const done = h.done.includes(todayKey);
            const days = streak(h.done, today);
            return (
              <View key={h.id} style={styles.rowWrap}>
                <Pressable
                  onPress={() => (editing ? remove(h) : toggle(h.id))}
                  style={({ pressed }) => [
                    styles.row,
                    done && !editing && styles.rowDone,
                    pressed && { opacity: 0.7 },
                  ]}
                  accessibilityRole="checkbox"
                  accessibilityState={{ checked: done }}
                  accessibilityLabel={h.name}
                >
                  {editing ? (
                    <View style={styles.removeDot}>
                      <Text style={styles.removeDotText}>−</Text>
                    </View>
                  ) : (
                    <View style={[styles.check, done && styles.checkOn]}>
                      {done && <Text style={styles.checkMark}>✓</Text>}
                    </View>
                  )}
                  <View style={{ flex: 1 }}>
                    <Text style={[styles.habitName, done && !editing && styles.habitNameDone]}>
                      {h.name}
                    </Text>
                    <Text style={styles.subtle}>{weekCount(h.done, today)}/7 this week</Text>
                  </View>
                  {!editing && (
                    <View style={styles.streak}>
                      <Text style={styles.streakNum}>{days}</Text>
                      <Text style={styles.streakLabel}>{days === 1 ? 'day' : 'days'}</Text>
                    </View>
                  )}
                </Pressable>
              </View>
            );
          })}

          {habits.length === 0 && (
            <Text style={[styles.subtle, { textAlign: 'center', marginVertical: 24 }]}>
              No habits yet. Add one below.
            </Text>
          )}

          <View style={styles.addRow}>
            <TextInput
              value={newName}
              onChangeText={setNewName}
              placeholder="New habit"
              placeholderTextColor={colors.muted}
              style={styles.input}
              returnKeyType="done"
              onSubmitEditing={add}
            />
            <Pressable
              onPress={add}
              style={({ pressed }) => [styles.addBtn, pressed && { opacity: 0.7 }]}
            >
              <Text style={styles.addBtnText}>Add</Text>
            </Pressable>
          </View>
          {editing && (
            <Text style={[styles.subtle, { textAlign: 'center' }]}>Tap a habit to remove it.</Text>
          )}
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg },
  content: { padding: 20, paddingBottom: 48, gap: 12 },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
    marginBottom: 8,
  },
  date: { fontSize: 15, color: colors.muted, fontWeight: '500' },
  title: { fontSize: 36, fontWeight: '700', color: colors.text, letterSpacing: -0.5 },
  editBtn: { paddingVertical: 8, paddingHorizontal: 4 },
  editText: { fontSize: 17, color: colors.accent, fontWeight: '600' },

  card: {
    backgroundColor: colors.card,
    borderRadius: 18,
    padding: 18,
    gap: 10,
    borderWidth: 1,
    borderColor: colors.line,
  },
  weekRow: { flexDirection: 'row', justifyContent: 'space-between' },
  weekLabel: { fontSize: 17, fontWeight: '600', color: colors.text },
  weekValue: { fontSize: 17, fontWeight: '600', color: colors.accent },
  barTrack: { height: 12, borderRadius: 6, backgroundColor: colors.line, overflow: 'hidden' },
  barFill: { height: '100%', borderRadius: 6, backgroundColor: colors.accent },
  subtle: { fontSize: 14, color: colors.muted },

  rowWrap: { borderRadius: 18, overflow: 'hidden' },
  row: {
    minHeight: 80,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
    paddingHorizontal: 18,
    paddingVertical: 14,
    backgroundColor: colors.card,
    borderRadius: 18,
    borderWidth: 1,
    borderColor: colors.line,
  },
  rowDone: { backgroundColor: colors.accentSoft, borderColor: colors.accentSoft },
  check: {
    width: 36,
    height: 36,
    borderRadius: 18,
    borderWidth: 2,
    borderColor: colors.line,
    alignItems: 'center',
    justifyContent: 'center',
  },
  checkOn: { backgroundColor: colors.accent, borderColor: colors.accent },
  checkMark: { color: '#fff', fontSize: 20, fontWeight: '700' },
  removeDot: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: colors.danger,
    alignItems: 'center',
    justifyContent: 'center',
  },
  removeDotText: { color: '#fff', fontSize: 24, fontWeight: '700', marginTop: -2 },
  habitName: { fontSize: 19, fontWeight: '600', color: colors.text },
  habitNameDone: { color: colors.accent },
  streak: { alignItems: 'center', minWidth: 48 },
  streakNum: { fontSize: 24, fontWeight: '700', color: colors.text },
  streakLabel: { fontSize: 12, color: colors.muted },

  addRow: { flexDirection: 'row', gap: 10, marginTop: 8 },
  input: {
    flex: 1,
    height: 56,
    borderRadius: 14,
    paddingHorizontal: 16,
    fontSize: 17,
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.line,
    color: colors.text,
  },
  addBtn: {
    height: 56,
    paddingHorizontal: 22,
    borderRadius: 14,
    backgroundColor: colors.accent,
    alignItems: 'center',
    justifyContent: 'center',
  },
  addBtnText: { color: '#fff', fontSize: 17, fontWeight: '700' },
});
