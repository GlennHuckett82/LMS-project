import React, { useEffect, useState } from 'react';
import './TeacherDashboard.css';
import api from '../services/api';
import { useAuth } from '../auth/AuthContext';
import { useNavigate } from 'react-router-dom';

interface CourseRow {
  id: number;
  title: string;
  description?: string;
  created_at?: string;
}

// Simple teacher control panel: lists your courses and lets you create new ones.
// Kept intentionally direct so a beginner can trace data loading and creation in one file.
const TeacherDashboard: React.FC = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const [courses, setCourses] = useState<CourseRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [creating, setCreating] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  // Load only the courses owned by the logged-in teacher; handles paginated or plain arrays.
  const fetchMyCourses = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get('courses/my/');
      const payload = res?.data;
      const list: CourseRow[] = Array.isArray(payload)
        ? payload
        : Array.isArray(payload?.results)
        ? (payload.results as CourseRow[])
        : [];
      setCourses(list);
    } catch (e: any) {
      setError(e?.message || 'Failed to load courses');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Initial page load: populate the table so you immediately see what you own.
    fetchMyCourses();
  }, []);

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2 className="heading-xl">Teacher Dashboard</h2>
        <button className="button" onClick={() => { logout(); navigate('/'); }}>Logout</button>
      </div>
      <p>Welcome, teacher! Here you can manage your courses.</p>

      <div className="card card--spaced">
        <h3>Create Course</h3>
        <div className="create-controls">
          <input
            aria-label="Course title"
            type="text"
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          <input
            aria-label="Course description"
            type="text"
            placeholder="Description (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
          <button
            className="button"
            disabled={creating || !title.trim()}
            onClick={async () => {
              setError(null);
              setCreating(true);
              try {
                const payload = { title: title.trim(), description: description.trim() || undefined };
                await api.post('courses/', payload);
                setTitle('');
                setDescription('');
                await fetchMyCourses();
              } catch (e: any) {
                const msg = e?.response?.data?.detail || e?.message || 'Failed to create course';
                setError(typeof msg === 'string' ? msg : JSON.stringify(msg));
              } finally {
                setCreating(false);
              }
            }}
            aria-label="Create course"
            title="Create course"
          >
            {creating ? 'Creating…' : 'Create'}
          </button>
        </div>
      </div>

      {error && <div className="auth-error">{error}</div>}
      {loading ? (
        <p>Loading your courses...</p>
      ) : courses.length === 0 ? (
        <p>You have no courses yet. Create one to get started.</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Description</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {courses.map((c) => (
              <tr key={c.id}>
                <td>{c.id}</td>
                <td>{c.title}</td>
                <td>{c.description || ''}</td>
                <td>{c.created_at || ''}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default TeacherDashboard;
