import { useState } from 'react';
import { loginRequest, request } from '../api';

export default function AuthPanel({ onAuth }) {
  const [isRegister, setIsRegister] = useState(false);
  const [form, setForm] = useState({ full_name: '', email: '', password: '' });
  const [error, setError] = useState('');

  const submit = async (event) => {
    event.preventDefault();
    setError('');
    try {
      if (isRegister) {
        await request('/api/auth/register', { method: 'POST', body: form });
      }
      const tokenData = await loginRequest(form.email, form.password);
      onAuth(tokenData.access_token);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <form className="card" onSubmit={submit}>
      <h2>{isRegister ? 'Create account' : 'Sign in'}</h2>
      {isRegister && (
        <input
          placeholder="Full name"
          value={form.full_name}
          onChange={(e) => setForm({ ...form, full_name: e.target.value })}
          required
        />
      )}
      <input
        placeholder="Email"
        type="email"
        value={form.email}
        onChange={(e) => setForm({ ...form, email: e.target.value })}
        required
      />
      <input
        placeholder="Password"
        type="password"
        value={form.password}
        onChange={(e) => setForm({ ...form, password: e.target.value })}
        required
      />
      {error && <p className="error">{error}</p>}
      <button type="submit">Continue</button>
      <button type="button" className="link" onClick={() => setIsRegister(!isRegister)}>
        {isRegister ? 'I already have an account' : 'Create new account'}
      </button>
    </form>
  );
}
