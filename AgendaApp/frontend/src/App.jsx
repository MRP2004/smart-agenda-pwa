import { useEffect, useMemo, useState } from 'react';
import AuthPanel from './components/AuthPanel';
import CalendarBoard from './components/CalendarBoard';
import EventQuickAdd from './components/EventQuickAdd';
import TaskPanel from './components/TaskPanel';
import { request } from './api';

const reminderOptions = [5, 15, 60];

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [events, setEvents] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [filters, setFilters] = useState({ q: '', category: '' });
  const [customReminder, setCustomReminder] = useState(30);

  const auth = (newToken) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
  };

  const loadData = async () => {
    const query = new URLSearchParams();
    if (filters.q) query.append('q', filters.q);
    if (filters.category) query.append('category', filters.category);

    const [eventsResponse, tasksResponse] = await Promise.all([
      request(`/api/events?${query.toString()}`, { token }),
      request('/api/tasks', { token }),
    ]);
    setEvents(eventsResponse);
    setTasks(tasksResponse);
  };

  useEffect(() => {
    if (token) loadData();
  }, [token, filters.q, filters.category]);

  const createEvent = async (payload) => {
    await request('/api/events', { method: 'POST', body: payload, token });
    await loadData();
  };

  const createTask = async (payload) => {
    await request('/api/tasks', { method: 'POST', body: payload, token });
    await loadData();
  };

  const toggleTask = async (task) => {
    await request(`/api/tasks/${task.id}`, {
      method: 'PUT',
      body: { is_done: !task.is_done },
      token,
    });
    await loadData();
  };

  const registerReminder = async (minutesBefore) => {
    if (!events[0]) return;
    await request('/api/reminders', {
      method: 'POST',
      token,
      body: {
        event_id: events[0].id,
        minutes_before: minutesBefore,
        daily_summary: false,
      },
    });
    if ('Notification' in window) {
      await Notification.requestPermission();
    }
  };

  const visibleEvents = useMemo(() => events, [events]);

  if (!token) {
    return (
      <main className="container auth-layout">
        <AuthPanel onAuth={auth} />
      </main>
    );
  }

  return (
    <main className="container">
      <section className="card">
        <h1>Smart Agenda</h1>
        <div className="grid-2">
          <input
            placeholder="Search title, location, notes"
            value={filters.q}
            onChange={(e) => setFilters({ ...filters, q: e.target.value })}
          />
          <select value={filters.category} onChange={(e) => setFilters({ ...filters, category: e.target.value })}>
            <option value="">All categories</option>
            <option value="subject">Subject</option>
            <option value="practice">Practice</option>
            <option value="exam">Exam</option>
            <option value="personal">Personal</option>
          </select>
        </div>
        <div className="toolbar">
          {reminderOptions.map((minutes) => (
            <button key={minutes} onClick={() => registerReminder(minutes)}>
              Remind {minutes} min
            </button>
          ))}
          <button onClick={() => registerReminder(customReminder)}>Custom {customReminder} min</button>
        </div>
      </section>

      <EventQuickAdd onCreate={createEvent} />
      <CalendarBoard events={visibleEvents} />
      <TaskPanel tasks={tasks} events={events} onCreateTask={createTask} onToggleDone={toggleTask} />
    </main>
  );
}
