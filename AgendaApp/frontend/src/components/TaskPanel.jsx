import { useState } from 'react';

export default function TaskPanel({ tasks, events, onCreateTask, onToggleDone }) {
  const [form, setForm] = useState({ title: '', due_date: '', priority: 'medium', notes: '', event_id: '' });

  const submit = async (e) => {
    e.preventDefault();
    await onCreateTask({ ...form, event_id: form.event_id ? Number(form.event_id) : null });
    setForm({ title: '', due_date: '', priority: 'medium', notes: '', event_id: '' });
  };

  return (
    <div className="card">
      <h3>Tasks</h3>
      <form onSubmit={submit}>
        <input value={form.title} placeholder="Task title" onChange={(e) => setForm({ ...form, title: e.target.value })} required />
        <div className="grid-2">
          <input type="date" value={form.due_date} onChange={(e) => setForm({ ...form, due_date: e.target.value })} />
          <select value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })}>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>
        <select value={form.event_id} onChange={(e) => setForm({ ...form, event_id: e.target.value })}>
          <option value="">Optional linked event</option>
          {events.map((event) => (
            <option key={event.id} value={event.id}>{event.title}</option>
          ))}
        </select>
        <textarea value={form.notes} placeholder="Notes" onChange={(e) => setForm({ ...form, notes: e.target.value })} />
        <button type="submit">Add task</button>
      </form>

      <ul className="list">
        {tasks.map((task) => (
          <li key={task.id}>
            <button className="link" onClick={() => onToggleDone(task)}>
              {task.is_done ? '✅' : '⬜'} {task.title}
            </button>
            <small>{task.priority} · {task.due_date || 'no due date'}</small>
          </li>
        ))}
      </ul>
    </div>
  );
}
