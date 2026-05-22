// src/utils/localStorageGoals.js

const GOALS_STORAGE_KEY = "user_goals";

export function loadGoals() {
  const stored = localStorage.getItem(GOALS_STORAGE_KEY);
  return stored ? JSON.parse(stored) : [];
}

export function saveGoals(goals) {
  localStorage.setItem(GOALS_STORAGE_KEY, JSON.stringify(goals));
}
