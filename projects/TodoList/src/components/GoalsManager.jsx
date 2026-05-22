import React, { useState, useEffect, useCallback } from "react";
import Button from "./Button";
import Input from "./Input";
import { loadGoals, saveGoals } from "../utils/localStorageGoals";

export default function GoalsManager() {
  const [goals, setGoals] = useState([]);
  const [newGoal, setNewGoal] = useState("");

  useEffect(() => {
    setGoals(loadGoals());
  }, []);

  useEffect(() => {
    saveGoals(goals);
  }, [goals]);

  const addGoal = useCallback(() => {
    const trimmed = newGoal.trim();
    if (trimmed === "") return;
    setGoals((prev) => [...prev, trimmed]);
    setNewGoal("");
  }, [newGoal]);

  const removeGoal = useCallback((index) => {
    setGoals((prev) => prev.filter((_, i) => i !== index));
  }, []);

  const handleKeyDown = useCallback((e) => {
    if (e.key === "Enter") addGoal();
  }, [addGoal]);

  return (
    <div className="p-4 sm:p-6 md:p-8 bg-background min-h-screen text-text">
      <div className="max-w-lg mx-auto">
        <h1 className="text-primary text-2xl sm:text-3xl font-bold mb-6">
          My Goals
        </h1>
        <div className="flex gap-2 mb-6">
          <Input
            type="text"
            value={newGoal}
            onChange={(e) => setNewGoal(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Add a new goal"
            aria-label="New goal"
            className="flex-1 min-w-0"
          />
          <Button onClick={addGoal} aria-label="Add goal">
            Add
          </Button>
        </div>
        <ul role="list" aria-label="Goals list">
          {goals.length === 0 && (
            <li className="text-gray-500 text-center py-8">
              No goals set yet. Add one above!
            </li>
          )}
          {goals.map((goal, index) => (
            <li
              key={index}
              className="flex justify-between items-center gap-2 p-3 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <span className="break-words">{goal}</span>
              <Button
                size="sm"
                variant="link"
                onClick={() => removeGoal(index)}
                className="text-secondary shrink-0"
                aria-label={`Remove goal: ${goal}`}
              >
                Remove
              </Button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
